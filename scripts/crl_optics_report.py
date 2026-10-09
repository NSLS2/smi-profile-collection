"""Document the current understanding of the installed SMI CRLs and focus settings.

Run from the repository root:
    PYTHONPATH=src python scripts/crl_optics_report.py --output docs/crl_report
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

from smi_beamline.devices.crl_optics import (
    COMBINATIONS, DEFAULT_HOLDERS, MEASURED_SAMPLE_DISTANCE_AT_Z0_MM,
    DEFAULT_INCIDENT_CURVATURE_PER_M, CRLGeometry, CRLModel,
)


def text_page(pdf, title, lines):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.08, 0.95, title, fontsize=17, weight="bold", va="top")
    fig.text(0.08, 0.89, "\n".join(lines), fontsize=10, family="monospace",
             va="top", linespacing=1.55)
    pdf.savefig(fig)
    plt.close(fig)


def ray_diagram(pdf, model, output):
    """Paraxial ray transfer at the travel limits and center; arbitrary ray heights."""
    g = model.geometry
    c0 = g.incident_curvature_per_m
    d = g.sample_distance_mm / 1000
    fig, axes = plt.subplots(3, 1, figsize=(8.27, 11.69))
    fig.subplots_adjust(left=0.09, right=0.96, top=0.82, bottom=0.27, hspace=0.75)
    fig.text(0.08, 0.95, "SSA to CRL to sample", fontsize=18, weight="bold")
    fig.text(0.08, 0.89,
             "Rays at the travel limits and center, focused onto the fixed sample.\n"
             "Each panel uses the required lens power at that position; the holder-3\n"
             "energy is an equivalent example, not the same energy in all three panels.",
             fontsize=10, linespacing=1.5)
    source = -1 / c0 if c0 > 0 else None
    left = source if source is not None else g.z_min_mm / 1000 - 2
    for ax, z_mm, color in zip(axes, (g.z_min_mm, 0, g.z_max_mm),
                                ("tab:blue", "tab:green", "tab:orange")):
        z = z_mm / 1000
        power = g.required_power_per_m(z_mm)
        curvature = c0 / (1 + c0 * z)
        f = 1 / power
        energy = 10 * np.sqrt(model.power_per_m(10, [3]) / power)
        for height in (-1, -0.5, 0.5, 1):
            slope_in = curvature * height
            height_left = height + slope_in * (left - z)
            # Thin lens changes slope by -height/f; propagate to the sample.
            height_sample = height + (slope_in - power * height) * (d - z)
            ax.plot([left, z, d], [height_left, height, height_sample], color=color, lw=1.2)
        ax.axhline(0, color="0.6", lw=0.6)
        ax.axvline(z, ymin=0.15, ymax=0.85, color=color, lw=3)
        ax.axvline(d, color="0.2", lw=1, ls="--")
        ax.axvline(0, color="0.6", lw=0.7, ls=":")
        ax.text(left, -1.4, "SSA" if source is not None else "Incident beam", fontsize=9)
        ax.text(z, 1.23, f"CRL Z={z_mm:+g} mm", ha="center", fontsize=9)
        ax.text(d, -1.4, "Sample", ha="right", fontsize=9)
        p_label = f"p={z-source:.3f} m; " if source is not None else ""
        ax.set_title(f"{p_label}q={d-z:.3f} m; required f={f*1000:.1f} mm\n"
                     f"Holder 3 example: {energy:.3f} keV", fontsize=10, loc="left", pad=12)
        ax.set(xlim=(left-0.3, d+0.4), ylim=(-1.6, 1.65), yticks=[],
               xticks=[left, 0, d], xlabel="Longitudinal position from CRL Z=0 (m)")
        ax.spines[["top", "right", "left"]].set_visible(False)
    fig.text(0.08, 0.10,
             "Positive CRL Z increases source-to-lens distance p and decreases q.\n"
             "Focusing condition: 1/f = 1/p + 1/q; SSA and sample stay fixed.\n"
             "Longitudinal scale is physical; transverse ray heights are arbitrary.\n"
             "Rays illustrate focusing geometry, not predicted beam size or aperture.",
             fontsize=10, linespacing=1.6)
    pdf.savefig(fig)
    fig.savefig(output / "ray_geometry.png", dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("docs/crl_report"))
    parser.add_argument("--sample-distance-mm", type=float,
                        default=MEASURED_SAMPLE_DISTANCE_AT_Z0_MM)
    parser.add_argument("--z-min-mm", type=float, default=-300)
    parser.add_argument("--z-max-mm", type=float, default=300)
    parser.add_argument("--incident-curvature-per-m", type=float,
                        default=DEFAULT_INCIDENT_CURVATURE_PER_M,
                        help="Curvature at CRL Z=0; default is 1/10.5 per m from SSA; 0 is collimated")
    args = parser.parse_args()
    geometry = CRLGeometry(args.sample_distance_mm, args.z_min_mm, args.z_max_mm,
                           args.incident_curvature_per_m)
    model = CRLModel(geometry)
    bands = model.selection_bands()
    args.output.mkdir(parents=True, exist_ok=True)
    energies = np.linspace(2.1, 24, 2191)  # 10 eV lookup spacing
    selected = [next(iter(model.candidates(e)), None) for e in energies]
    with (args.output / "lookup.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["energy_keV", "reachable", "holders", "elements",
                         "focal_length_mm", "image_distance_mm", "z_mm", "z_margin_mm"])
        for e, s in zip(energies, selected):
            writer.writerow([f"{e:.3f}", s is not None,
                             " ".join(map(str, s.holders)) if s else "",
                             s.element_count if s else "",
                             *([f"{value:.6f}" for value in (
                                 s.focal_length_mm, s.image_distance_mm, s.z_mm,
                                 s.z_margin_mm)] if s else [""] * 4)])
    with (args.output / "selection_bands.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["energy_min_keV", "energy_max_keV", "holders"])
        for band in bands:
            writer.writerow([f"{band.energy_min_keV:.9f}", f"{band.energy_max_keV:.9f}",
                             " ".join(map(str, band.holders)) if band.holders else "unreachable"])

    with PdfPages(args.output / "crl_optics_report.pdf") as pdf:
        text_page(pdf, "SMI CRLs: the installed beamline", [
            "CURRENT BEST UNDERSTANDING",
            "Reconstructing the operating beamline - September 2026",
            "Original installed-system documentation is no longer available.",
            "This records our current best understanding and calculated settings.",
            "",
            "LAYOUT",
            f"Lens plane to sample at Z=0: {geometry.sample_distance_mm:g} mm",
            f"Z travel: {geometry.z_min_mm:g} to {geometry.z_max_mm:g} mm; positive downstream",
            (f"SSA secondary source: {1/geometry.incident_curvature_per_m:g} m upstream of CRL Z=0."
             if geometry.incident_curvature_per_m > 0 else
             f"Incident curvature at Z=0: {geometry.incident_curvature_per_m:g} /m"),
            "",
            "KNOWN INVENTORY (sizes are quoted radii)",
            "Holder  Contents                              IN mm   OUT mm",
            "------  ------------------------------------  -----   ------",
            *[f"{h.number:>6}  {h.description:<36}  {h.in_mm:>5.1f}   {h.out_mm:>6.1f}"
              for h in DEFAULT_HOLDERS],
            "",
            "Blank holders 6-8 may contain diamond CRLs; contents unconfirmed.",
            "Locate and measure the 12 reported diamonds during commissioning.",
            "Blanks and aperture 12 are excluded from automatic lens selection.",
            "IN=0 mm is nominal, pending alignment within about +/-2 mm.",
            "",
            "CALCULATION BASIS",
            "Two-sided parabolic lenses assumed; all labeled lenses are Be.",
            "Be density 1.848 g/cm^3; free-electron delta scales as energy^-2.",
            "Common-plane thin lenses image the SSA onto the sample.",
            "Predicts geometrical focus, not spot size or transmission.",
            "",
            "FOLLOW-UP",
            "Test a few energies/combinations; confirm and measure blank contents",
            "(diamond?); develop advanced alignment routines.",
        ])
        ray_diagram(pdf, model, args.output)

        fig, (ax, count_ax) = plt.subplots(2, 1, figsize=(11, 8), sharex=True,
                                          layout="constrained", height_ratios=(3, 1))
        for combo in COMBINATIONS:
            interval = model.combination_energy_range(combo)
            if interval:
                es = np.linspace(*interval, 80)
                zs = [geometry.focus_positions_mm(
                    model.power_per_m(e, combo.holders)) for e in es]
                ax.plot(es, [z[0] if z else np.nan for z in zs], color="0.8",
                        alpha=0.35, linewidth=0.6)
        for index, band in enumerate(bands):
            if band.holders is None:
                for axis in (ax, count_ax):
                    axis.axvspan(band.energy_min_keV, band.energy_max_keV,
                                color="tab:red", alpha=0.22)
                continue
            es = np.linspace(band.energy_min_keV, band.energy_max_keV, 80)
            zs = [geometry.focus_positions_mm(1000 / model.focal_length_mm(e, band.holders))
                  for e in es]
            color = plt.get_cmap("tab20")(index % 20)
            ax.plot(es, [z[0] if z else np.nan for z in zs], color=color, linewidth=2.5)
            mid = len(es) // 2
            label = "+".join(map(str, band.holders))
            if es[mid] > 17.6:
                ax.annotate(label, (es[mid], zs[mid][0]),
                            xytext=(es[mid], 95 + 55 * (index % 2)),
                            fontsize=8, rotation=90, ha="center", va="bottom",
                            arrowprops={"arrowstyle": "-", "color": "0.5", "lw": 0.6})
            else:
                ax.annotate(label, (es[mid], zs[mid][0]), fontsize=7,
                            xytext=(0, 5), textcoords="offset points")
            count_ax.plot([es[0], es[-1]], [len(band.holders)] * 2, color=color, linewidth=3)
        ax.set(ylabel="Recommended CRL Z (mm)",
               title="Fewest-holder selection; labels are holder numbers; gray = alternatives\n"
                     "Minimum holder count takes priority, including at travel limits",
               ylim=(geometry.z_min_mm - 15, geometry.z_max_mm + 15))
        max_holders = max(len(s.holders) for s in selected if s)
        count_ax.set(xlabel="Energy (keV)", ylabel="Holders IN", xlim=(2.1, 24),
                     yticks=range(1, max_holders + 1))
        for axis in (ax, count_ax):
            axis.grid(alpha=0.2)
        pdf.savefig(fig)
        fig.savefig(args.output / "selection.png", dpi=160)
        plt.close(fig)

        rows = []
        for band in bands:
            if band.holders:
                combo = next(c for c in COMBINATIONS if c.holders == band.holders)
                z_values = [geometry.focus_positions_mm(
                    1000 / model.focal_length_mm(e, band.holders))[0]
                    for e in (band.energy_min_keV, band.energy_max_keV)]
                rows.append(f"{band.energy_min_keV:7.3f}-{band.energy_max_keV:7.3f}  "
                            f"{'+'.join(map(str, band.holders)):<17} {combo.element_count:>3}  "
                            f"{z_values[0]:7.1f} -> {z_values[1]:7.1f}")
            else:
                rows.append(f"{band.energy_min_keV:7.3f}-{band.energy_max_keV:7.3f}  UNREACHABLE")
        for offset in range(0, len(rows), 35):
            text_page(pdf, "Recommended energy bands", [
                "Energy (keV)      Holders IN        N     Z start -> Z end (mm)",
                *rows[offset:offset + 35], "",
                "Endpoints rounded; use selection_bands.csv for precision.",
                "At shared endpoints both adjacent choices can be reachable.",
                "Use recommend() at the exact energy, not interpolation across",
                "a holder change. N is the total number of individual lenses.",
                "All 255 known combinations evaluated; fewest holders first,",
                "then fewest elements, then holder IDs. Travel limits included.",
            ])

    print(f"Report: {args.output / 'crl_optics_report.pdf'}")
    for band in bands:
        print(f"{band.energy_min_keV:.6f}-{band.energy_max_keV:.6f} keV: "
              f"{band.holders or 'unreachable'}")


if __name__ == "__main__":
    main()
