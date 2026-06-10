# Geant4 Prompt-Flash Study

Quantifies the beam-related background environment at the near decay chamber
and far hall of the proposed SNS BSM dump station, testing the
zero-background assumption used in the [ALP sensitivity study](../README.md).

## Setup

- **Geant4 11.4.1**, `Shielding` reference physics list (HP neutron transport,
  G4NDL 4.7.1), conda-forge build.
- Geometry (`flash.cc`): 1.3 GeV proton pencil beam on a **bare** compact
  tungsten dump (r = 15 cm, L = 30 cm ≈ 3 λ_int) in an air hall — i.e. the
  worst case, no shielding at all. Matches the ALP-study near configuration.
- Scoring: every particle (E > 0.1 MeV) crossing, in the +z direction:
  - plane 0: z = 0.6 m, r < 0.5 m — decay-chamber entrance;
  - plane 1: z = 3.6 m, r < 0.5 m — calorimeter face;
  - plane 2: z = 15 m, r < 1.0 m — far-hall detector.
- 10⁵ primaries (delta pulse at t = 0); beam pulse shapes applied by
  convolution in `analyze_flash.py`. Tracks killed at t > 10 µs; neutrons
  killed below 100 keV.

Build/run:

```bash
micromamba run -p /opt/g4env cmake .. && make    # in build/
micromamba run -p /opt/g4env ./flash 100000
python3 analyze_flash.py
```

## Results

Per beam pulse of 2.4×10¹⁴ protons (option 2b full power), particles crossing
each plane; "in window" = arriving within the ~700 ns pulse, i.e.
indistinguishable from signal by timing at that pulse width:

| Plane | photons / pulse | neutrons / pulse | charged / pulse | median E_n | n arriving < γTOF+8 ns |
|---|---|---|---|---|---|
| chamber entrance (0.6 m) | 4.6×10¹³ | 6.7×10¹⁴ | 3.4×10¹³ | 0.48 MeV | — |
| calorimeter face (3.6 m) | 1.4×10¹² | 2.0×10¹³ (90% in window) | 6.8×10¹² | 0.54 MeV | **4.2%** |
| far hall (15 m) | 2.7×10¹¹ | 4.1×10¹² (25% in window) | 1.9×10¹² | 0.60 MeV | ~0 |

![flash time spectra](geant_flash.png)

![micro-slice TOF](geant_flash_microslice.png)

## Interpretation

1. **A bare dump + 700 ns pulse does not support the near-detector
   zero-background assumption.** ~10¹⁴-scale neutrons and ~10¹³ photons
   sweep the chamber aperture inside the prompt window every pulse. The
   vacuum volume itself is inert, but the calorimeter face sees ~3×10¹³
   particles per pulse — far beyond any in-window exclusive reconstruction.
2. **Time of flight is the strongest single handle, and it requires a short
   pulse.** At 3.6 m, 96% of neutrons arrive later than the photon flight
   time + 8 ns (they are mostly few-MeV evaporation neutrons, β ~ 0.05; the
   4% early tail is the >200 MeV spallation component). With the ~700 ns
   option-2b pulse this ordering is washed out; with a **ns-scale
   micro-slice** (gated laser stripping at the linac station) the signal
   window cleanly precedes the bulk of the flash (second figure). Per
   402.5 MHz micro-bunch (~6×10⁸ p), the in-signal-window neutron crossing
   count drops to ~2×10⁶ over the full calorimeter face — a ~10⁷ reduction
   before any shielding, vertexing, or kinematic cuts.
3. **The far hall works as advertised with the 700 ns pulse.** Only 25% of
   neutrons arrive in-window at 15 m and the field is 160× weaker than at the
   chamber entrance; with the standard tens-of-cm steel/poly monolith
   (not simulated here) plus the 6×10⁻⁶ duty factor, this is the
   CCM/COHERENT operating regime, validated by those experiments.
4. **Charged punch-through (median ~570 MeV forward protons/pions, ~7×10¹²
   per pulse at 3.6 m) motivates a sweeper dipole** between dump and chamber,
   plus the tracker front veto.

Design consequences adopted in `docs/experiment_design.md`: shield plug and
sweeper for the near line; the near chamber's flagship operation pairs
naturally with ns micro-slices (linac station) while the 700 ns ring pulses
drive the far-hall program.

## Caveats

- No shielding, building, or floor in the geometry: prompt fluxes through the
  planes are conservative (high), but room-return/albedo neutrons — relevant
  at late times — are underestimated.
- Neutrons below 100 keV and times beyond 10 µs are truncated (capture-γ
  backgrounds between pulses not addressed; the 167 ms inter-pulse gap and
  duty factor handle these).
- Delta-pulse convolution assumes a rectangular beam pulse.
- Statistics: 10⁵ primaries → few-% precision at the far plane.

## DAMSA-at-SNS background budget: validating the zero-background assumption

The limit plots assume zero background (90% CL = 2.3 signal events) for the
DAMSA-at-SNS configuration. A second Geant4 run (`flash_damsa.cc`: 10 cm W
dump + 10 cm W plug ≈ 30 X₀ ≈ 1 λ_int; calorimeter plane z = 0.55 m,
r = 0.1 m; 10⁵ protons) tests that assumption directly. An ALP candidate
requires **two neutral EM clusters, each > 30 MeV, inside the 0.4 ns TOF
gate, forming a vertex inside the vacuum volume and pointing back to the
dump**. Sparse-train exposure: 5.4×10¹² gates in 5 yr
(`analyze_damsa_flash.py` → `damsa_background_budget.json`).

| Component | Measured / derived | In-gate, per bunch | Killed by |
|---|---|---|---|
| Prompt flash (same bunch) | **0 hits in 10⁵ p — even before the plug** at the DAMSA aperture; plug adds e⁻²² for γ | < 3×10⁻⁶ (90% UL × plug) | MC UL alone → ≤ 26 accidental pairs / 5 yr |
| Glow γ (π/µ decay chain, phase-uniform) | 10.9/gate, but max E = 23.2 MeV — nuclear (giant-dipole) endpoint ~25 MeV | > 30 MeV: ~4×10⁻⁹ (Michel-brems escape, calculable) | 30 MeV cluster threshold |
| Glow e± (Michel) | 0.75/gate, ≤ 53 MeV | — | tracker charged veto |
| Glow neutrinos | 65/gate | — | invisible (σ ~ 10⁻⁴³ cm²) |
| Glow neutrons | 2.2/gate, all < 15 MeV | — | threshold + CsI pulse-shape |
| Cosmics | in-gate live time = 2160 s / 5 yr | ~10³–10⁴ µ total | charged veto; neutrals fail vertex+pointing |

Combining: ≤ 26 accidental diphoton pairs in 5 yr **before** topology cuts
(dominated by the MC-statistics upper limit on prompt punch-through, not by
any observed process), and **N_bkg ≈ 8×10⁻⁴ events after the fiducial-vertex
(≤10⁻³) and mass-window (~3%) requirements alone** — pointing, cluster shape,
and the 4D timing are still in reserve. Even the deliberately unphysical
exponential extrapolation of the glow spectrum through the nuclear endpoint
(2.3×10⁻³ γ>30 MeV/gate) yields only ~4 events after the full cut chain.

Conclusion: **the zero-background assumption is fair for the sparse ns-bunch
DAMSA-at-SNS configuration**, with three load-bearing requirements exposed by
the simulation: (i) the ≥30 MeV per-cluster threshold (the glow is entirely
below it — a physics statement about nuclear γ endpoints, confirmed by the
MC spectrum); (ii) the front-tracker charged veto (Michel positrons);
(iii) the ~30 X₀ dump-side plug (prompt γ flash). A dedicated high-statistics
run of the prompt punch-through (the current number is an MC-stat bound, not
a measurement) is the one item left for a full proposal.
