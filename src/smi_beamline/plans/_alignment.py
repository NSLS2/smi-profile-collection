"""Bounded scan/fit/move recovery, independent of beamline device instances."""

import bluesky.plan_stubs as bps
import bluesky.plans as bp
import numpy as np
from ophyd.utils import LimitError


def _check_positions(motor, *positions):
    """Preflight through the motor, including pseudo-to-real limit checks."""
    for position in positions:
        if not np.isfinite(position):
            raise RuntimeError(f"Alignment of {motor.name}: non-finite position {position}")
        try:
            motor.check_value(float(position))
        except (LimitError, ValueError) as exc:
            raise RuntimeError(
                f"Alignment of {motor.name}: position {position:g} would exceed "
                f"motor limits; cannot continue the scan. {exc}"
            ) from exc


def _profile_feature(stats, *, der, target):
    """Locate the measured peak/edge, without trusting an extrapolated fit."""
    x = np.asarray(stats.x_data, dtype=float)
    y = np.asarray(stats.y_data, dtype=float)
    if (len(x) < 3 or x.shape != y.shape or not np.all(np.isfinite(x))
            or not np.all(np.isfinite(y)) or np.ptp(y) == 0):
        raise RuntimeError("No usable alignment feature: flat, non-finite, or insufficient scan data")
    order = np.argsort(x)
    x, y = x[order], y[order]
    if np.any(np.diff(x) <= 0):
        raise RuntimeError("No usable alignment feature: repeated motor positions")

    # A falling knife edge has a NEGATIVE derivative. Its strongest change,
    # rather than the numerical maximum (usually background), gives direction.
    if der:
        feature = x[np.argmax(np.abs(y))]
        at_edge = feature in (x[0], x[-1])
    elif target == "cen" and stats.fit_kind == "step":
        i = np.argmax(np.abs(np.diff(y) / np.diff(x)))
        feature = (x[i] + x[i + 1]) / 2
        at_edge = i in (0, len(x) - 2)
    else:
        feature = x[np.argmax(y)]
        at_edge = feature in (x[0], x[-1])
    return x[0], x[-1], feature, at_edge


def scan_and_center(detectors, motor, rang, point, stats, *, der=False,
                    target="cen", max_retries=3):
    """Relative alignment scan with at most ``max_retries`` edge-centered rescans.

    Fit centers must be finite, inside the measured interval, and accompanied
    by an interior measured feature. Both center and peak are checked because
    the enclosing alignment routines may subsequently use either statistic.
    Failed fits use the measured peak/strongest slope to choose the nearer
    scan edge, never the sign or magnitude of a runaway fitted center.
    The rescan retains the original width and point count. All endpoints are
    checked before recentering, including the real limits of pseudo motors.
    """
    if not np.isfinite(rang) or rang <= 0 or point < 4:
        raise ValueError("Alignment requires a positive finite range and at least 4 points")
    if not isinstance(max_retries, int) or max_retries < 0:
        raise ValueError("max_retries must be a non-negative integer")
    if target not in ("cen", "peak"):
        raise ValueError("target must be 'cen' or 'peak'")

    visited = []
    for attempt in range(max_retries + 1):
        center = float(motor.position)
        low, high = center - rang, center + rang
        _check_positions(motor, low, high)
        visited.append(center)
        uid = yield from bp.rel_scan(detectors, motor, -rang, rang, point)
        # Bind statistics to THIS scan, not whichever run happens to be latest.
        fit_error = None
        try:
            stats(uid=uid, der=der, plot=False)
        except (ValueError, FloatingPointError) as exc:
            # ps resets its results and records the profile before fitting.
            fit_error = str(exc)

        xmin, xmax, feature, at_edge = _profile_feature(stats, der=der, target=target)
        valid = (fit_error is None and stats.fit_success
                 and np.isfinite(stats.cen) and xmin < stats.cen < xmax
                 and np.isfinite(stats.peak) and xmin <= stats.peak <= xmax
                 and not at_edge)
        if valid:
            position = float(getattr(stats, target))
            _check_positions(motor, position)
            yield from bps.mv(motor, position)
            return position

        reason = fit_error or (
            f"center={stats.cen!r}, measured interval=[{xmin:g}, {xmax:g}], "
            f"feature at scan edge={at_edge}, fit success={stats.fit_success}"
        )
        if attempt == max_retries:
            raise RuntimeError(
                f"Alignment of {motor.name} failed after {attempt + 1} scans: {reason}"
            )

        # Use the original scan endpoints (ps may drop a point for derivatives).
        edge = low if feature <= (xmin + xmax) / 2 else high
        if any(np.isclose(edge, old, rtol=0, atol=rang * 1e-6) for old in visited):
            raise RuntimeError(
                f"Alignment of {motor.name} would repeat an already scanned center "
                f"at {edge:g}: {reason}"
            )
        _check_positions(motor, edge, edge - rang, edge + rang)
        print(
            f"Alignment of {motor.name}: rejecting fit ({reason}). "
            f"Recentering at scan edge {edge:g}; retry {attempt + 1}/{max_retries}."
        )
        yield from bps.mv(motor, edge)
