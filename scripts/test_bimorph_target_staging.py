"""Non-applying test helpers for CAENels bimorph target staging.

Run this in the live SMI IPython session with::

    %run scripts/test_bimorph_target_staging.py

Then call ``test_bimorph_target_staging(...)`` with ``hfm_voltage`` or
``vfm_voltage``.  These helpers write only ``SET-VTRGT<n>`` target PVs and
poll ``GET-VTRGT<n>``.  They never write ``SET-ALLTRGT`` and never call the
profile's apply/load helpers.
"""

import time
import contextlib
import os

from smi_beamline.devices.bimorph import _quiet_ca_messages


@contextlib.contextmanager
def _suppress_stderr_fd():
    """Suppress C-level stderr noise from this controller's put callback."""
    saved = os.dup(2)
    devnull = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull, 2)
        yield
    finally:
        os.dup2(saved, 2)
        os.close(saved)
        os.close(devnull)


def _read_target_rb(dev, channel):
    return float(getattr(dev, f"ch{channel}_trg_rb").get())


def _write_target(dev, channel, value):
    with _quiet_ca_messages(), _suppress_stderr_fd():
        getattr(dev, f"ch{channel}_trg").put(float(value), use_complete=False)


def _write_targets(dev, target_by_channel):
    with _quiet_ca_messages(), _suppress_stderr_fd():
        for channel, value in target_by_channel.items():
            getattr(dev, f"ch{int(channel)}_trg").put(float(value), use_complete=False)


def _wait_for_targets_rb(dev, target_by_channel, *, timeout, poll, tolerance, stable_reads):
    deadline = time.monotonic() + float(timeout)
    stable = {int(channel): 0 for channel in target_by_channel}
    reads = {int(channel): [] for channel in target_by_channel}
    while True:
        matched_now = True
        for channel, target in target_by_channel.items():
            channel = int(channel)
            rb = _read_target_rb(dev, channel)
            matched = abs(rb - float(target)) <= float(tolerance)
            reads[channel].append(rb)
            if matched:
                stable[channel] += 1
            else:
                stable[channel] = 0
            if stable[channel] < int(stable_reads):
                matched_now = False
        if matched_now:
            return True, reads
        if time.monotonic() >= deadline:
            return False, reads
        time.sleep(float(poll))


def _wait_for_target_rb(dev, channel, target, *, timeout, poll, tolerance, stable_reads):
    deadline = time.monotonic() + float(timeout)
    stable = 0
    reads = []
    while True:
        rb = _read_target_rb(dev, channel)
        matched = abs(rb - target) <= float(tolerance)
        reads.append(rb)
        if matched:
            stable += 1
            if stable >= int(stable_reads):
                return rb, True, reads
        else:
            stable = 0
        if time.monotonic() >= deadline:
            return rb, False, reads
        time.sleep(float(poll))


def test_bimorph_target_staging(
    dev,
    channel=0,
    target=None,
    *,
    attempts=3,
    delay=2.0,
    poll=0.5,
    tolerance=0.5,
    stable_reads=2,
    restore_initial=True,
):
    """Write one SET-VTRGT channel repeatedly and poll GET-VTRGT.

    Parameters
    ----------
    dev
        ``hfm_voltage`` or ``vfm_voltage``.
    channel : int
        Bimorph channel number, 0 through 15.
    target : float, optional
        Target voltage to stage.  Defaults to the current live output for the
        same channel, which is the safest non-moving value to stage.
    attempts : int
        Number of times to write ``SET-VTRGT<n>`` if the readback has not
        reached the target yet.
    delay : float
        Maximum seconds to wait after each write for ``GET-VTRGT<n>`` to match.
    poll : float
        Seconds between ``GET-VTRGT<n>`` polls during the wait window.
    tolerance : float
        Absolute voltage tolerance used to decide whether the readback matched.
    stable_reads : int
        Number of consecutive matching ``GET-VTRGT<n>`` reads required before
        declaring success.  This catches delayed/stale controller readbacks.
    restore_initial : bool
        If true, write the initial ``GET-VTRGT`` value back at the end when the
        requested target differs from the initial target readback.  This is only
        another target-stage write; it still does not apply/move.

    Returns
    -------
    list[dict]
        One row per write/read attempt.
    """
    channel = int(channel)
    if channel < 0 or channel > 15:
        raise ValueError("channel must be 0 through 15")
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    output = float(getattr(dev, f"ch{channel}").get())
    initial_rb = _read_target_rb(dev, channel)
    target = output if target is None else float(target)

    print(
        f"{dev.name} ch{channel}: live output={output:.3f}, "
        f"initial GET-VTRGT={initial_rb:.3f}, target={target:.3f}"
    )
    print("Writing SET-VTRGT only. Not writing SET-ALLTRGT/apply.")

    rows = []
    for attempt in range(1, int(attempts) + 1):
        before = _read_target_rb(dev, channel)
        _write_target(dev, channel, target)
        after, matched, reads = _wait_for_target_rb(
            dev,
            channel,
            target,
            timeout=delay,
            poll=poll,
            tolerance=tolerance,
            stable_reads=stable_reads,
        )
        output_after = float(getattr(dev, f"ch{channel}").get())
        row = {
            "attempt": attempt,
            "before": before,
            "target": target,
            "after": after,
            "output_after": output_after,
            "reads": reads,
            "matched": matched,
        }
        rows.append(row)
        print(
            f"attempt {attempt}: before={before:.3f}, "
            f"after={after:.3f}, output={output_after:.3f}, "
            f"matched={matched}, reads={reads}"
        )
        if matched:
            break

    if restore_initial and abs(target - initial_rb) > float(tolerance):
        print(f"Restoring initial staged target {initial_rb:.3f} via SET-VTRGT only.")
        _write_target(dev, channel, initial_rb)
        restored, _, _ = _wait_for_target_rb(
            dev,
            channel,
            initial_rb,
            timeout=delay,
            poll=poll,
            tolerance=tolerance,
            stable_reads=stable_reads,
        )
        print(f"post-restore GET-VTRGT={restored:.3f}")

    return rows


def test_bimorph_sync_to_output(
    dev,
    channels=None,
    *,
    attempts=3,
    delay=2.0,
    poll=0.5,
    tolerance=0.5,
    stable_reads=2,
):
    """Stage each selected channel to its live output and poll target readback.

    This is a convenience wrapper around ``test_bimorph_target_staging`` with
    ``restore_initial=False`` because the intent is to leave staged targets
    equal to live outputs.
    """
    if channels is None:
        channels = range(16)
    all_rows = {}
    for channel in channels:
        target = float(getattr(dev, f"ch{int(channel)}").get())
        all_rows[int(channel)] = test_bimorph_target_staging(
            dev,
            channel=int(channel),
            target=target,
            attempts=attempts,
            delay=delay,
            poll=poll,
            tolerance=tolerance,
            stable_reads=stable_reads,
            restore_initial=False,
        )
    return all_rows


def test_bimorph_offset_all_targets(
    dev,
    offset=1.0,
    channels=None,
    *,
    attempts=5,
    delay=5.0,
    poll=0.5,
    tolerance=0.5,
    stable_reads=3,
    restore_initial=True,
):
    """Stage all selected target readbacks by ``offset`` volts, then restore.

    This writes only per-channel ``SET-VTRGT<n>`` values and polls
    ``GET-VTRGT<n>``.  It does not write ``SET-ALLTRGT``.  By default it
    restores the initial staged targets at the end, so this is a reversible
    communication test rather than a lasting target change.
    """
    if channels is None:
        channels = range(16)
    channels = [int(channel) for channel in channels]
    offset = float(offset)

    initial_targets = {channel: _read_target_rb(dev, channel) for channel in channels}
    initial_outputs = {
        channel: float(getattr(dev, f"ch{channel}").get()) for channel in channels
    }

    print(
        f"{dev.name}: staging {len(channels)} channels by offset {offset:+.3f} V. "
        "Writing SET-VTRGT only; not writing SET-ALLTRGT/apply."
    )
    rows = {}
    for channel in channels:
        target = initial_targets[channel] + offset
        channel_rows = []
        for attempt in range(1, int(attempts) + 1):
            before = _read_target_rb(dev, channel)
            _write_target(dev, channel, target)
            after, matched, reads = _wait_for_target_rb(
                dev,
                channel,
                target,
                timeout=delay,
                poll=poll,
                tolerance=tolerance,
                stable_reads=stable_reads,
            )
            output_after = float(getattr(dev, f"ch{channel}").get())
            output_changed = abs(output_after - initial_outputs[channel]) > float(tolerance)
            row = {
                "attempt": attempt,
                "before": before,
                "target": target,
                "after": after,
                "output_initial": initial_outputs[channel],
                "output_after": output_after,
                "output_changed": output_changed,
                "reads": reads,
                "matched": matched,
            }
            channel_rows.append(row)
            print(
                f"ch{channel}: attempt {attempt}: before={before:.3f}, "
                f"after={after:.3f}, output={output_after:.3f}, "
                f"matched={matched}, output_changed={output_changed}"
            )
            if matched:
                break
        rows[channel] = channel_rows

    if restore_initial:
        print("Restoring initial staged targets via SET-VTRGT only.")
        restore_rows = {}
        for channel in channels:
            target = initial_targets[channel]
            _write_target(dev, channel, target)
            after, matched, reads = _wait_for_target_rb(
                dev,
                channel,
                target,
                timeout=delay,
                poll=poll,
                tolerance=tolerance,
                stable_reads=stable_reads,
            )
            output_after = float(getattr(dev, f"ch{channel}").get())
            output_changed = abs(output_after - initial_outputs[channel]) > float(tolerance)
            restore_rows[channel] = {
                "target": target,
                "after": after,
                "output_initial": initial_outputs[channel],
                "output_after": output_after,
                "output_changed": output_changed,
                "reads": reads,
                "matched": matched,
            }
            print(
                f"restore ch{channel}: after={after:.3f}, output={output_after:.3f}, "
                f"matched={matched}, output_changed={output_changed}"
            )
        return {"stage": rows, "restore": restore_rows}

    return {"stage": rows}


def test_bimorph_batch_offset_targets(
    dev,
    offset=1.0,
    channels=None,
    *,
    attempts=3,
    timeout=10.0,
    poll=0.5,
    tolerance=0.5,
    stable_reads=3,
    restore_initial=True,
):
    """Batch-write all selected targets, then poll all target readbacks together.

    This tests whether the controller accepts many ``SET-VTRGT<n>`` writes up
    front and updates the corresponding ``GET-VTRGT<n>`` readbacks in parallel.
    It never writes ``SET-ALLTRGT``.  By default it restores the initial staged
    targets with the same batch-write/poll pattern.

    Commissioning note: early live tests indicate this controller may serialize
    target updates internally and ignore/latch later writes while an earlier
    channel is still settling.  Do not use this path for snapshot restore unless
    that behavior is disproven.  Prefer ``stage_bimorph_targets_sequential``.
    """
    if channels is None:
        channels = range(16)
    channels = [int(channel) for channel in channels]
    offset = float(offset)

    initial_targets = {channel: _read_target_rb(dev, channel) for channel in channels}
    initial_outputs = {
        channel: float(getattr(dev, f"ch{channel}").get()) for channel in channels
    }
    stage_targets = {
        channel: initial_targets[channel] + offset for channel in channels
    }

    print(
        f"{dev.name}: batch-staging {len(channels)} channels by offset {offset:+.3f} V. "
        "Writing SET-VTRGT only; not writing SET-ALLTRGT/apply."
    )
    stage_rows = []
    for attempt in range(1, int(attempts) + 1):
        t0 = time.monotonic()
        _write_targets(dev, stage_targets)
        matched, reads = _wait_for_targets_rb(
            dev,
            stage_targets,
            timeout=timeout,
            poll=poll,
            tolerance=tolerance,
            stable_reads=stable_reads,
        )
        elapsed = time.monotonic() - t0
        outputs_after = {
            channel: float(getattr(dev, f"ch{channel}").get()) for channel in channels
        }
        output_changed = {
            channel: abs(outputs_after[channel] - initial_outputs[channel]) > float(tolerance)
            for channel in channels
        }
        stage_rows.append({
            "attempt": attempt,
            "targets": dict(stage_targets),
            "matched": matched,
            "elapsed": elapsed,
            "reads": reads,
            "outputs_after": outputs_after,
            "output_changed": output_changed,
        })
        print(
            f"batch attempt {attempt}: matched={matched}, elapsed={elapsed:.2f}s, "
            f"any_output_changed={any(output_changed.values())}"
        )
        if matched:
            break

    result = {"stage": stage_rows}
    if restore_initial:
        print("Restoring initial staged targets with one batch SET-VTRGT pass.")
        t0 = time.monotonic()
        _write_targets(dev, initial_targets)
        matched, reads = _wait_for_targets_rb(
            dev,
            initial_targets,
            timeout=timeout,
            poll=poll,
            tolerance=tolerance,
            stable_reads=stable_reads,
        )
        elapsed = time.monotonic() - t0
        outputs_after = {
            channel: float(getattr(dev, f"ch{channel}").get()) for channel in channels
        }
        output_changed = {
            channel: abs(outputs_after[channel] - initial_outputs[channel]) > float(tolerance)
            for channel in channels
        }
        result["restore"] = {
            "targets": dict(initial_targets),
            "matched": matched,
            "elapsed": elapsed,
            "reads": reads,
            "outputs_after": outputs_after,
            "output_changed": output_changed,
        }
        print(
            f"batch restore: matched={matched}, elapsed={elapsed:.2f}s, "
            f"any_output_changed={any(output_changed.values())}"
        )

    return result


def stage_bimorph_targets_sequential(
    dev,
    targets,
    channels=None,
    *,
    attempts=5,
    delay=5.0,
    poll=0.5,
    tolerance=0.5,
    stable_reads=3,
):
    """Stage target voltages one channel at a time and wait after each channel.

    ``targets`` may be a 16-element list/tuple indexed by channel, or a mapping
    ``{channel: target}``.  This is the restore-safe staging pattern supported
    by today's live tests: write one ``SET-VTRGT<n>``, poll that channel's
    ``GET-VTRGT<n>`` until stable, then move to the next channel.  It never
    writes ``SET-ALLTRGT``.
    """
    if isinstance(targets, dict):
        target_by_channel = {int(k): float(v) for k, v in targets.items()}
    else:
        target_by_channel = {i: float(v) for i, v in enumerate(targets)}

    if channels is None:
        channels = sorted(target_by_channel)
    channels = [int(channel) for channel in channels]

    initial_outputs = {
        channel: float(getattr(dev, f"ch{channel}").get()) for channel in channels
    }
    print(
        f"{dev.name}: sequentially staging {len(channels)} channels. "
        "Writing SET-VTRGT only; not writing SET-ALLTRGT/apply."
    )

    rows = {}
    for channel in channels:
        if channel not in target_by_channel:
            raise KeyError(f"no target provided for channel {channel}")
        target = target_by_channel[channel]
        channel_rows = []
        for attempt in range(1, int(attempts) + 1):
            before = _read_target_rb(dev, channel)
            _write_target(dev, channel, target)
            after, matched, reads = _wait_for_target_rb(
                dev,
                channel,
                target,
                timeout=delay,
                poll=poll,
                tolerance=tolerance,
                stable_reads=stable_reads,
            )
            output_after = float(getattr(dev, f"ch{channel}").get())
            output_changed = abs(output_after - initial_outputs[channel]) > float(tolerance)
            row = {
                "attempt": attempt,
                "before": before,
                "target": target,
                "after": after,
                "output_initial": initial_outputs[channel],
                "output_after": output_after,
                "output_changed": output_changed,
                "reads": reads,
                "matched": matched,
            }
            channel_rows.append(row)
            print(
                f"ch{channel}: attempt {attempt}: before={before:.3f}, "
                f"target={target:.3f}, after={after:.3f}, output={output_after:.3f}, "
                f"matched={matched}, output_changed={output_changed}"
            )
            if matched:
                break
        rows[channel] = channel_rows
    return rows
