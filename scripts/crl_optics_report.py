"""Generate the offline CRL feasibility PDF, plots, and machine-readable tables.

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
    COMBINATIONS, DEFAULT_HOLDERS, CRLGeometry, CRLModel,
)


def text_page(pdf, title, lines):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.08, 0.95, title, fontsize=17, weight="bold", va="top")
    fig.text(0.08, 0.89, "\n".join(lines), fontsize=10, family="monospace",
             va="top", linespacing=1.55)
    pdf.savefig(fig)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("docs/crl_report"))
    parser.add_argument("--sample-distance-mm", type=float, default=615)
    parser.add_argument("--z-min-mm", type=float, default=-50)
    parser.add_argument("--z-max-mm", type=float, default=250)
    parser.add_argument("--incident-curvature-per-m", type=float, default=0)
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
        gaps = [b for b in bands if b.holders is None]
        text_page(pdf, "SMI CRL microfocusing: initial feasibility", [
            "PROVISIONAL OPTICS MODEL - September 2026",
            "",
            f"Lens plane to sample at Z=0: {geometry.sample_distance_mm:g} mm",
            f"Z travel: {geometry.z_min_mm:g} to {geometry.z_max_mm:g} mm; positive downstream",
            f"Accessible image distance: {geometry.sample_distance_mm - geometry.z_max_mm:g}"
            f" to {geometry.sample_distance_mm - geometry.z_min_mm:g} mm",
            f"Incident curvature at Z=0: {geometry.incident_curvature_per_m:g} /m",
            "Eight populated holders; 255 nonempty combinations evaluated.",
            "Priority: fewest holders, then elements, then holder numbers.",
            "",
            "Predicted gaps within 2.1-24 keV (analytic boundaries):",
            *([f"  {b.energy_min_keV:.4f} - {b.energy_max_keV:.4f} keV" for b in gaps]
              or ["  None in this model."]),
            "",
            "ASSUMPTIONS",
            "Diamond, density 3.515 g/cm^3; two parabolic surfaces per lens.",
            "Quoted radii apply to each surface. All holders share one plane.",
            "Free-electron delta (carbon f1=6); delta scales as energy^-2.",
            f"At 10 keV: delta = {model.delta(10):.7g}.",
            "Focal length: f = 1 / [2 delta sum(N/R)].",
            "Ray curvature C: 1/q = 1/f - C(Z); q = (615-Z) mm by default.",
            "C(Z) = C(0) / [1 + C(0) Z(m)]. Positive C means divergence.",
            "",
            "INTERPRETATION",
            "Coverage means a geometrical focus exists within nominal travel.",
            "It does not establish spot size, transmission, or beam quality.",
            "Material, radius convention, holder spacing and Z zero need",
            "confirmation. No tabulated dispersion correction is included.",
            "Transmission needs lens aperture and web thickness; spot size",
            "also needs incident size/emittance and wavefront information.",
            "Fewest holders can favor a thick stack over fewer lens elements.",
            "",
            "Switches may require large Z jumps. Boundary solutions have",
            "zero travel margin; usable coverage will shrink with a margin.",
            "A 1% focal-length error shifts Z by roughly 3.7-6.7 mm here.",
            "Model and report generation issue no hardware commands.",
        ])
        text_page(pdf, "Holder inventory and nominal positions", [
            "Holder  Contents                              IN mm   OUT mm",
            "------  ------------------------------------  -----   ------",
            *[f"{h.number:>6}  {h.description:<36}  {h.in_mm:>5.1f}   {h.out_mm:>6.1f}"
              for h in DEFAULT_HOLDERS],
            "",
            "Empty holders 6-8 and aperture holder 12 have no lens power.",
            "They are excluded from automatic lens selection.",
            "IN=0 mm is nominal, pending alignment within about +/-2 mm.",
            "",
            "NEXT CALIBRATIONS / DECISIONS",
            "1. Confirm material, per-surface radii, and holder axial spacing.",
            "2. Measure at least one energy + holders + best-focus Z point.",
            "3. Confirm actual motor travel and choose working end margins.",
            "4. Choose alignment signal: transmission or measured spot size.",
            "5. Decide aperture-12 behavior and persistence of IN positions.",
            "6. Check horizontal/vertical curvature separately if astigmatic.",
            "",
            "The existing lens1...lens12, x/y/z/ph/th remain motor components.",
            "Initial CRL helpers expose inventory and offline calculations.",
        ])

        fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
        for holder in DEFAULT_HOLDERS:
            if holder.count:
                ax.plot(energies, [model.focal_length_mm(e, [holder.number]) for e in energies],
                        label=f"H{holder.number}: {holder.count} x R{holder.radius_um:g} um")
        ax.axhspan(geometry.sample_distance_mm - geometry.z_max_mm,
                   geometry.sample_distance_mm - geometry.z_min_mm,
                   color="gray", alpha=0.2, label="Sample distance range (q)")
        ax.set(yscale="log", xlabel="Energy (keV)", ylabel="Effective focal length (mm)",
               title="Individual holder focal lengths (q = f only for collimated input)",
               xlim=(2.1, 24), ylim=(10, 1e5))
        ax.legend(ncols=2, fontsize=8)
        ax.grid(alpha=0.25, which="both")
        pdf.savefig(fig)
        fig.savefig(args.output / "focal_lengths.png", dpi=160)
        plt.close(fig)

        fig, (ax, count_ax) = plt.subplots(2, 1, figsize=(11, 8), sharex=True,
                                          layout="constrained", height_ratios=(3, 1))
        for combo in COMBINATIONS:
            interval = model.combination_energy_range(combo)
            if interval:
                es = np.linspace(*interval, 80)
                zs = [geometry.focus_positions_mm(
                    2 * model.delta(e) * combo.strength_per_m) for e in es]
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
               title="Fewest-holder selection; labels are holder numbers; gray = alternatives",
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
            ])

        fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
        reference = np.array([s.z_mm if s else np.nan for s in selected])
        for curvature in (-0.1, 0.1):
            varied = CRLModel(CRLGeometry(geometry.sample_distance_mm, geometry.z_min_mm,
                                         geometry.z_max_mm, curvature))
            differences = []
            for e, s in zip(energies, selected):
                positions = varied.geometry.focus_positions_mm(
                    1000 / model.focal_length_mm(e, s.holders)) if s else ()
                differences.append(positions[0] if positions else np.nan)
            difference = np.array(differences) - reference
            for i in range(1, len(selected)):
                if selected[i] and selected[i - 1] and selected[i].holders != selected[i - 1].holders:
                    difference[i] = np.nan
            ax.plot(energies, difference,
                    label=f"C(0)={curvature:+g} /m (signed radius {1/curvature:+g} m)")
        ax.set(xlabel="Energy (keV)", ylabel="Z change from baseline (mm)", xlim=(2.1, 24),
               title="Sensitivity to incident curvature, holding baseline lens choice fixed")
        ax.text(0.03, 0.45, "Breaks: outside travel or a baseline holder change.\n"
                "Different X/Y curvatures generally give different focus positions.",
                transform=ax.transAxes, fontsize=9)
        ax.legend()
        ax.grid(alpha=0.25)
        pdf.savefig(fig)
        fig.savefig(args.output / "curvature_sensitivity.png", dpi=160)
        plt.close(fig)
    print(f"Report: {args.output / 'crl_optics_report.pdf'}")
    for band in bands:
        print(f"{band.energy_min_keV:.6f}-{band.energy_max_keV:.6f} keV: "
              f"{band.holders or 'unreachable'}")


if __name__ == "__main__":
    main()
