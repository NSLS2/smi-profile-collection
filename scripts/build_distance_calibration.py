import os
import numpy as np
from smibase.base import mdsave

CAL_DIR = "/nsls2/data/smi/shared/config/bluesky/profile_collection/startup/agb_z_calibration_results"
PIXEL_SIZE_MM = 0.172

# Recorded beamstop motor positions during the calibration scan.
# Fill these in from your logbook / scan metadata.
ROD_MOTOR_X = 6.80
ROD_MOTOR_Y = 0.0
PIN_MOTOR_X = -227.0
PIN_MOTOR_Y = 6.8


def _load(name):
    return np.load(os.path.join(CAL_DIR, name))


def build_calibration(z_bin_mm=2.0, write=False, verbose=True):
    motor_x = _load("motor_x.npy")
    motor_y = _load("motor_y.npy")
    motor_z = _load("motor_z.npy")
    bc_col  = _load("bc_col.npy")           # rod-in dataset
    bc_row  = _load("bc_row.npy")
    sdd_mm  = _load("sdd_mm.npy")

    # Optional pin dataset (only used if shapes match motor_z)
    try:
        bc_col_pin = _load("bc_col_pin.npy")
        bc_row_pin = _load("bc_row_pin.npy")
        pin_sh_col = _load("pin_shadow_col.npy")
        pin_sh_row = _load("pin_shadow_row.npy")
        have_pin = True
    except FileNotFoundError:
        have_pin = False

    # Per-frame derived offsets
    beam_off_x = -motor_x + bc_col * PIXEL_SIZE_MM
    beam_off_y = -motor_y + bc_row * PIXEL_SIZE_MM
    samp_off_z = sdd_mm - motor_z

    if have_pin:
        pd_off_x = PIN_MOTOR_X + (bc_col_pin - pin_sh_col) * PIXEL_SIZE_MM
        pd_off_y = PIN_MOTOR_Y + (bc_row_pin - pin_sh_row) * PIXEL_SIZE_MM
    else:
        pd_off_x = np.full_like(beam_off_x, PIN_MOTOR_X)
        pd_off_y = np.full_like(beam_off_y, PIN_MOTOR_Y)

    # Bin by z to suppress per-frame noise
    z_min, z_max = motor_z.min(), motor_z.max()
    edges = np.arange(z_min, z_max + z_bin_mm, z_bin_mm)
    cal = {}
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (motor_z >= lo) & (motor_z < hi)
        if m.sum() < 1:
            continue
        z_center = float(np.mean(motor_z[m]))
        entry = {
            "beam_offset_x":   float(np.median(beam_off_x[m])),
            "beam_offset_y":   float(np.median(beam_off_y[m])),
            "rod_offset_x":    float(ROD_MOTOR_X),
            "rod_offset_y":    float(ROD_MOTOR_Y),
            "pd_offset_x":     float(np.median(pd_off_x[m])),
            "pd_offset_y":     float(np.median(pd_off_y[m])),
            "sample_offset_z": float(np.median(samp_off_z[m])),
        }
        cal[f"{z_center:.6f}"] = entry
        if verbose:
            print(f"z={z_center:8.3f}  n={m.sum():3d}  "
                  f"bx={entry['beam_offset_x']:.3f} by={entry['beam_offset_y']:.3f} "
                  f"sz={entry['sample_offset_z']:.3f}")

    if write:
        mdsave["distance_calibration"] = cal
        print(f"Wrote {len(cal)} calibration points to mdsave['distance_calibration'].")
    return cal


if __name__ == "__main__":
    build_calibration(write=False)