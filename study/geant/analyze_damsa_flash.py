#!/usr/bin/env python3
"""
Background budget for the DAMSA-at-SNS configuration, from the Geant4
flash_damsa simulation (10 cm W dump + 10 cm W plug (~30 X0), DAMSA chamber:
entrance plane z = 0.24 m / r = 0.1 m, calorimeter plane z = 0.55 m / r = 0.1 m).

Converts the delta-pulse response into expected counts per 5.9e8-proton
micro-bunch inside the TOF signal gate (gamma TOF - 0.05 ns .. + 0.35 ns),
then into expected background EVENTS in a 5-year sparse-train exposure
(6e4 bunches/s * 5000 h/yr * 5 yr = 5.4e12 gates), to test the
zero-background assumption behind the limit plots.
"""

import glob
import json
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent
P_BUNCH = 5.9e8            # protons per 402.5 MHz micro-bunch
GATE_LO, GATE_HI = -0.05, 0.35   # ns around gamma TOF
GATES_5YR = 6.0e4 * 5000 * 3600 * 5   # sparse train, 1 bunch/us
CALO_Z_M = 0.55
N_EVENTS = 100_000


def main():
    d = np.vstack([np.loadtxt(f, delimiter=",", skiprows=1)
                   for f in sorted(glob.glob(str(HERE / "build" / "flash_damsa_hits_t*.csv")))])
    plane, pdg, ekin, t = d[:, 0].astype(int), d[:, 1].astype(int), d[:, 2], d[:, 3]
    gtof = CALO_Z_M / 0.2998  # ns

    out = {}
    pm = plane == 1  # calorimeter face
    for name, mask in [("photon", pm & (pdg == 22)),
                       ("neutron", pm & (pdg == 2112)),
                       ("charged", pm & (pdg != 22) & (pdg != 2112))]:
        tt, ee = t[mask], ekin[mask]
        in_gate = (tt - gtof > GATE_LO) & (tt - gtof < GATE_HI)
        out[name] = {
            "per_p": mask.sum() / N_EVENTS,
            "per_p_gt30MeV": (ee > 30).sum() / N_EVENTS,
            "per_bunch_in_gate": in_gate.sum() / N_EVENTS * P_BUNCH,
            "per_bunch_in_gate_gt30MeV": (in_gate & (ee > 30)).sum() / N_EVENTS * P_BUNCH,
        }
        # aliased rate: arrival-time density near 1 us (previous-bunch pile-in)
        late = (tt > 500) & (tt < 2000)
        dens_per_ns = late.sum() / N_EVENTS / 1500.0
        out[name]["per_bunch_aliased_in_gate"] = dens_per_ns * (GATE_HI - GATE_LO) * P_BUNCH
    out["gates_5yr"] = GATES_5YR

    # expected in-gate singles over 5 yr and accidental diphoton pairs/gate
    for name in ("photon", "neutron", "charged"):
        s = out[name]
        mu = s["per_bunch_in_gate_gt30MeV"] + s["per_bunch_aliased_in_gate"]
        s["singles_5yr"] = mu * GATES_5YR
        s["accidental_pairs_5yr"] = 0.5 * mu**2 * GATES_5YR

    (HERE / "damsa_background_budget.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
