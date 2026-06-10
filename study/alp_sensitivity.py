#!/usr/bin/env python3
"""
ALP (a -> gamma gamma) sensitivity study for an SNS BSM fixed-target station.

Benchmark: the "option 2b" beam from the workshop slide -- 1.3 GeV protons,
accumulated ~1 us pulses at ~6 Hz, up to 300 kW on a dedicated tungsten dump
(duty factor 6e-6) -- with a DAMSA-style near detector: an evacuated decay
volume starting 15 m from the dump, 3 m long, read out by a photon
calorimeter of 1 m radius.

Signal chain:
  p (1.3 GeV) + W -> pi0 -> gamma gamma          (photon source in the dump)
  gamma + W(Z=74) -> a + W   (Primakoff)         (P_conv = sigma_P / sigma_abs)
  a -> gamma gamma in the decay volume           (exp(-L1/d) - exp(-(L1+L2)/d))

Background is assumed to be zero in the beam-prompt window, justified by the
6e-6 duty factor, neutron time-of-flight rejection over 15+ m, and the vacuum
decay volume; the 90% CL sensitivity is then N_sig = 2.3 events.

Conservative simplifications (all err toward weaker sensitivity):
  - only pi0 decay photons are used (EM shower photons ignored);
  - isotropic pi0 emission; ALP takes the parent photon direction;
  - flat 50% reconstruction efficiency for the diphoton final state.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

rng = np.random.default_rng(20260610)
HERE = Path(__file__).parent

# ----------------------------------------------------------------------
# Constants (natural units, GeV; lengths converted where needed)
# ----------------------------------------------------------------------
HBARC_CM = 1.9733e-14        # GeV*cm
GEV2_TO_CM2 = 3.8938e-28     # (1/GeV^2) in cm^2
ALPHA_EM = 1.0 / 137.036
M_E = 0.511e-3               # GeV
FM_TO_INV_GEV = 5.0677       # 1 fm in GeV^-1

# Tungsten target/dump
Z_W, A_W = 74, 183.84
X0_W_CM = 0.3504             # radiation length of W in cm
LAMBDA_GAMMA_CM = (9.0 / 7.0) * X0_W_CM      # photon attenuation length (pair-prod. dominated)
N_W = 19.30 * 6.02214e23 / A_W               # atoms / cm^3
SIGMA_ABS = 1.0 / (N_W * LAMBDA_GAMMA_CM)    # effective photon absorption cross section, cm^2

# ----------------------------------------------------------------------
# Beam / source assumptions
# ----------------------------------------------------------------------
E_PROTON = 1.3               # GeV kinetic
POWER_W = 300e3              # W
SECONDS_YEAR = 5000.0 * 3600.0
POT_PER_SEC = POWER_W / (E_PROTON * 1.602e-10)
POT_YEAR = POT_PER_SEC * SECONDS_YEAR        # ~2.6e22
PI0_PER_POT = 0.13           # ~ pi+ yield at 1.3 GeV (COHERENT/STS flux papers)
T0_PI0 = 0.080               # GeV; dN/dT ~ T exp(-T/T0), DAR-regime spectrum
T_MAX_PI0 = 0.600            # GeV kinematic-ish cutoff
M_PI0 = 0.1350

# Detector configurations: (L1, L2, r_detector) in cm.
#  "near": DAMSA-style -- compact W dump with an evacuated decay chamber starting
#          0.3 m downstream of the production point; this is what reaches the
#          short-lifetime (high-coupling, high-mass) gap above old beam dumps.
#  "far":  CCM-style hall at 15 m, where the 6e-6 duty factor plus neutron
#          time-of-flight make the zero-background assumption robust.
CONFIGS = {
    "near": dict(L1=30.0, L2=300.0, r=50.0),
    "far": dict(L1=1500.0, L2=300.0, r=100.0),
}
EFF = 0.5                    # diphoton reconstruction efficiency
E_A_MIN = 0.030              # GeV analysis threshold on ALP energy
N90 = 2.3                    # 90% CL signal for zero background

# ----------------------------------------------------------------------
# Photon spectrum from pi0 decay (Monte Carlo)
# ----------------------------------------------------------------------
def photon_spectrum(n_mc=2_000_000, n_bins=240):
    """Photon energy histogram (per pi0) from isotropic pi0 with
    dN/dT ~ T exp(-T/T0) truncated at T_MAX_PI0."""
    T = rng.gamma(2.0, T0_PI0, size=3 * n_mc)
    T = T[T < T_MAX_PI0][:n_mc]
    E_pi = T + M_PI0
    p_pi = np.sqrt(E_pi**2 - M_PI0**2)
    beta, gamma = p_pi / E_pi, E_pi / M_PI0
    # isotropic decay: photon energy flat in [gamma(1-beta), gamma(1+beta)] * m/2
    u = rng.uniform(-1.0, 1.0, size=len(E_pi))
    E_g = 0.5 * M_PI0 * gamma * (1.0 + beta * u)
    edges = np.linspace(0.0, 0.75, n_bins + 1)
    hist, _ = np.histogram(E_g, bins=edges)
    centers = 0.5 * (edges[1:] + edges[:-1])
    # 2 photons per pi0
    weights = 2.0 * hist / len(E_pi)
    return centers, weights

# ----------------------------------------------------------------------
# Primakoff cross section, sigma_P = g^2 * sigma_hat(E, m)
# dsigma/dcos = (1/4) g^2 alpha Z^2 F(t)^2 p_a^4 sin^2(theta) / t^2
# ----------------------------------------------------------------------
def helm_ff(q):
    """Helm nuclear form factor; q in GeV."""
    s = 0.9 * FM_TO_INV_GEV
    c = (1.23 * A_W ** (1.0 / 3.0) - 0.60) * FM_TO_INV_GEV
    a = 0.52 * FM_TO_INV_GEV
    R1 = np.sqrt(np.maximum(c**2 + (7.0 / 3.0) * np.pi**2 * a**2 - 5.0 * s**2, 1e-12))
    x = np.maximum(q * R1, 1e-8)
    j1 = (np.sin(x) - x * np.cos(x)) / x**2
    return 3.0 * j1 / x * np.exp(-0.5 * (q * s) ** 2)

def atomic_screening(q):
    """Tsai atomic screening: suppresses coherence at q below inverse atomic radius."""
    a_atom = 111.0 * Z_W ** (-1.0 / 3.0) / M_E
    x = (a_atom * q) ** 2
    return x / (1.0 + x)

def sigma_hat_primakoff(E, m):
    """sigma_P / g^2 in cm^2 * GeV^2 units (multiply by g[GeV^-1]^2 -> cm^2).
    E, m broadcastable arrays [GeV]."""
    E = np.asarray(E)[..., None]          # add theta axis
    m = np.asarray(m)[..., None]
    p = np.sqrt(np.maximum(E**2 - m**2, 0.0))
    u = np.geomspace(1e-12, 2.0, 400)     # u = 1 - cos(theta)
    cos = 1.0 - u
    sin2 = np.clip(1.0 - cos**2, 0.0, 1.0)
    t = m**2 - 2.0 * E * (E - p * cos)    # t < 0
    q = np.sqrt(np.maximum(-t, 1e-30))
    ff2 = (helm_ff(q) * atomic_screening(q)) ** 2
    dsig = 0.25 * ALPHA_EM * Z_W**2 * ff2 * p**4 * sin2 / t**2
    sig = np.trapezoid(dsig, u, axis=-1)
    return np.where(E[..., 0] > m[..., 0], sig, 0.0) * GEV2_TO_CM2

# ----------------------------------------------------------------------
# Decay length and signal yield
# ----------------------------------------------------------------------
def signal_yield(m_grid, g_grid, E_bins, f_gamma, pot, L1, L2, r):
    """N_sig on (m, g) grid for a given geometry. f_gamma: photons/pi0 per E bin."""
    geom = r**2 / (4.0 * (L1 + L2) ** 2)  # dOmega/4pi for ~isotropic point source
    sel = E_bins > E_A_MIN
    E = E_bins[sel]
    fg = f_gamma[sel] * PI0_PER_POT  # photons/POT (f_gamma is per pi0, incl. the factor 2)
    sighat = sigma_hat_primakoff(E[None, :].repeat(len(m_grid), 0),
                                 m_grid[:, None].repeat(len(E), 1))  # (m, E)
    p_a = np.sqrt(np.maximum(E[None, :] ** 2 - m_grid[:, None] ** 2, 1e-30))
    N = np.zeros((len(m_grid), len(g_grid)))
    for j, g in enumerate(g_grid):
        gamma_width = g**2 * m_grid**3 / (64.0 * np.pi)          # GeV
        ctau_cm = HBARC_CM / np.maximum(gamma_width, 1e-300)
        d = (p_a / m_grid[:, None]) * ctau_cm[:, None]           # lab decay length (m, E)
        p_dec = np.exp(-L1 / d) - np.exp(-(L1 + L2) / d)
        p_conv = sighat * g**2 / SIGMA_ABS
        N[:, j] = pot * np.sum(fg[None, :] * p_conv * p_dec, axis=1) * geom * EFF
    return N

# ----------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------
def main():
    E_bins, f_gamma = photon_spectrum()
    n_gamma_pot = PI0_PER_POT * f_gamma.sum()
    print(f"POT/yr = {POT_YEAR:.2e}, photons/POT = {n_gamma_pot:.3f}, "
          f"sigma_abs = {SIGMA_ABS/1e-24:.1f} b")

    m_grid = np.geomspace(3e-4, 0.45, 90)        # GeV
    g_grid = np.geomspace(1e-9, 3e-2, 260)       # GeV^-1

    results = {}
    for cfg, years in [("near", 1.0), ("near", 5.0), ("far", 5.0)]:
        key = f"{cfg} {years:.0f} yr"
        N = signal_yield(m_grid, g_grid, E_bins, f_gamma, POT_YEAR * years,
                         **CONFIGS[cfg])
        results[key] = N
        print(f"{key}: max N_sig = {N.max():.3g}")

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.2, 6.4))
    from matplotlib.path import Path as MplPath

    excluded_polys = []

    def overlay(fname, color, label, lx, ly):
        dat = np.loadtxt(HERE / "limit_data" / fname)
        m_mev, g = dat[:, 0] / 1e6, dat[:, 1]
        excluded_polys.append(np.column_stack([np.log10(m_mev), np.log10(g)]))
        ax.fill(m_mev, g, color=color, alpha=0.30, lw=0, zorder=1)
        ax.plot(m_mev, g, color=color, alpha=0.6, lw=0.7, zorder=1)
        ax.text(lx, ly, label, fontsize=8.5, color="0.25", zorder=6)

    overlay("BeamDump.txt", "0.45", "E137/E141/CHARM", 0.45, 3e-5)
    overlay("PrimEx.txt", "tab:olive", "PrimEx", 85, 2.5e-3)
    overlay("BESIII.txt", "tab:cyan", "BESIII", 300, 4.5e-4)
    overlay("GlueX.txt", "tab:purple", "GlueX", 215, 1.5e-3)
    overlay("FASER.txt", "tab:green", "FASER", 14, 4e-4)
    overlay("OPAL.txt", "tab:pink", "OPAL", 30, 1e-2)
    overlay("LEP.txt", "thistle", "LEP", 2.5, 2.5e-3)
    overlay("SN1987A_decay.txt", "tab:blue", "SN1987A (decay)", 1.5, 2e-9)
    overlay("SN1987A_HeavyALP_gamma.txt", "steelblue", "SN1987A ($\\gamma$)", 0.5, 1.5e-7)
    overlay("BBN_10MeV.txt", "tab:brown", "BBN", 12, 3e-8)

    mg = m_grid * 1e3
    styles = {
        "near 1 yr": ("--", "tab:red"),
        "near 5 yr": ("-", "tab:red"),
        "far 5 yr": (":", "darkorange"),
    }
    names = {
        "near 1 yr": "near chamber (0.3 m), 1 yr",
        "near 5 yr": "near chamber (0.3 m), 5 yr",
        "far 5 yr": "far hall (15 m), 5 yr",
    }
    for key, (ls, col) in styles.items():
        ax.contour(mg, g_grid, results[key].T, levels=[N90],
                   colors=[col], linestyles=[ls], linewidths=2, zorder=5)
        ax.plot([], [], ls=ls, color=col, lw=2,
                label=f"SNS 300 kW dump, {names[key]}, 90% CL")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.4, 450)
    ax.set_ylim(1e-9, 3e-2)
    ax.set_xlabel(r"$m_a$  [MeV]")
    ax.set_ylabel(r"$g_{a\gamma\gamma}$  [GeV$^{-1}$]")
    ax.set_title("ALP $\\to\\gamma\\gamma$ at an SNS fixed-target station\n"
                 "1.3 GeV, 300 kW (1 $\\mu$s @ 6 Hz, duty $6\\times10^{-6}$), "
                 "3 m vacuum decay volume",
                 fontsize=10.5)
    # shade the part of the 5 yr near-chamber reach not excluded by anything shown
    MM, GG = np.meshgrid(mg, g_grid, indexing="ij")
    pts = np.column_stack([np.log10(MM.ravel()), np.log10(GG.ravel())])
    excl = np.zeros(len(pts), dtype=bool)
    for poly in excluded_polys:
        excl |= MplPath(poly).contains_points(pts)
    new_space = (results["near 5 yr"] >= N90) & ~excl.reshape(MM.shape)
    ax.contourf(mg, g_grid, new_space.T.astype(float), levels=[0.5, 1.5],
                colors=["tab:red"], alpha=0.35, zorder=2)
    ax.fill([], [], color="tab:red", alpha=0.35,
            label="newly probed parameter space (near, 5 yr)")

    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.95)
    ax.grid(alpha=0.2, which="both", lw=0.4)
    fig.tight_layout()
    out = HERE / "alp_limit_plot.png"
    fig.savefig(out, dpi=180)
    print(f"saved {out}")

if __name__ == "__main__":
    main()
