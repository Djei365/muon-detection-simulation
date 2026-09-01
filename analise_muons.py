import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

# 1. CONFIGURAÇÕES

INPUT_FILE = "build/dados_completos.csv"
OUTPUT_PNG = "muon_spectrum2.png"
OUTPUT_PDF = "muon_spectrum2.pdf"

Z_MIN  = 200.0    # mm  — só eventos que cruzam o detector
P_MIN  = 0.9      # GeV/c — limite inferior dos bins
P_MAX  = 1500.0   # GeV/c — limite superior dos bins
N_BINS = 22       # número de bins logarítmicos

# Faixas de ângulo zenital [graus] e faixa de normalização [GeV/c]
PANELS = [
    # (label, zmin, zmax, norm_pmin, norm_pmax)
    ("A",  0.0,  30.0,  5.0, 20.0),   # próximo da vertical
    ("B", 30.0,  60.0,  3.0, 15.0),   # intermediário
    ("C", 60.0,  90.0,  2.0, 10.0),   # próximo da horizontal
]

# 2. MODELOS TEÓRICOS  — fluxo em (cm² s sr GeV/c)⁻¹

def gaisser_tang(p, theta):
    """Gaisser-Tang (2002) — usado internamente para normalização."""
    ct = np.cos(theta)
    ct_eff = np.sqrt(ct**2
                     + 0.102573**2
                     - 0.068287 * ct**0.958633
                     + 0.0407253 * ct**0.817285)
    return (0.14 * p**(-2.7)
            * (1.0 / (1 + 1.1*p*ct_eff/115.0)
               + 0.054 / (1 + 1.1*p*ct_eff/850.0)))

# 3. LEITURA DOS DADOS

def parse_data(filepath):
    """Extrai (p, zenith) de cada linha G4WTx do CSV do Geant4."""
    p_list, zenith_list = [], []
    with open(filepath) as f:
        for line in f:
            if not line.startswith("G4WT"):
                continue
            try:
                vals  = line.split("> ")[1].strip().split(",")
                z     = float(vals[0])
                p     = float(vals[1])
                theta = float(vals[2])
            except Exception:
                continue
            if z > Z_MIN and p > 0:
                p_list.append(p)
                zenith_list.append(np.pi - theta)   # ângulo zenital em rad
    return np.array(p_list), np.array(zenith_list)

# 4. BINAGEM E CÁLCULO DO FLUXO

def compute_flux(p_sim, zenith_sim, zmin_deg, zmax_deg,
                 p_bins, norm_pmin, norm_pmax):
    """
    Converte contagens simuladas em fluxo diferencial.

    Phi(p) = dN / (dp · A·T · dΩ)

    O fator A·T é estimado igualando as contagens ao modelo Gaisser-Tang
    na faixa [norm_pmin, norm_pmax] GeV/c.
    Se souber A (cm²) e T (s) do código C++, substitua AT diretamente.
    """
    zd   = np.degrees(zenith_sim)
    mask = (zd >= zmin_deg) & (zd < zmax_deg)

    theta_mean = float(np.mean(zenith_sim[mask]))
    dOmega     = 2.0 * np.pi * (np.cos(np.radians(zmin_deg))
                                 - np.cos(np.radians(zmax_deg)))

    count, _ = np.histogram(p_sim[mask], bins=p_bins)
    bc = np.sqrt(p_bins[:-1] * p_bins[1:])   # centro geométrico de cada bin
    bw = np.diff(p_bins)

    # Ajuste de normalização
    m_norm   = (bc >= norm_pmin) & (bc <= norm_pmax)
    expected = gaisser_tang(bc[m_norm], theta_mean) * dOmega * bw[m_norm]
    AT       = float(np.sum(count[m_norm]) / np.sum(expected))

    denom = AT * dOmega * bw
    flux  = np.where(count > 0, count / denom, 0.0)
    ferr  = np.where(count > 0, np.sqrt(count) / denom, 0.0)

    return bc, flux, ferr, count, theta_mean

# 5. PLOTAGEM

def draw_panel(ax, label, zmin, zmax, bc, flux, ferr, count):
    ax.set_xscale("log")
    ax.set_yscale("log")

    m = count > 0
    ax.errorbar(bc[m], flux[m], yerr=ferr[m],
                fmt="o", color="red", markeredgecolor="darkred",
                ms=4.5, elinewidth=0.9, capsize=2,
                label="Simulação (CRY)", zorder=5)

    ax.set_xlim(1, 1000)
    ax.set_ylim(1e-11, 1e-1)
    ax.set_xlabel(r"$p$ /(GeV/c)", fontsize=12)
    ax.set_ylabel(
        r"$\Phi(p,\theta)$/(GeV/c)$^{-1}\!\cdot$cm$^{-2}\!\cdot$sr$^{-1}\!\cdot$s$^{-1}$",
        fontsize=10)

    # Label do painel + faixa angular
    ax.text(0.03, 0.97, label, transform=ax.transAxes,
            fontsize=15, fontweight="bold", va="top")
    ax.text(0.97, 0.97, rf"$\theta$ = {zmin:.0f}°–{zmax:.0f}°",
            transform=ax.transAxes, fontsize=9,
            va="top", ha="right", color="0.35")

    ax.grid(True, which="major", alpha=0.25, linestyle=":", lw=0.6)
    ax.grid(True, which="minor", alpha=0.10, linestyle=":", lw=0.4)
    ax.tick_params(which="both", direction="in", top=True, right=True)
    ax.xaxis.set_minor_locator(LogLocator(subs=np.arange(2, 10) * 0.1))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_locator(LogLocator(subs=np.arange(2, 10) * 0.1))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.legend(fontsize=8.5, loc="lower left", framealpha=0.85, edgecolor="0.7")


def main():
    # --- Leitura ---
    print(f"Lendo {INPUT_FILE} ...")
    p_sim, zenith_sim = parse_data(INPUT_FILE)
    print(f"  {len(p_sim)} eventos válidos | "
          f"p = [{p_sim.min():.2f}, {p_sim.max():.1f}] GeV/c")

    # --- Bins ---
    p_bins = np.logspace(np.log10(P_MIN), np.log10(P_MAX), N_BINS)

    # --- Figura: 3 painéis empilhados ---
    plt.rcParams.update({"font.family": "serif", "font.size": 11,
                         "axes.linewidth": 0.8})
    fig, axes = plt.subplots(3, 1, figsize=(7.0, 15.0),
                             dpi=120, facecolor="white")

    for ax, (label, zmin, zmax, np_min, np_max) in zip(axes, PANELS):
        bc, flux, ferr, count, theta_mean = compute_flux(
            p_sim, zenith_sim, zmin, zmax, p_bins, np_min, np_max)
        print(f"Painel {label} ({zmin:.0f}°–{zmax:.0f}°): "
              f"{count.sum()} eventos | ⟨θ⟩ = {np.degrees(theta_mean):.1f}°")
        draw_panel(ax, label, zmin, zmax, bc, flux, ferr, count)

    plt.tight_layout(h_pad=3.0)

    for fname in (OUTPUT_PNG, OUTPUT_PDF):
        plt.savefig(fname, dpi=300, bbox_inches="tight")
        print(f"Salvo → {fname}")
    plt.close()


if __name__ == "__main__":
    main()