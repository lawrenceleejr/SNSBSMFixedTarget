# RF Time-Structure Options: 400 MHz Ring Modulation and 2.4 ns Laser-Stripped Bunches

Two beam-structure upgrades beyond the four workshop options, and what each buys
the BSM program. Quantitative statements use the Geant4 flash simulation
([`../study/geant/`](../study/geant/README.md)) and the ALP sensitivity machinery
([`../study/`](../study/README.md)).

## 1. 400 MHz modulation of the extracted ring pulse

**What it is.** Preserve (or re-impose) the linac's 402.5 MHz structure on the
~700 ns extracted pulse: a comb of ~100–300 ps micro-buckets every 2.48 ns,
at the full 300 kW. The detector then measures arrival *phase* relative to the
RF, not just arrival within the macro-pulse.

**The key fact (measured in our Geant4 data + analytic):** every dangerous
background is **uniform in RF phase**, while signal is **phase-locked**:

| Population | timing relative to 2.48 ns comb | in a 0.35 ns gate |
|---|---|---|
| ALPs, dark photons, π⁰-portal DM (β ≈ 1; π⁰ decays in 10⁻¹⁶ s) | phase-locked | ~100% |
| Beam neutrons at 3.6 m / 15 m | uniform (measured: in-gate fraction 0.142 vs uniform 0.141) | 14% |
| Prompt ν_µ from π⁺ DAR (τ_π = 26 ns ≫ 2.48 ns) | uniform | 14% |
| Steady-state (cosmics etc.) | uniform | 14% (duty → 8×10⁻⁷) |

So a phase gate is a **~7–17× cut on every background at zero signal cost and
zero power cost** (7× for a 0.35 ns gate, 17× for 0.15 ns, set by calorimeter
timing). It is a frequency-domain (lock-in) version of the short-pulse trick.

**BSM applications:**

1. **Beating the prompt-neutrino floor in the far-hall DM search.** In the
   COHERENT-style analysis, relativistic DM and prompt ν_µ occupy the *same*
   prompt window — the ν_µ is the irreducible floor. The RF comb splits them:
   DM is phase-locked to the production bucket, ν_µ is phase-uniform because
   the parent π⁺ forgets the bucket over its 26 ns lifetime. A 7–17× prompt-ν
   suppression at full 300 kW directly extends the dark-photon/DM (ε, y) reach
   in the background-limited regime.
2. **Velocity spectroscopy on any discovery.** A phase slip
   Δt = (L/c)(1/β − 1), measurable at the ~100 ps level over 15–25 m, turns
   a candidate excess into a mass measurement, and off-phase populations tag
   slow heavy states (the MiniBooNE / T2K off-bucket search technique,
   here with 20× finer combs).
3. **What it does *not* fix:** the near-chamber in-pulse flash only drops from
   ~2.6×10¹³ to ~3×10¹² per pulse in-gate — still hopeless. The near chamber
   needs option 2 below.

**Feasibility flag for the accelerator group:** ring revolution frequency is
~1.06 MHz, and 402.5 MHz is *not* an integer harmonic; preserving the comb
through 1060-turn accumulation requires an h ≈ 380 RF system (~402 MHz) with
enough voltage to prevent debunching, or RF re-bunching in the extraction
line. This is the question to pose; the physics payoff above is the
justification.

## 2. 2.4 ns bunch structure from precision laser stripping

**What it is.** A stripping laser phase-locked to the 402.5 MHz linac
structure extracts *individual micro-bunches*: ~50 ps long, ~5.9×10⁸ protons
each (38 mA peak / 402.5 MHz), with fully programmable spacing — from every
bucket (≈100 kW) down to arbitrarily sparse trains. This is the strongest
version of the "gated micro-slice" idea: each event gets an unambiguous,
ps-precision production-time reference.

**The sweet spot is a sparse train: one bucket per ~1 µs** (1 MHz during the
1 ms macropulse, 60 Hz): **7.3 kW, 6.4×10²⁰ POT/yr**, parasitic to the
neutron program. The 1 µs spacing lets each bunch's neutron flash clear the
3.6 m hall (98.5% of neutrons arrive within 1 µs) before the next bunch.

**Geant4-anchored background budget per bunch, in the γ-TOF signal gate
(0.35 ns) at the calorimeter face, bare dump:**

| Source | per bunch in gate | mitigation |
|---|---|---|
| photons > 30 MeV | 1.2×10⁴ | ~20 X₀ Pb plug on dump face → < 1 |
| neutrons, same bunch | ~0 (needs β > 0.96 ⇒ T_n > 2.4 GeV) | kinematically excluded |
| neutrons, previous bunches (µs-aliased) | ~30, vertex-less | diphoton vertex + mass |
| steady-state | in-gate duty 2.1×10⁻⁵ | negligible for a ~0.1 m² detector |

This is the configuration where the **zero-background assumption of the ALP
study is actually defensible**, with each candidate independently verified by
TOF.

**Sensitivity cost of the lower power:** added as the purple contour in
[`../study/alp_limit_plot.png`](../study/alp_limit_plot.png). With 5 yr
(3.2×10²¹ POT) the exclusion floor sits only ~2.5× above the 300 kW near-chamber
curve — near the floor the zero-background limit scales as POT^(1/4) — and the
high-coupling ceiling, which is exponential in geometry rather than statistics,
barely moves. **The ns-bunch mode covers most of the newly probed wedge at 2%
of the beam power**, and it can run from day one at the phase-1 linac station.

## 3. The combined program

| Beam mode | Station | Power | Role |
|---|---|---|---|
| 2b: 700 ns @ 6 Hz | far hall | 300 kW | DM scattering, CEvNS/NSI, steriles |
| 2b + 400 MHz comb | far hall | 300 kW | DM below the prompt-ν floor; β spectroscopy |
| linac 2.4 ns sparse train | near chamber | ~7 kW | ALP → γγ wedge, true zero background |
| linac 2.4 ns full train | near chamber | ≤100 kW | ALP statistics running with phase gating, if flash occupancy allows |

The two upgrades are complementary, not competing: **400 MHz modulation is a
far-hall (scattering) tool — it rescues full beam power for searches limited
by phase-uniform backgrounds — while ps laser-stripped bunches are the
near-chamber (decay) tool — they buy event-by-event TOF where no amount of
power helps.** Together they would make the SNS the only facility offering
both a 300 kW phase-combed DAR source and a ps-timed beam-dump line.
