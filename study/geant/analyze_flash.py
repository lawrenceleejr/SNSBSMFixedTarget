#!/usr/bin/env python3
"""
Analysis of the Geant4 prompt-flash simulation (flash.cc).

Reads the per-thread CSV hit files (particles crossing the scoring planes for
a delta-function 1.3 GeV proton pulse on the bare W dump), and produces:

  1. arrival-time spectra of neutrons / photons at each plane, both for the
     delta pulse and convolved with the option-2b ~700 ns beam pulse and with
     a 5 ns laser-sliced micro-pulse;
  2. per-beam-pulse particle counts through each plane inside the prompt
     window, scaled to 2.4e14 protons/pulse (300 kW, 6 Hz, 1.3 GeV);
  3. the figure geant_flash.png and a machine-readable summary.

Planes (must match flash.cc):
  0: decay-chamber entrance, z = 0.6 m, r < 0.5 m
  1: calorimeter face,       z = 3.6 m, r < 0.5 m
  2: far hall,               z = 15 m,  r < 1.0 m
"""

import glob
import json
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).parent
PROTONS_PER_PULSE = 2.4e14
PULSE_NS = 700.0          # option 2b (one ring turn)
SLICE_NS = 5.0            # laser-sliced micro-pulse scenario
PLANES = {0: ("decay-chamber entrance (0.6 m)", 0.6),
          1: ("calorimeter face (3.6 m)", 3.6),
          2: ("far hall (15 m)", 15.0)}
SPECIES = {"neutron": [2112], "photon": [22], "charged": None}  # None = the rest


def load(n_events):
    rows = []
    for f in sorted(glob.glob(str(HERE / "build" / "flash_hits_t*.csv"))):
        rows.append(np.loadtxt(f, delimiter=",", skiprows=1))
    d = np.vstack(rows)
    return {"plane": d[:, 0].astype(int), "pdg": d[:, 1].astype(int),
            "ekin": d[:, 2], "t": d[:, 3], "r": d[:, 4], "n_events": n_events}


def species_mask(d, name):
    pdgs = SPECIES[name]
    if pdgs is None:
        m = np.ones(len(d["pdg"]), bool)
        for p in [2112, 22]:
            m &= d["pdg"] != p
        return m
    return np.isin(d["pdg"], pdgs)


def main():
    n_events = int((HERE / "build" / "n_events.txt").read_text())
    d = load(n_events)
    scale = PROTONS_PER_PULSE / n_events   # delta-pulse hits -> per beam pulse

    summary = {"n_events": n_events, "protons_per_pulse": PROTONS_PER_PULSE}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)

    tbins = np.geomspace(1.0, 1e4, 120)
    for ip, (label, dist_m) in PLANES.items():
        ax = axes[ip]
        pm = d["plane"] == ip
        plane_sum = {}
        for sp, color in [("photon", "tab:orange"), ("neutron", "tab:blue"),
                          ("charged", "tab:green")]:
            m = pm & species_mask(d, sp)
            t = d["t"][m]
            w = np.full(len(t), scale)
            ax.hist(t, bins=tbins, weights=w, histtype="step", lw=1.6,
                    color=color, label=sp)
            # in-window counts: delta-pulse arrivals within [0, PULSE_NS]
            # after convolution with a square pulse of width PULSE_NS, every
            # particle arriving with delay < PULSE_NS overlaps the pulse.
            plane_sum[sp] = {
                "per_pulse_total": float(len(t) * scale),
                "per_pulse_within_700ns": float((t < PULSE_NS).sum() * scale),
                "median_t_ns": float(np.median(t)) if len(t) else None,
                "median_ekin_MeV": float(np.median(d["ekin"][m])) if len(t) else None,
            }
        gamma_tof = dist_m / 0.2998
        ax.axvline(gamma_tof, color="0.4", ls=":", lw=1)
        ax.text(gamma_tof * 1.15, ax.get_ylim()[1] if False else 1e12,
                "$\\gamma$ TOF", rotation=90, fontsize=8, color="0.4")
        ax.axvspan(gamma_tof, gamma_tof + PULSE_NS, color="tab:red",
                   alpha=0.08, lw=0)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("arrival time after proton impact  [ns]")
        ax.set_title(label, fontsize=10)
        summary[f"plane{ip}"] = plane_sum

    axes[0].set_ylabel(f"particles / beam pulse ({PROTONS_PER_PULSE:.1e} p) / bin")
    axes[0].legend(fontsize=9)
    for ax in axes:
        ax.grid(alpha=0.25, which="both", lw=0.4)
    fig.suptitle("Prompt flash at the SNS BSM dump (Geant4 Shielding, delta-pulse response; "
                 "red band = 700 ns prompt window)", fontsize=11)
    fig.tight_layout()
    fig.savefig(HERE / "geant_flash.png", dpi=170)

    # ---- TOF separability in the 5 ns micro-slice scenario at plane 1 ----
    fig2, ax2 = plt.subplots(figsize=(7.2, 4.6))
    pm = d["plane"] == 1
    tb = np.linspace(0, 200, 201)
    for sp, color in [("photon", "tab:orange"), ("neutron", "tab:blue")]:
        m = pm & species_mask(d, sp)
        # convolve delta response with a 5 ns square micro-pulse
        t = d["t"][m][:, None] + np.random.default_rng(1).uniform(
            0, SLICE_NS, (species_mask(d, sp) & pm).sum())[:, None]
        ax2.hist(t.ravel(), bins=tb, weights=np.full(t.size, scale),
                 histtype="stepfilled", alpha=0.45, color=color, label=sp)
    ax2.axvspan(12.0, 12.0 + SLICE_NS + 3, color="tab:red", alpha=0.15,
                label="signal window ($\\gamma$ TOF + 8 ns)")
    ax2.set_yscale("log")
    ax2.set_xlabel("arrival time at calorimeter face (3.6 m)  [ns]")
    ax2.set_ylabel("particles / micro-pulse-equivalent / ns")
    ax2.set_title("TOF separation with a 5 ns laser-sliced micro-pulse", fontsize=10.5)
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.25, lw=0.4)
    fig2.tight_layout()
    fig2.savefig(HERE / "geant_flash_microslice.png", dpi=170)

    # fraction of neutrons at plane 1 arriving AFTER gamma window
    m = pm & species_mask(d, "neutron")
    tn = d["t"][m]
    frac_late = float((tn > 20.0).sum() / max(len(tn), 1))
    summary["plane1_neutron_frac_after_20ns"] = frac_late

    (HERE / "flash_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
