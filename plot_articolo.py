import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from pathlib import Path
from itertools import product

#Colonne rilevanti
COLUMNS=['size', 'type', 'walltime']
COLUMNS_H=['size', 'step', 'walltime']
kappa=list(range(5,9))
core=['1', '2', '4', '8', '16', '20', '24']
personal_path='C:/Users/scapp/Downloads/mathoverflow/'

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
    data = [df[i:i + 4] for i in range(0, len(df), 4)]
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
            label=f"k= {j+3}"
        )

    # Etichette

    ax.set_xlabel("")
    ax.set_ylabel("Time (in sec)")
    ax.set_title(name)
    ax.set_xticks(x)
    ax.set_xticklabels([f'1 Core'] + [f'{i} Cores' for i in core[1::]])
    ax.legend(title="Max graphlet size")

    plt.tight_layout()
if __name__=='__main__':

    # Faccio una lista di dataframe pandas per ogni tipo di run
    g, g_d, h, h_d = ([], [], [], [])

    #Nota: ogni lista ha 42 elementi. Prima scorre su k, poi per i core (dunque 0-5 per 1 core, 6-11 per 2 etc.)
    
    for (c, k) in product(core, kappa):
        l = select_columns(load_table(r""+personal_path+"hyperedges-mathoverflow-answers_gaifman_K"+str(k)+"_T"+str(c)+"_S1000000.csv"))
        l = l[~l['type'].str.contains('sample', na=False)]
        m = select_columns(load_table(r""+personal_path+"hyperedges-mathoverflow-answers_gaifman_dedup_K"+str(k)+"_T"+str(c)+"_S1000000.csv"))
        m = m[~m['type'].str.contains('sample', na=False)]
        n = select_columns(load_table(r""+personal_path+"hyperedges-mathoverflow-answers_hyper_dedup_K"+str(k)+"_T"+str(c)+"_S1000000.csv"), COLUMNS_H)
        n = n[~n['step'].str.contains('sample', na=False)]
        o = select_columns(load_table(r""+personal_path+"hyperedges-mathoverflow-answers_hyper_K"+str(k)+"_T"+str(c)+"_S1000000.csv"), COLUMNS_H)
        o = o[~o['step'].str.contains('sample', na=False)]
        g.append(l)
        g_d.append(m)
        h_d.append(n)
        h.append(o)
    # Aggregazione per size
    g = [times_by_k(table) for table in g]
    g_d = [times_by_k(table) for table in g_d]
    h = [times_by_k(table) for table in h]
    h_d = [times_by_k(table) for table in h_d]
    # Totale tempo
    g_tot = [times_total(table) for table in g]
    g_d_tot = [times_total(table) for table in g_d]
    h_tot = [times_total(table) for table in h]
    h_d_tot = [times_total(table) for table in h_d]

    compute_aggregate_times(g_tot, "Gaifman + Motivo")
    compute_aggregate_times(g_d_tot, "Dedup Motivo")
    compute_aggregate_times(h_tot, "HyperMotivo (No dedup)")
    compute_aggregate_times(h_d_tot, "Aggregate build-up runtime for HyperMotivo")
    plt.show()
    

    
