# What the SNS Beam Time Structure Options Buy Us for BSM Physics

Working notes on the "Beam Time Structure" slide (SNS fixed-target workshop), which lists
four possible beam delivery modes for a new fixed-target station. The question addressed
here: which of these modes enable a competitive BSM search program à la DAMSA, CCM,
COHERENT, or PIP2-BD, and what physics each mode is good for.

## 1. Decoding the slide

All modes assume the post-PPU linac: 1.3 GeV protons, 1 ms macropulses, 60 Hz.
Converting each option into the numbers that matter for a search experiment:

| # | Option | Pulse width | Rep rate | Power | Duty factor | POT/yr (5000 h) | p/pulse |
|---|--------|------------|----------|-------|-------------|------------------|---------|
| 1a | Linac station, laser-assisted extraction | 1 ms | 60 Hz | ≤100 kW | 6×10⁻² | ~9×10²¹ | ~8×10¹² |
| 1b | Linac station, kicker extraction | 1 ms | ~6 Hz | ≤300 kW | 6×10⁻³ | ~2.6×10²² | ~2.4×10¹⁴ |
| 2a | Ring station, no accumulation | 1 ms | ~6 Hz | ≤300 kW | 6×10⁻³ | ~2.6×10²² | ~2.4×10¹⁴ |
| 2b | **Ring station, with accumulation** | **~1 µs** | ~6 Hz | ≤300 kW | **6×10⁻⁶** | ~2.6×10²² | ~2.4×10¹⁴ |

(POT/s at 300 kW and 1.3 GeV is 1.4×10¹⁵; at 100 kW it is 4.8×10¹⁴. The ~1 µs pulse in
2b is one ring turn — the same ~700 ns FWHM structure delivered to the FTS today.)

At 1.3 GeV (√s ≈ 2.44 GeV in pN collisions) a stop-target is a π⁺/µ⁺ decay-at-rest (DAR)
source: ~0.1 ν per flavor per POT, a comparable π⁰ yield feeding photon/dark-sector
portals, and essentially no kaons. The accessible new-particle mass range is
MeV–few hundred MeV: exactly the DAMSA / CCM / COHERENT-DM territory.

## 2. Why time structure is *the* figure of merit

A DAR-source BSM search fights two background classes, and the beam time structure
controls both:

**Steady-state backgrounds (cosmics, radioactivity) scale with duty factor.**
Any beam-correlated search only counts background inside the beam window. Option 2b
(6×10⁻⁶) rejects steady-state background 10⁴× better than the 1 ms modes and ~10×
better than the present FTS as seen by COHERENT (60 Hz × ~700 ns ≈ 4×10⁻⁵). It matches
CCM at Lujan (20 Hz × 290 ns ≈ 6×10⁻⁶) and the PIP2-BD C-PAR design goal of O(10⁻⁶).

**Beam-related neutrons (BRN) are fought with pulse width + time of flight.**
This is the DAMSA design insight: signal photons/ALPs travel at ~c, while spallation
neutrons (mostly tens of MeV, β ≈ 0.1–0.5) arrive late. TOF discrimination only works if
the pulse is shorter than the neutron delay over the baseline. At 20 m, a 10 MeV neutron
arrives ~400 ns after the prompt window — resolvable with a ~700 ns pulse (this is how
CCM works at 23 m), totally invisible inside a 1 ms pulse.

**Pulse width vs the muon lifetime (τ_µ = 2.2 µs).**
With a ~1 µs pulse, prompt ν_µ from π⁺ DAR (τ_π = 26 ns) separate cleanly from delayed
ν_e/ν̄_µ from µ⁺ DAR. This is the engine of the COHERENT-style dark matter search
(D. Pershey et al.): relativistic DM scatters *in the prompt window*, while the delayed
window gives an in-situ neutrino/NIN control sample, largely cancelling flux systematics.
A 1 ms pulse (≫ τ_µ) erases this handle completely — prompt and delayed populations are
fully mixed. The ESS (2.86 ms pulses, duty 4×10⁻²) is the cautionary tale: enormous power,
but its long pulse is the main obstacle for its CEvNS/BSM program.

**Bottom line: option 2b (accumulated ~1 µs pulses at ~6 Hz) is the only mode on the
slide that supports the full modern stopped-pion BSM toolkit.** It is effectively a
dedicated, 300 kW copy of the beam CCM gets at Lujan (100 kW, shared) — at higher energy
and with 3× the power, i.e. the world's best dedicated pulsed DAR source for BSM.

## 3. Physics program by beam mode

### Option 2b — flagship BSM mode (1 µs, 6 Hz, 300 kW, ≥2×10²² POT/yr)

- **ALPs → γγ / e⁺e⁻ (DAMSA-style):** Primakoff/Compton production off the EM shower in
  the dump; a compact near detector (~10–20 m) with a vacuum decay volume, tracking, and
  fast crystal calorimetry probes the "cosmological triangle" and MeV-scale a–γ and a–e
  couplings. DAMSA's ultra-short baseline argument applies directly: proximity beats the
  beam-dump ceiling for short lifetimes; duty factor 6×10⁻⁶ + TOF handles cosmics and BRN.
- **Vector-portal light dark matter:** π⁰ → γ A′, A′ → χχ̄; χ scatters on
  electrons/nuclei in a CCM/COHERENT-class 10-ton LAr or CsI detector. Prompt-window
  search with delayed-window neutrino control. Leptophobic portals via π⁻ absorption à la
  CCM's leptophobic DM search.
- **CEvNS as a BSM probe:** precision NSI, neutrino magnetic moments, light mediators,
  with the prompt/delayed flavor decomposition intact.
- **Sterile neutrinos:** short-baseline ν_µ disappearance with the prompt monoenergetic
  29.8 MeV ν_µ (timing-tagged), plus LSND-style ν̄_e appearance.
- The 167 ms quiet gap between pulses gives essentially unlimited in-situ steady-state
  background measurement.

### Option 1a — cheapest first beam (1 ms, 60 Hz, ≤100 kW, parasitic)

Laser-assisted (laser-stripping) extraction peels beam off every macropulse without
stealing pulses from the neutron program — politically and operationally the easiest
start. The 6% duty factor rules out timing-based searches, but it supports:

- **Searches with self-tagging signatures:** LSND itself ran at 7% duty — IBD delayed
  coincidence substitutes for beam timing. An OscSNS-style ν̄_µ → ν̄_e program survives
  long pulses.
- **Millicharged particles** (integrating scintillator-telescope searches), muon physics
  (SEEMS-like, arXiv:2212.09823), detector R&D, irradiation, and target/dump prototyping
  for the flagship station.
- **A unique lever worth pursuing with the accelerator group:** laser stripping only
  extracts while the laser is on, and the linac micro-bunch structure is 402.5 MHz
  (~ps bunches every 2.5 ns). If the stripping laser can be gated/pulsed, this line could
  in principle deliver **ns-scale micro-slices at high repetition rate** — shorter pulses
  than CCM or even PIP2-BD C-PAR, at reduced power. That would enable genuinely
  DAMSA-like few-meter-baseline TOF physics that even option 2b's 1 µs pulse cannot do.
  This question should be put to the laser-stripping team explicitly.

### Options 1b / 2a — power without timing (1 ms, 6 Hz, 300 kW)

Full POT but 1 ms pulses: no prompt/delayed separation, no TOF, duty 6×10⁻³. Useful for
coincidence-tagged searches (LSND-style) and any flux-integrating measurement, but
strictly dominated by 2b for the headline BSM program. If the ring is available, there is
no physics case for extracting unaccumulated beam to a BSM target — 2a only makes sense
as a commissioning stage or if ring accumulation of the diverted pulses is precluded.

## 4. Where this would sit in the world

| Facility | E_p | Power to BSM-usable target | Pulse | Duty | Status |
|----------|-----|---------------------------|-------|------|--------|
| SNS FTS (COHERENT) | 1.3 GeV | 2 MW (shared, 20 m basement) | ~700 ns, 60 Hz | 4×10⁻⁵ | running |
| Lujan/CCM | 0.8 GeV | 100 kW (shared) | 290 ns, 20 Hz | 6×10⁻⁶ | running |
| J-PARC MLF (JSNS²) | 3 GeV | 1 MW (shared) | 2×100 ns, 25 Hz | ~5×10⁻⁶ | running |
| ESS | 2 GeV | 5 MW (shared) | 2.86 ms, 14 Hz | 4×10⁻² | ramping |
| PIP2-BD (proposed) | 0.8–1.2 GeV | 100 kW dedicated | <30 ns goal | 10⁻⁴–10⁻⁶ | not funded |
| **SNS option 2b** | **1.3 GeV** | **300 kW dedicated** | **~1 µs, 6 Hz** | **6×10⁻⁶** | this proposal |

A dedicated 300 kW station with 10⁻⁶-class duty factor would exceed CCM's source power
by 3× at higher energy, be available *now-ish* rather than on the PIP2-BD timescale, and
— unlike the COHERENT basement — allow purpose-built dump geometry, near-detector halls
at chosen baselines/angles, and overburden/shielding designed for the physics rather
than retrofitted.

## 5. Open questions for the accelerator side

1. Can the stripping laser be gated to extract ns-scale micro-slices (402.5 MHz bunch
   selection) instead of the full 1 ms envelope? At what extracted power?
2. Is the ~1 µs accumulated pulse from option 2b identical to the FTS pulse (~695 ns
   FWHM with 250 ns extraction gap), and could a sub-turn (shorter) extraction or
   in-ring rebunching shorten it further?
3. What is the realistic ramp: 1a parasitic kW-scale first beam → 2b at 6 Hz? Does 6 Hz
   to the new station trade 1:1 against FTS/STS pulses?
4. Dump design: a thick stopping target (DAR source, π⁻ capture) vs DAMSA-style compact
   tungsten dump with near vacuum chamber — these favor different stations and baselines;
   ideally the facility reserves space for both a ~10 m near hall and a ~20–30 m hall.

## References

- DAMSA conceptual design white paper: [arXiv:2601.15255](https://arxiv.org/abs/2601.15255);
  DAMSA concept paper: [arXiv:2504.02923](https://arxiv.org/abs/2504.02923)
- PIP2-BD: [arXiv:2203.08079](https://arxiv.org/abs/2203.08079); PIP-II beam dump physics
  opportunities: [arXiv:2311.09915](https://arxiv.org/abs/2311.09915)
- CCM first DM results: [PRD 106, 012001](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.106.012001);
  leptophobic DM: [arXiv:2109.14146](https://arxiv.org/abs/2109.14146);
  Lujan short-pulse upgrade (PSR): [arXiv:2204.01860](https://arxiv.org/abs/2204.01860)
- COHERENT at the SNS: [arXiv:2111.07033](https://arxiv.org/abs/2111.07033)
- OscSNS white paper: [arXiv:1307.7097](https://arxiv.org/abs/1307.7097)
- SEEMS (SNS linac extraction concept): [arXiv:2212.09823](https://arxiv.org/abs/2212.09823)
- Laser-assisted charge exchange at SNS: [NAPAC'25 TUYD01](https://prebys.physics.ucdavis.edu/NAPAC-25/proceedings/pdf/TUYD01.pdf)
- Accelerator-based dark sector facilities (Snowmass): [arXiv:2206.04220](https://arxiv.org/abs/2206.04220)

## 6. First quantitative sensitivity study

A first-pass ALP (a → γγ, Primakoff production) sensitivity study for the
option-2b beam is in [`study/`](../study/README.md), including the resulting
limit plot over the world's existing constraints. Headline: a DAMSA-style near
decay chamber (0.3 m from a compact W dump) with 5 yr at 300 kW probes new
parameter space in the short-lifetime wedge m_a ≈ 30–300 MeV between the
E137/E141/CHARM ceiling and the FASER/PrimEx/BESIII floors.
