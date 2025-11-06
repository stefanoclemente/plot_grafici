import statistics

file_path=r'C:\Users\scapp\OneDrive\Documenti\hypergraphs\arxiv_cats_sample.txt'
def calcola_gradi(file_path, deg=5):
    # dizionario: vertice -> grado (numero di iperlati che lo contengono)
    gradi = {}
    gradi_grandi = []
    count = 0
    rank = 0
    with open(file_path, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            vertici = set(int(x) for x in linea.split(",") if x.strip() != "")
            count +=1
            if rank < len(vertici):
                rank= len(vertici)
            for v in vertici:
                gradi[v] = gradi.get(v, 0) + 1
                if gradi[v] > deg:
                    gradi_grandi.append((v, gradi[v]))

    if not gradi:
        raise ValueError("Il file non contiene iperlati / vertici.")

    # grado massimo
    grado_massimo = max(gradi.values())

    # grado medio (media sui vertici che compaiono almeno in un iperlato)
    lista_gradi = list(gradi.values())
    somma_gradi = sum(gradi.values())
    numero_vertici = len(gradi)
    grado_medio = somma_gradi / numero_vertici

    grado_mediano = statistics.median(lista_gradi)

    return grado_massimo, grado_medio, gradi, gradi_grandi, grado_mediano, count, rank


if __name__ == "__main__":
    grado_max, grado_med, gradi, gradi_grandi, grado_mediano, count, rank = calcola_gradi(file_path)
    print(f"Grado massimo: {grado_max}")
    print(f"Grado medio:   {grado_med}")
    print(f"Grado mediano:   {grado_mediano}")
    print(f"Gradi grandi:   {len(gradi_grandi)}")
    print(f"% Gradi grandi: {len(gradi_grandi)/len(gradi.keys())*100:.2f}%")
    print(f"n° vertici {len(gradi)}")
    print(f"n° iperlati {count}")
    print(f"Rank: {rank}")
