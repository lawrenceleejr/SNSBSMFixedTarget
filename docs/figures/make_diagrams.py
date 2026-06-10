#!/usr/bin/env python3
"""Generate technical diagrams for the SNS BSM fixed-target design note:
facility_layout.png (beam delivery) and near_detector.png (experiment side view)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Circle, FancyArrow, FancyArrowPatch,
                                Polygon, Wedge)
from pathlib import Path

HERE = Path(__file__).parent


def facility_layout():
    fig, ax = plt.subplots(figsize=(9.5, 5.2))

    # ---- linac ----
    ax.add_patch(Rectangle((0.2, 6.2), 4.6, 0.55, fc="#9ecae1", ec="k", lw=1))
    ax.text(2.5, 6.95, "SNS linac  (H$^-$, 1.3 GeV, 1 ms macropulses @ 60 Hz, 2.8 MW)",
            ha="center", fontsize=9)
    ax.add_patch(FancyArrow(4.8, 6.475, 0.55, 0, width=0.06, color="k",
                            length_includes_head=True))

    # ---- HEBT / ring ----
    ring = Circle((7.4, 6.45), 1.05, fc="none", ec="k", lw=1.6)
    ax.add_patch(ring)
    ax.text(7.4, 6.45, "accumulator\nring\n(~1 µs/turn)", ha="center",
            va="center", fontsize=8.5)

    # ring -> FTS/STS
    ax.add_patch(FancyArrow(8.45, 6.45, 1.25, 0, width=0.06, color="k",
                            length_includes_head=True))
    ax.add_patch(Rectangle((9.7, 6.1), 1.6, 0.7, fc="#cccccc", ec="k"))
    ax.text(10.5, 6.45, "FTS / STS\n(neutrons)", ha="center", va="center", fontsize=8.5)

    # ---- option 1a/1b: linac station ----
    ax.add_patch(FancyArrowPatch((3.9, 6.2), (3.9, 4.45),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color="tab:green", lw=1.8))
    ax.text(4.05, 5.3, "1a: laser-assisted extraction\n"
                       "(parasitic, ≤100 kW, 1 ms @ 60 Hz;\n"
                       "gated ns micro-slices?)",
            fontsize=8, color="tab:green", va="center")
    ax.add_patch(Rectangle((3.2, 3.7), 1.5, 0.75, fc="#c7e9c0", ec="k"))
    ax.text(3.95, 4.07, "linac station\n(phase 1)", ha="center", va="center", fontsize=8.5)

    # ---- option 2b: ring extraction to BSM dump ----
    ax.add_patch(FancyArrowPatch((7.4, 5.4), (7.4, 3.1),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color="tab:red", lw=2.2))
    ax.text(7.55, 4.35, "2b: single-turn kicker extraction\n"
                        "~1 µs pulses @ ~6 Hz, ≤300 kW\n"
                        "duty factor 6×10$^{-6}$, 2.6×10$^{22}$ POT/yr",
            fontsize=8, color="tab:red", va="center")

    # ---- BSM dump station ----
    ax.add_patch(Rectangle((6.55, 2.3), 1.7, 0.8, fc="#fcbba1", ec="k"))
    ax.text(7.4, 2.7, "BSM dump station\n(flagship)", ha="center", va="center", fontsize=8.5)

    # near chamber + far hall
    ax.add_patch(FancyArrowPatch((7.4, 2.3), (7.4, 1.45), arrowstyle="-|>",
                                 mutation_scale=12, color="k", lw=1.2))
    ax.add_patch(Rectangle((5.7, 0.75), 3.4, 0.7, fc="#fee0d2", ec="k"))
    ax.text(7.4, 1.1, "near decay chamber (0.3–3.6 m)", ha="center",
            va="center", fontsize=8.5)
    ax.add_patch(FancyArrowPatch((8.8, 1.1), (10.4, 1.1), arrowstyle="-|>",
                                 mutation_scale=12, color="k", lw=1.2))
    ax.add_patch(Rectangle((10.4, 0.75), 1.5, 0.7, fc="#fee0d2", ec="k"))
    ax.text(11.15, 1.1, "far hall\n(15–25 m)", ha="center", va="center", fontsize=8.5)

    ax.set_xlim(0, 12.2)
    ax.set_ylim(0.3, 7.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Beam delivery options for an SNS BSM fixed-target program", fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "facility_layout.png", dpi=180)


def near_detector():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    # z in meters on x-axis, transverse meters on y
    # beam
    ax.add_patch(FancyArrow(-0.9, 0, 0.75, 0, width=0.02, head_width=0.08,
                            color="tab:red", length_includes_head=True))
    ax.text(-0.55, 0.12, "p, 1.3 GeV\n2.4×10$^{14}$/pulse", fontsize=8,
            color="tab:red", ha="center")

    # tungsten dump
    ax.add_patch(Rectangle((0, -0.15), 0.30, 0.30, fc="#636363", ec="k"))
    ax.text(0.225, -0.72, "W dump: r=15 cm, L=30 cm (~3$\\lambda_{int}$)",
            ha="center", fontsize=8)

    # shielding collar
    ax.add_patch(Rectangle((0, -0.55), 0.45, 0.40, fc="#bdbdbd", ec="k", alpha=0.8))
    ax.add_patch(Rectangle((0, 0.15), 0.45, 0.40, fc="#bdbdbd", ec="k", alpha=0.8))
    ax.text(0.225, 0.62, "steel/poly shield collar", ha="center", fontsize=8)

    # vacuum decay chamber
    ax.add_patch(Rectangle((0.6, -0.5), 3.0, 1.0, fc="#deebf7", ec="k", lw=1.2))
    ax.text(2.1, 0, "evacuated decay volume\n($<10^{-3}$ mbar), L = 3 m, r = 0.5 m",
            ha="center", va="center", fontsize=9)

    # tracker
    for z in (3.38, 3.48):
        ax.add_patch(Rectangle((z, -0.5), 0.035, 1.0, fc="#31a354", ec="k", lw=0.5))
    ax.text(3.45, 0.62, "2 tracking planes\n(LGAD/µRWELL, <1 mm)", ha="center", fontsize=8)

    # calorimeter
    ax.add_patch(Rectangle((3.6, -0.55), 0.45, 1.1, fc="#fdae6b", ec="k", lw=1.2))
    ax.text(3.83, -0.72, "4D EM calorimeter\n(CsI(Tl)+LGAD, ~50 ps)", ha="center", fontsize=8)

    # ALP trajectory
    ax.plot([0.12, 2.6], [0, 0.0], ls="--", color="tab:red", lw=1)
    ax.plot([2.6, 3.78], [0.0, 0.28], color="tab:orange", lw=1)
    ax.plot([2.6, 3.78], [0.0, -0.22], color="tab:orange", lw=1)
    ax.text(2.62, 0.08, "$a\\to\\gamma\\gamma$", fontsize=9, color="tab:red")

    # dimension arrows
    for (z1, z2, y, txt) in [(0.30, 0.6, -0.95, "0.3 m"),
                             (0.6, 3.6, -0.95, "3.0 m")]:
        ax.add_patch(FancyArrowPatch((z1, y), (z2, y), arrowstyle="<|-|>",
                                     mutation_scale=10, color="k", lw=1))
        ax.text((z1 + z2) / 2, y - 0.13, txt, ha="center", fontsize=8)

    # far hall indicator
    ax.add_patch(FancyArrowPatch((4.3, 0), (5.1, 0), arrowstyle="-|>",
                                 mutation_scale=10, color="0.4", lw=1, ls=":"))
    ax.text(4.7, 0.12, "to far hall:\n10-t LAr @ 15 m\n(DM scatter / CEvNS)",
            fontsize=8, color="0.3", ha="center")

    ax.set_xlim(-1.05, 5.6)
    ax.set_ylim(-1.25, 0.95)
    ax.set_aspect("equal")
    ax.set_xlabel("z  [m]")
    ax.axis("off")
    ax.set_title("Near detector: side view (not to scale transversely)", fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "near_detector.png", dpi=180)


if __name__ == "__main__":
    facility_layout()
    near_detector()
    print("diagrams written")
