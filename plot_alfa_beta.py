import re
import numpy as np
import matplotlib.pyplot as plt
import sys

try:
    from scipy.interpolate import make_interp_spline
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("ATTENZIONE: SciPy non è installato. Il grafico smooth userà un'interpolazione lineare.")

filepath=r'C:\Users\scapp\OneDrive\Documenti\hypergraphs\hyperedges-datascience-stackexchange-tags.txt'
#hyperedges-amazon-reviews.txt
#hyperedges-stackoverflow-answers
#hyperedges-google
#hyperedges-wikipedia-pages
#hyperedges-mathoverflow-answers
#hyperedges-cpc-group-2024-2025.txt
#hyperedges-datascience-stackexchange-tags.txt <- splittare sugli spazi, non sulle virgole
def load_hypergraph_from_text(filepath):
    """
    Legge un ipergrafo da un file di testo.

    Formato:
      - Ogni riga = un iperarco.
      - I vertici sono separati da spazi e/o virgole.
      - Le righe vuote o che iniziano con '#' sono ignorate.

    Ritorna:
      hyperedges: lista di iperarchi, ciascuno come insieme di vertici (stringhe).
    """
    hyperedges = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # separa per spazi o virgole
            tokens = re.split(r"[,\s ]+", line)
            # rimuovi eventuali stringhe vuote
            tokens = [t for t in tokens if t]
            if tokens:
                hyperedges.append(set(tokens))
    if not hyperedges:
        raise ValueError("Nessun iperarco valido trovato nel file.")
    return hyperedges


def compute_alpha_beta(hyperedges, rank):
    """
    hyperedges: lista di iperarchi, ciascuno rappresentato come iterabile di vertici
    Ritorna:
        alphas: array degli alpha
        betas:  array dei corrispondenti beta
    """
    sizes = []
#    rank = 0
#    for e in hyperedges:
#        sizes.append(e)
#        if len(e) > rank:
#            rank = len(e)

    alphas = []
    betas = []

    for alpha in range(1, rank + 1):
        new_sizes = []
        for e in hyperedges:
            if len(e) > alpha:
                new_sizes.append(e)
                
        hyperedges = new_sizes
        alphas.append(alpha)
        betas.append(len(hyperedges))

    return np.array(alphas), np.array(betas)\




def plot_alpha_beta(alphas, betas, alpha_mark=None):
    # Primo grafico: punti (alpha, beta) senza interpolazione
    #plt.figure()
    #plt.plot(alphas, betas, marker=".", linestyle="none")
    #plt.xlabel(r"$\alpha$")
    #plt.ylabel(r"$\beta(\alpha)$")
    #plt.title("(Alpha, Beta) pairs")

    # Se l'utente vuole marcare un alfa specifico
    if alpha_mark is not None:
        # Interpola beta in quel punto
        beta_mark = np.interp(alpha_mark, alphas, betas)

        # Disegna una barra verticale tratteggiata
        plt.vlines(
            alpha_mark,
            ymin=0,
            ymax=beta_mark,
            color="red",
            linestyle="--",
            linewidth=1.5,
        )

        plt.hlines(
            beta_mark,
            xmin=0,
            xmax=alpha_mark,
            color="green",
            linestyle="--",
            linewidth=1.5,
        )

        # Punto di intersezione
        plt.plot(alpha_mark, beta_mark, 'ro')

    plt.grid(True)

    plt.figure()
    alphas = np.asarray(alphas)
    betas = np.asarray(betas)

    # Ordiniamo per sicurezza (la spline vuole x crescente)
    sort_idx = np.argsort(alphas)
    alphas_sorted = alphas[sort_idx]
    betas_sorted = betas[sort_idx]

    # Costruiamo una griglia fine di alpha per la curva smooth
    alpha_smooth = np.linspace(alphas_sorted.min(), alphas_sorted.max(), 1000)

    # Spline cubica MOLTO smooth (interpolante, non di fitting)
    spline = make_interp_spline(alphas_sorted, betas_sorted, k=3)
    beta_smooth = spline(alpha_smooth)

    plt.figure()

    # Punti originali
    plt.plot(alphas, betas, ".", label="Dati")

    # Curva smooth
    plt.plot(alpha_smooth, beta_smooth, label="Interpolazione smooth")
    
    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def plot_alpha_beta_smooth(alphas, betas, alpha_mark=None):
    alphas = np.asarray(alphas)
    betas = np.asarray(betas)

    # Ordiniamo i dati
    sort_idx = np.argsort(alphas)
    alphas_sorted = alphas[sort_idx]
    betas_sorted = betas[sort_idx]

    # Spline smooth
    alpha_smooth = np.linspace(alphas_sorted.min(), alphas_sorted.max(), 1000)
    spline = make_interp_spline(alphas_sorted, betas_sorted, k=3)
    beta_smooth = spline(alpha_smooth)

    fig, ax = plt.subplots()

    # Curva smooth
    ax.plot(alpha_smooth, beta_smooth)

    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel(r"$\beta(\alpha)$")
    ax.set_title(r"Plot of ($\alpha, \beta$) pairs for SE")

    # Assicuriamoci che 0 sia visibile su entrambi gli assi
    x_min, x_max = alpha_smooth.min(), alpha_smooth.max()
    y_min, y_max = beta_smooth.min(), beta_smooth.max()

    x_min = min(x_min, 0)
    x_max = max(x_max, 0)
    y_min = min(y_min, 0)
    y_max = max(y_max, 0)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Spostiamo le spines in modo che si incrocino in (0,0)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")

    # Nascondiamo le spines in alto e a destra
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    # Mettiamo i ticks solo sugli assi che ci interessano
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    if alpha_mark is not None:
        alpha_mark_clipped = np.clip(alpha_mark, alphas_sorted.min(), alphas_sorted.max())
        beta_mark = float(spline(alpha_mark_clipped))

        # Barra verticale (rossa) da 0 a beta_mark
        ax.vlines(alpha_mark_clipped, 0, beta_mark,
                  colors="red", linestyles="--", linewidth=1.5)

        # Barra orizzontale (verde) da 0 a alpha_mark
        ax.hlines(beta_mark, 0, alpha_mark_clipped,
                  colors="green", linestyles="--", linewidth=1.5)

        # Punto di intersezione
        ax.plot(alpha_mark_clipped, beta_mark, "ro")

        # Etichetta α* sull'asse x (ora che passa per y=0)
        ax.text(alpha_mark_clipped, 0,
                r"$\alpha^{*}$",
                color="red", ha="center", va="top", fontsize=12)

        # Etichetta β(α*) sull'asse y (ora che passa per x=0)
        ax.text(0, beta_mark,
                r"$\beta(\alpha^{*})$",
                color="green", ha="right", va="center", fontsize=12)

    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    plt.show()
if __name__ == "__main__":
    hypergraph = load_hypergraph_from_text(filepath)

    alphas, betas = compute_alpha_beta(hypergraph, 11391)
    print("alpha:", alphas)
    print("beta :", betas)

    plot_alpha_beta_smooth(alphas, betas, 400)
    #plot_alpha_beta(alphas[:50000], betas[:50000])
