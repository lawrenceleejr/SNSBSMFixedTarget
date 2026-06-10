#!/usr/bin/env python3
"""
"Just put DAMSA here": the DAMSA detector geometry (vacuum decay chamber
30 cm long, 20 cm diameter, immediately behind a compact W dump; CsI(Tl)
4D calorimeter) evaluated with our sensitivity machinery under four beams:

  A. SNS linac station, sparse ns-bunch mode (1 micro-bunch/us, 7.3 kW,
     6.4e20 POT/yr) -- the low-cost, parasitic, true-zero-background option;
  B. SNS linac station, full 402.5 MHz train (100 kW, 9e21 POT/yr) --
     statistics ceiling, background story NOT zero (phase gating only);
  C. DAMSA's own proton endgame: PIP-II/F2D2, 1 GeV, 2.5 MW
     (1.565e16 p/s -> 2.8e23 POT/yr), same zero-background treatment;
  D. DAMSA Path-Finder baseline: SLAC LESA, 8 GeV electrons, 1.5e14 EOT
     (track-length approximation for the shower photon flux).

Everything else (Primakoff cross section, W dump conversion, 2.3-event 90% CL,
30 MeV threshold) is identical across scenarios, so differences are purely
beam + geometry. Detector: L1 = 0.2 m (production point to chamber),
L2 = 0.3 m, aperture r = 0.1 m, eff = 0.5.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

import alp_sensitivity as S

HERE = Path(__file__).parent
rng = np.random.default_rng(7)

GEOM = dict(L1=20.0, L2=30.0, r=10.0)  # cm, DAMSA chamber
SECONDS_YEAR = 5000.0 * 3600.0


def proton_photon_spectrum(T0, Tmax, pi0_per_pot, n_bins=240, e_max=0.85):
    """Photons/POT spectrum from pi0 decay for a given pi0 KE spectrum."""
    T = rng.gamma(2.0, T0, size=6_000_000)
    T = T[T < Tmax][:2_000_000]
    E_pi = T + S.M_PI0
    p_pi = np.sqrt(E_pi**2 - S.M_PI0**2)
    beta, gamma = p_pi / E_pi, E_pi / S.M_PI0
    u = rng.uniform(-1.0, 1.0, size=len(E_pi))
    E_g = 0.5 * S.M_PI0 * gamma * (1.0 + beta * u)
    edges = np.linspace(0.0, e_max, n_bins + 1)
    hist, _ = np.histogram(E_g, bins=edges)
    centers = 0.5 * (edges[1:] + edges[:-1])
    return centers, 2.0 * pi0_per_pot * hist / len(E_pi)


def lesa_photon_spectrum(E0=8.0, n_bins=240):
    """Photons/EOT in a thick W dump from an E0 electron shower,
    track-length approximation: N(>E) ~ 0.572 E0/E."""
    edges = np.geomspace(0.03, E0, n_bins + 1)
    centers = np.sqrt(edges[1:] * edges[:-1])
    n_above = 0.572 * E0 / edges
    return centers, n_above[:-1] - n_above[1:]


def yield_grid(m_grid, g_grid, E, fg, n_primaries, L1, L2, r, eff=0.5):
    geom = r**2 / (4.0 * (L1 + L2) ** 2)
    sel = E > S.E_A_MIN
    E, fg = E[sel], fg[sel]
    sighat = S.sigma_hat_primakoff(E[None, :].repeat(len(m_grid), 0),
                                   m_grid[:, None].repeat(len(E), 1))
    p_a = np.sqrt(np.maximum(E[None, :] ** 2 - m_grid[:, None] ** 2, 1e-30))
    N = np.zeros((len(m_grid), len(g_grid)))
    for j, g in enumerate(g_grid):
        width = g**2 * m_grid**3 / (64.0 * np.pi)
        ctau = S.HBARC_CM / np.maximum(width, 1e-300)
        d = (p_a / m_grid[:, None]) * ctau[:, None]
        p_dec = np.exp(-L1 / d) - np.exp(-(L1 + L2) / d)
        N[:, j] = n_primaries * np.sum(fg[None, :] * sighat * g**2 / S.SIGMA_ABS
                                       * p_dec, axis=1) * geom * eff
    return N


def main():
    m_grid = np.geomspace(3e-4, 0.6, 100)
    g_grid = np.geomspace(1e-9, 3e-2, 260)

    E_sns, f_sns = proton_photon_spectrum(0.080, 0.600, 0.13)
    E_pip, f_pip = proton_photon_spectrum(0.060, 0.350, 0.08)
    E_lesa, f_lesa = lesa_photon_spectrum()

    scenarios = {
        "SNS ns-bunch (7.3 kW), 5 yr":
            (E_sns, f_sns, 6.4e20 * 5, "tab:red", "-"),
        "SNS 100 kW full train, 5 yr (stats only)":
            (E_sns, f_sns, 9.0e21 * 5, "tab:red", "--"),
        "DAMSA endgame: PIP-II 2.5 MW, 5 yr":
            (E_pip, f_pip, 1.565e16 * SECONDS_YEAR * 5, "tab:blue", ":"),
        "DAMSA Path-Finder: LESA 8 GeV, 1.5e14 EOT":
            (E_lesa, f_lesa, 1.5e14, "tab:green", "-."),
    }

    fig, ax = plt.subplots(figsize=(8.2, 6.4))

    def overlay(fname, label, lx, ly):
        dat = np.loadtxt(HERE / "limit_data" / fname)
        ax.fill(dat[:, 0] / 1e6, dat[:, 1], color="0.55", alpha=0.28, lw=0, zorder=1)
        ax.text(lx, ly, label, fontsize=7, color="0.45", zorder=6, alpha=0.85)

    overlay("BeamDump.txt", "E137/E141/CHARM", 0.45, 3e-5)
    overlay("PrimEx.txt", "PrimEx", 100, 2.5e-3)
    overlay("BESIII.txt", "BESIII", 320, 4.5e-4)
    overlay("GlueX.txt", "GlueX", 230, 1.4e-3)
    overlay("FASER.txt", "FASER", 14, 3e-4)
    overlay("OPAL.txt", "OPAL", 30, 1.2e-2)
    overlay("LEP.txt", "LEP", 2.0, 2.5e-3)
    overlay("SN1987A_decay.txt", "SN1987A (decay)", 1.5, 3e-9)
    overlay("SN1987A_HeavyALP_gamma.txt", "SN1987A ($\\gamma$)", 0.5, 1.5e-7)
    overlay("BBN_10MeV.txt", "BBN", 12, 3e-8)

    print(f"{'scenario':45s}  {'floor@100MeV':>12s}  {'ceiling@100MeV':>14s}  {'max mass':>9s}")
    for label, (E, fg, npr, col, ls) in scenarios.items():
        N = yield_grid(m_grid, g_grid, E, fg, npr, **GEOM)
        ax.contour(m_grid * 1e3, g_grid, N.T, levels=[S.N90], colors=[col],
                   linestyles=[ls], linewidths=2, zorder=5)
        ax.plot([], [], ls=ls, color=col, lw=2, label=label)
        i100 = np.argmin(abs(m_grid - 0.1))
        ok = np.where(N[i100] >= S.N90)[0]
        okm = [m_grid[i] for i in range(len(m_grid)) if (N[i] >= S.N90).any()]
        print(f"{label:45s}  "
              f"{g_grid[ok[0]] if len(ok) else float('nan'):12.2e}  "
              f"{g_grid[ok[-1]] if len(ok) else float('nan'):14.2e}  "
              f"{max(okm) * 1e3 if okm else 0:7.0f} MeV")

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.4, 600); ax.set_ylim(1e-9, 3e-2)
    ax.set_xlabel(r"$m_a$  [MeV]")
    ax.set_ylabel(r"$g_{a\gamma\gamma}$  [GeV$^{-1}$]")
    ax.set_title("DAMSA detector (0.3 m chamber @ 0.2 m) under different beams\n"
                 "identical machinery: zero bkg, 2.3 evts, 90% CL; gray = existing limits",
                 fontsize=10.5)
    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.95)
    ax.grid(alpha=0.2, which="both", lw=0.4)
    fig.tight_layout()
    fig.savefig(HERE / "damsa_at_sns.png", dpi=180)
    print("saved", HERE / "damsa_at_sns.png")


if __name__ == "__main__":
    main()
