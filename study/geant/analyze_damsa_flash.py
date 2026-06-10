#!/usr/bin/env python3
"""
Background budget for the DAMSA-at-SNS configuration -- the zero-background
validation behind the limit plots.

Inputs: Geant4 flash_damsa run (10 cm W dump + 10 cm W plug (~30 X0, ~1
lambda_int); calorimeter plane z = 0.55 m, r = 0.1 m) and the bare-dump
flash run (punch-through bound before the plug).

Signal gate: gamma TOF (1.83 ns) - 0.05 .. + 0.35 ns, per 5.9e8-proton
micro-bunch; sparse train 1 bunch/us -> 5.4e12 gates in 5 yr.
An ALP candidate = two EM clusters, each > 30 MeV, in-gate, neutral,
forming a vertex inside the vacuum volume and pointing back to the dump.
"""

import glob
import json
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent
P_BUNCH = 5.9e8
GATE_NS = 0.40
GATES_5YR = 6.0e4 * 5000 * 3600 * 5
N_EVENTS = 100_000
NEUTRINOS = {12, -12, 14, -14}


def load(pattern):
    d = np.vstack([np.loadtxt(f, delimiter=",", skiprows=1)
                   for f in sorted(glob.glob(str(HERE / "build" / pattern)))])
    return (d[:, 0].astype(int), d[:, 1].astype(int), d[:, 2], d[:, 3], d[:, 4])


def main():
    out = {"protons_per_bunch": P_BUNCH, "gate_ns": GATE_NS, "gates_5yr": GATES_5YR}

    # ---- DAMSA-geometry run: prompt and glow at the calorimeter plane ----
    plane, pdg, ekin, t, _ = load("flash_damsa_hits_t*.csv")
    pm = plane == 1
    gtof = 0.55 / 0.2998
    in_gate = pm & (t - gtof > -0.05) & (t - gtof < 0.35)
    out["prompt_in_gate_hits_in_MC"] = int(in_gate.sum())  # all species, 1e5 p

    late = pm & (t > 500)  # the pi/mu decay "glow", phase-uniform
    glow_g = late & (pdg == 22)
    glow_e = late & (np.abs(pdg) == 11)
    glow_nu = late & np.isin(pdg, list(NEUTRINOS))
    glow_n = late & (pdg == 2112)
    span_ns = 9500.0  # 0.5..10 us MC window
    per_gate = lambda n: n / N_EVENTS / span_ns * GATE_NS * P_BUNCH
    out["glow_per_gate"] = {
        "photon_all": per_gate(glow_g.sum()),
        "photon_gt15MeV": per_gate((glow_g & (ekin > 15)).sum()),
        "photon_gt30MeV_MCcount": int((glow_g & (ekin > 30)).sum()),  # 0 observed
        "photon_max_E_MeV": float(ekin[glow_g].max()),
        "electron_positron": per_gate(glow_e.sum()),
        "neutrino_invisible": per_gate(glow_nu.sum()),
        "neutron": per_gate(glow_n.sum()),
    }
    # Late photons above 30 MeV: nuclear capture/inelastic gammas end at the
    # giant-dipole endpoint ~25 MeV (observed max 23.2 MeV), so the only
    # source is Michel-positron bremsstrahlung escaping the dump:
    #   ~0.1 mu+/p  x  ~0.2 (brems > 30 MeV before stopping in W)
    #   x  e^-22 (escape >= 25 X0)  x  8.3e-3 (aperture)  / ~3000 ns (mu chain)
    mu_glow30 = 0.1 * 0.2 * np.exp(-22) * 8.3e-3 / 3000.0 * GATE_NS * P_BUNCH
    out["glow_gamma_gt30_per_gate_physics"] = mu_glow30
    out["glow_accidental_pairs_5yr"] = 0.5 * mu_glow30**2 * GATES_5YR
    # ultra-conservative cross-check, exponential tail through the nuclear
    # endpoint (unphysical; kept to show even this fails to matter after
    # the vertex requirement -- see README):
    s_15 = (glow_g & (ekin > 15)).sum() / max(glow_g.sum(), 1)
    out["glow_gamma_gt30_per_gate_exp_extrapolation"] = float(
        per_gate(glow_g.sum()) * s_15 * np.exp(-15 / 3.2))

    # ---- bare-dump run: prompt punch-through bound before the plug ----
    plane, pdg, ekin, t, r = load("flash_hits_t*.csv")
    ap = (plane == 0) & (r < 10.0)  # DAMSA aperture at 0.6 m
    ig = (t - 2.0 > -0.05) & (t - 2.0 < 0.35)
    bare_g30 = (ap & ig & (pdg == 22) & (ekin > 30)).sum()  # 0 observed
    out["bare_prompt_gamma30_in_MC"] = int(bare_g30)
    mu_bare = max(bare_g30, 2.3) / N_EVENTS  # 90% UL per proton
    plug_atten = np.exp(-10.0 / 0.3504 * 7.0 / 9.0)  # 30 X0 W, pair-dominated
    mu_prompt = mu_bare * plug_atten * P_BUNCH
    out["prompt_gamma30_per_gate_after_plug_UL"] = mu_prompt
    out["prompt_pairs_5yr_UL"] = 0.5 * mu_prompt**2 * GATES_5YR

    # ---- combined: accidental diphoton candidates before topology cuts ----
    mu_tot = mu_glow30 + mu_prompt
    pairs = 0.5 * mu_tot**2 * GATES_5YR
    out["total_accidental_pairs_5yr_before_topology"] = pairs
    # fiducial vacuum vertex (<1e-3) and diphoton mass window (~3%):
    out["expected_events_5yr_after_topology"] = pairs * 1e-3 * 0.03

    (HERE / "damsa_background_budget.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
