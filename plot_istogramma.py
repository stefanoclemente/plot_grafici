import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from pathlib import Path
from itertools import product
from matplotlib.ticker import ScalarFormatter

#Colonne rilevanti
COLUMNS=['size', 'type', 'walltime']
COLUMNS_H=['size', 'step', 'walltime']
kappa=list(range(3,6))
core=['8', '16', '32']
personal_path1=r"C:\Users\scapp\Downloads\mathoverflow"
personal_path2=r"C:\Users\scapp\Downloads\mathoverflow"

def load_table(path: str) -> pd.DataFrame:
    """
    Load a comma-separated CSV into a pandas DataFrame (table).
    """
    path = Path(path)
    df = pd.read_csv(path)  
    return df

def select_columns(df: pd.DataFrame, columns=COLUMNS) -> pd.DataFrame:
    """
    Return only the requested columns (preserving order).
    """
    return df.loc[:, columns]


def times_by_k(df: pd.DataFrame):

    return df.groupby("size")["walltime"].sum().reset_index()


def times_total(df: pd.DataFrame):

    return df["walltime"].sum()

def compute_aggregate_times(df: pd.DataFrame, name: str):
    #Divido g in 7 liste (una per core) da 6
    data = [df[i:i + 6] for i in range(0, len(df), 6)]
    data = [[int(el) for el in lista] for lista in data]

    n_groups = len(data)     # 7
    n_levels = len(data[0])  # 6

    x = np.arange(n_groups)

    # Colori distinti per ogni livello
    colors = cm.plasma(np.linspace(0.1, 0.9, n_levels))

    fig, ax = plt.subplots(figsize=(8,5))
    bar_width = 0.6

    # Disegniamo DAL PIÙ PICCOLO al PIÙ GRANDE → quello grande dietro
    for j in range(n_levels):
        heights = [lst[j] for lst in data]
        ax.bar(
            x,
            heights,
            width=bar_width,
            color=colors[j],
            alpha=0.8 - 0.6 * (j / n_levels),  # più grande = leggermente più trasparente
            edgecolor='black',
            linewidth=0.5,
            zorder=10-j,  # piccolo davanti
            label=f"Tempo {j+1}"
        )

    # Etichette

    ax.set_xlabel("")
    ax.set_ylabel("Aggregate times (in sec)")
    ax.set_title(name)
    ax.set_xticks(x)
    ax.set_xticklabels([f'1 Core'] + [f'{i} Cores' for i in core[1::]])
    ax.legend(title="Max graphlet size")

    plt.tight_layout()


def plot_pairs_aligned(coppie, etichette=None, show_values=False):
    """
    coppie: lista di tuple (gaifman_normale, hypermotivo), es. [(g1,h1), (g2,h2), ...]
    etichette: etichette sull'asse X, una per coppia
    show_values: True per mostrare il valore numerico sopra ogni barra
    """
    gaifman = [g for g, h in coppie]      # sinistra (blu)
    hyper   = [h for g, h in coppie]      # destra (rosso)

    n = len(coppie)
    if etichette is None:
        etichette = ['MA', 'SA', 'AR', 'RM', 'GP', 'SE']

    bar_width = 0.38       # larghezza singola barra
    pair_gap  = 0.75       # distanza tra coppie (tra i centri delle barre sinistre successive)

    # posizioni: x di sinistra e destra (x è il CENTRO della barra in matplotlib)
    x_left, x_right, x_ticks = [], [], []
    for i in range(n):
        xl = i * (2*bar_width + pair_gap)   # centro barra sinistra
        xr = xl + bar_width                 # centro barra destra (adiacente)
        x_left.append(xl)
        x_right.append(xr)
        x_ticks.append((xl + xr) / 2)       # centro della coppia

    fig, ax = plt.subplots(figsize=(9, 5))

    # barre: sinistra blu (gaifman), destra rossa (hypermotivo)
    ax.bar(x_left,  gaifman, width=bar_width, color='blue',
           edgecolor='black', linewidth=1.2, label='Gaifman + Motivo')
    ax.bar(x_right, hyper,   width=bar_width, color='red',
           edgecolor='black', linewidth=1.2, label=' HyperMotivo')

    # etichette X centrate sulla coppia
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(etichette)

    # opzionale: valore numerico sopra ogni barra
    if show_values:
        for x, y in zip(x_left, gaifman):
            ax.text(x, y, f"{y:.2f}", ha='center', va='bottom')
        for x, y in zip(x_right, hyper):
            ax.text(x, y, f"{y:.2f}", ha='center', va='bottom')

    ax.set_ylabel("Time (s)")
    ax.set_title("Comparison of build-up runtime")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.35)

    plt.tight_layout()
    plt.show()


def plot_pairs_aligned1(coppie, etichette=None, show_values=False):
    """
    coppie: lista di tuple (gaifman_normale, hypermotivo), es. [(g1,h1), (g2,h2), ...]
    etichette: etichette sull'asse X, una per coppia
    show_values: True per mostrare il valore numerico sopra ogni barra
    """
    motivo = [g for g, h in coppie]      # sinistra (blu)
    hyper   = [h for g, h in coppie]      # destra (rosso)

    n = len(coppie)
    if etichette is None:
        etichette = ['MA', 'SA', 'AR', 'WI', 'GP', 'SE']

    bar_width = 0.38       # larghezza singola barra
    pair_gap  = 0.75       # distanza tra coppie (tra i centri delle barre sinistre successive)

    # posizioni: x di sinistra e destra (x è il CENTRO della barra in matplotlib)
    x_left, x_right, x_ticks = [], [], []
    for i in range(n):
        xl = i * (2*bar_width + pair_gap)   # centro barra sinistra
        xr = xl + bar_width                 # centro barra destra (adiacente)
        x_left.append(xl)
        x_right.append(xr)
        x_ticks.append((xl + xr) / 2)       # centro della coppia

    fig, ax = plt.subplots(figsize=(9, 5))

    # barre: sinistra blu (gaifman), destra rossa (hypermotivo)
    ax.bar(x_left,  motivo, width=bar_width, color='yellow',
           edgecolor='black', linewidth=1.2, label='Gaifman + Motivo')
    ax.bar(x_right, hyper,   width=bar_width, color='green',
           edgecolor='black', linewidth=1.2, label='HyperMotivo')

    # etichette X centrate sulla coppia
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(etichette)

    # opzionale: valore numerico sopra ogni barra
    if show_values:
        for x, y in zip(x_left, motivo):
            ax.text(x, y, f"{y:.2f}", ha='center', va='bottom')
        for x, y in zip(x_right, hyper):
            ax.text(x, y, f"{y:.2f}", ha='center', va='bottom')

    ax.set_ylabel("GB")
    ax.set_title("Use of memory")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.35)

    plt.tight_layout()
    plt.show()

def compute_projection_times(df: pd.DataFrame):
    sp = df[df['stage'].str.contains('split', na=False)]
    split = sp[sp['variant'].str.contains('orig', na=False)].iloc[0]['walltime']
    lw = df[df['stage'].str.contains('gaifman_low', na=False)]
    low = lw[lw['variant'].str.contains('orig', na=False)].iloc[0]['walltime']
    fl = df[df['stage'].str.contains('gaifman_full', na=False)]
    full = fl[fl['variant'].str.contains('orig', na=False)].iloc[0]['walltime']

    return full, split+low
    

    
if __name__=='__main__':



# Mathoverflow
# aggrego per k
# sommo 
    a = select_columns(load_table(r""+personal_path2+r"\hyperedges-mathoverflow-answers_gaifman_K8_T8_S1000000.csv"))
    a = a[~a['type'].str.contains('sample', na=False)]
    a = times_total(times_by_k(a))
    b = select_columns(load_table(r""+personal_path2+r"\hyperedges-mathoverflow-answers_hyper_K8_T8_S1000000.csv"), COLUMNS_H)
    b = b[~b['step'].str.contains('sample', na=False)]
    b = times_total(times_by_k(b))
# Stackoverflow (manca il tempo di proiezione)
    m = select_columns(load_table(r""+personal_path1+r"\hyperedges-stackoverflow-answers_gaifman_K5_T8_S100000.csv"))
    m = m[~m['type'].str.contains('sample', na=False)]
    m = times_total(times_by_k(m))
    o = select_columns(load_table(r""+personal_path1+r"\hyperedges-stackoverflow-answers_hyper_K5_T8_S100000.csv"), COLUMNS_H)
    o = o[~o['step'].str.contains('sample', na=False)]
    o = times_total(times_by_k(o))
    tempi_pz = load_table(r""+personal_path1+r"\hyperedges-stackoverflow-answers_preproc.csv")
    tempo_full, tempo_low = compute_projection_times(tempi_pz)
    print(m, o)
    m += tempo_full
    o += tempo_low
    print(m, o)
# Amazon (manca il tempo di proiezione)
    l = select_columns(load_table(r""+personal_path1+r"\hyperedges-amazon-reviews_gaifman_K6_T16_S100000.csv"))
    l = l[~l['type'].str.contains('sample', na=False)]
    l = times_total(times_by_k(l))
    n = select_columns(load_table(r""+personal_path1+r"\hyperedges-amazon-reviews_hyper_K6_T16_S100000.csv"), COLUMNS_H)
    n = n[~n['step'].str.contains('sample', na=False)]
    n = times_total(times_by_k(n))
    tempi_pz1 = load_table(r""+personal_path1+r"\hyperedges-amazon-reviews_preproc.csv")
    tempo_full1, tempo_low1 = compute_projection_times(tempi_pz1)
    l = float(l) + float(tempo_full1)
    n = float(n) + float(tempo_low1)
# RE

# GP
    g = select_columns(load_table(r""+personal_path1+r"\hyperedges-cpc-group-2024-2025_gaifman_K5_T8_S100000.csv"))
    g = g[~g['type'].str.contains('sample', na=False)]
    g = times_total(times_by_k(g))
    p = select_columns(load_table(r""+personal_path1+r"\hyperedges-cpc-group-2024-2025_hyper_K5_T8_S100000.csv"), COLUMNS_H)
    p = p[~p['step'].str.contains('sample', na=False)]
    p = times_total(times_by_k(p))
    tempi_pz2 = load_table(r""+personal_path1+r"\hyperedges-cpc-group-2024-2025_preproc.csv")
    tempo_full2, tempo_low2 = compute_projection_times(tempi_pz2)
    g = float(g) + float(tempo_full2)
    p = float(p) + float(tempo_low2)
# SE (manca il tempo di proiezione)
    w = select_columns(load_table(r""+personal_path1+r"\hyperedges-datascience-stackexchange-tags_gaifman_K8_T8_S100000.csv"))
    w = w[~w['type'].str.contains('sample', na=False)]
    w = times_total(times_by_k(w))
    z = select_columns(load_table(r""+personal_path1+r"\hyperedges-datascience-stackexchange-tags_hyper_K8_T8_S100000.csv"), COLUMNS_H)
    z = z[~z['step'].str.contains('sample', na=False)]
    z = times_total(times_by_k(z))
    #tempi_pz = load_table(r""+personal_path1+r"\hyperedges-datascience-stackexchange-tags_preproc.csv")
    #tempo_full, tempo_low = compute_projection_times(tempi_pz)
    #w = float(w) + float(tempo_full)
    #z = float(z) + float(tempo_low)
    coppie = [(a, b), (m, o), (l, n), (1000, 1000), (g, p), (w, z)]
    #plot_pairs_aligned(coppie)
    tempi= [(2507076, 3793676), (114481064, 20830848), (23694512, 20900140), (1000, 1000), (5274816, 3504632), (2098564, 1604280)]
    tempi = [(g/(1024**2), h/(1024**2)) for g,h in tempi]
    plot_pairs_aligned1(tempi)

