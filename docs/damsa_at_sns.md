# DAMSA at the SNS: a Minimal Near-Chamber-Only Program

Question addressed: if we keep costs low and build *only* a near chamber —
specifically, the DAMSA detector as designed (table-top: 30 cm vacuum decay
chamber, 20 cm diameter, immediately behind a compact W dump; LGAD/µRWELL
tracking + ~100-crystal CsI(Tl) 4D calorimeter) — what do we get at the SNS,
and how does it compare to DAMSA's own staged projections?

## What makes DAMSA different from other beam dumps

A conventional beam-dump search (E137, E141, CHARM, NuCal) puts the detector
tens to hundreds of meters behind massive shielding. Distance + dirt *is* the
background strategy — but it makes the experiment blind to short-lived
particles: anything with a lab decay length below tens of meters decays inside
the shield. That is the beam-dump **ceiling**, and it is why the
high-coupling / high-mass wedge above the E137/CHARM bands is still open.

DAMSA's design inverts the strategy. It puts an *evacuated decay volume*
centimeters behind the dump and replaces passive shielding with **active,
exclusive reconstruction**: a two-photon vertex inside vacuum (nothing else
makes vertices there), an invariant mass, ~ps-class 4D calorimetry, and
time-of-flight against the neutron flash. Three consequences:

1. **Lifetime acceptance**: decay lengths of *centimeters* are visible —
   the ceiling moves up by orders of magnitude;
2. **Solid angle**: at 0.5 m total standoff, a 10 cm aperture covers
   ~1% of 4π — a 20 m baseline experiment needs a 4 m-radius detector to match;
3. **The cost structure collapses**: no decay tunnel, no shielding monolith,
   a table-top vacuum tank and one small calorimeter.

The price: the detector sits in the most hostile radiation environment of any
dump experiment, so the concept only works at a beam whose *time structure*
lets reconstruction + TOF carry the background load. That is exactly what the
sparse laser-stripped ns-bunch mode provides
([rf_structure_options.md](rf_structure_options.md)).

## DAMSA's own staging vs. "DAMSA at SNS"

DAMSA's published path (white paper, arXiv:2601.15255): Stage 0 at FAST
(300 MeV e⁻), Stage 1 at SLAC LESA (8 GeV e⁻, baseline 1.5×10¹⁴ EOT in
3–4 months, 200 W max), endgame at a future PIP-II beam-dump facility
(1 GeV protons, 2.5 MW, 1.565×10¹⁶ p/s). The pathfinders are *flux-starved*
(parasitic electron beams); the endgame *facility does not exist*.

The SNS sparse ns-bunch mode (1 micro-bunch/µs from gated laser stripping:
7.3 kW, 6.4×10²⁰ POT/yr, parasitic) feeds the same detector a photon flux of
8×10²⁰ γ over 5 yr — **~35,000× the LESA baseline photon flux** — because a
1.3 GeV proton makes 0.26 π⁰-decay photons for 0.2 nJ, while pathfinder
electrons are rationed in watts.

## Same detector, four beams, identical machinery

`study/damsa_at_sns.py` runs the DAMSA geometry (L₁ = 0.2 m, L₂ = 0.3 m,
r = 0.1 m, ε = 0.5, zero background, 2.3 events at 90% CL) under four beams.
Output: `study/damsa_at_sns.png`.

| Beam | POT/EOT | g floor @ 100 MeV | mass reach |
|---|---|---|---|
| **SNS ns-bunch sparse, 7.3 kW, 5 yr** | 3.2×10²¹ | **1.8×10⁻⁶** | 221 MeV |
| SNS 100 kW full train, 5 yr (stats only) | 4.5×10²² | 9.4×10⁻⁷ | 258 MeV |
| DAMSA endgame: PIP-II 2.5 MW, 5 yr | 1.4×10²⁴ | 4.8×10⁻⁷ | 258 MeV |
| DAMSA Path-Finder: LESA, 1.5×10¹⁴ EOT | 1.5×10¹⁴ | no coverage at 100 MeV | ~80 MeV (high-g only) |

Reading of the table:

- **DAMSA-at-SNS (7 kW, parasitic) lands within a factor ~4 in coupling floor
  of DAMSA's own 2.5 MW endgame** — 440× less POT costs only ~4.5× in floor
  because zero-background limits scale as POT^(1/4), and the SNS partially
  compensates with energy: 1.3 GeV gives 1.6× the π⁰/POT and a harder photon
  spectrum than 1 GeV.
- It is **orders of magnitude beyond the LESA pathfinder baseline**, which at
  1.5×10¹⁴ EOT only grazes the high-coupling region below ~80 MeV. (LESA's
  8 GeV spectrum eventually wins above ~300 MeV, but only with 10²–10⁴× more
  EOT than baseline.)
- The 100 kW full-train line shows the statistics headroom *if* phase-gated
  running proves clean enough; it is not the baseline claim.

**Why "better": the comparison is not detector vs. detector — it is photon
flux per dollar and timing per dollar.** The detector is identical (and
table-top cheap). The SNS provides (i) a GeV proton source that out-produces
parasitic electron pathfinders by ~10⁴–10⁵ in photon flux at essentially zero
marginal beam cost, (ii) ps-class bunch timing from laser stripping that makes
the zero-background claim *measurable* (per-bunch TOF) rather than assumed,
and (iii) existence: no new MW facility needs to be approved. The one thing
the SNS cannot match is the eventual PIP-II endgame's raw POT and LESA's
8 GeV mass reach — but both are further away in time than a parasitic SNS
installation, and the factor-4 floor gap is small compared to the decade of
unexplored coupling the wedge spans.

## Is the zero-background assumption fair?

Yes — and it is now *checked*, not assumed. The Geant4 flash study exists for
exactly this purpose: the first (bare-dump, 700 ns) run **falsified** the
naive assumption and drove the design to the sparse ns-bunch mode + shield
plug; a second run in the actual DAMSA-at-SNS geometry then **validated** the
final configuration. The budget (`study/geant/README.md`, table at the end):
zero prompt in-gate hits in 10⁵ simulated protons even before the plug; the
inter-bunch "glow" is 11 photons per gate but with a hard nuclear endpoint at
~25 MeV (observed max 23.2 MeV) — below the 30 MeV cluster threshold; the
remaining in-gate populations are neutrinos (invisible) and <1 Michel
positron per gate (charged-vetoed). Expected background:
**≤26 accidental pairs in 5 yr before topology cuts (an MC-statistics upper
limit), ~8×10⁻⁴ events after the fiducial-vertex and mass requirements** —
far below the 2.3-event sensitivity quantum. The load-bearing design items:
30 MeV per-cluster threshold, front-tracker charged veto, ~30 X₀ plug.

## Costing posture

Beam: gated stripping laser on the existing laser-stripping development line
(phase-1 linac station), ~7 kW to a compact dump — no kicker, no new ring
hardware, no high-power target station. Detector: DAMSA-pathfinder-scale
(vacuum tank < 1 m, two tracking planes, ~100 CsI(Tl) crystals + LGAD
readout). Shielding: a ~20 X₀ Pb plug and a modest collar (Geant4-sized in
`study/geant/`). This is a university-group-scale experiment sitting on a
world-class photon source.
