import statistics

file_path=r'C:\Users\scapp\OneDrive\Documenti\hypergraphs\ipergrafo_random_large.txt'
#hypergraphs\hyperedges-amazon-reviews.txt
#hyperedges-stackoverflow-answers
#hyperedges-google
#hyperedges-wikipedia-pages
#hyperedges-mathoverflow-answers
#hyperedges-cpc-group-2024-2025.txt
#hyperedges-datascience-stackexchange-tags.txt
def calcola_gradi(file_path, deg=5):
    # dizionario: vertice -> grado (numero di iperlati che lo contengono)
    gradi = {}
    gradi_grandi = []
    count = 0
    rank = 0
    dimensione = 0
    dimensione_gaifman = 0
    with open(file_path, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            
            vertici = set(int(x) for x in linea.split(",") if x.strip() != "")
            dimensione+=len(vertici)
            dimensione_gaifman+=(len(vertici)**2)
            count +=1
            if rank < len(vertici):
                rank= len(vertici)
            for v in vertici:
                gradi[v] = gradi.get(v, 0) + 1
            
        for v in gradi.keys():
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

    return grado_massimo, grado_medio, gradi, gradi_grandi, grado_mediano, count, rank, dimensione, dimensione_gaifman


if __name__ == "__main__":
    grado_max, grado_med, gradi, gradi_grandi, grado_mediano, count, rank, dimensione, dimensione_gaifman = calcola_gradi(file_path)
    print(f"Grado massimo: {grado_max}")
    print(f"Grado medio:   {grado_med}")
    print(f"Grado mediano:   {grado_mediano}")
    print(f"Gradi grandi:   {len(gradi_grandi)}")
    print(f"% Gradi grandi: {len(gradi_grandi)/len(gradi.keys())*100:.2f}%")
    print(f"n° vertici {len(gradi)}")
    print(f"n° iperlati {count}")
    print(f"Rank: {rank}")
    print(f"Dimensione:   {dimensione}")
    print(f"Dimensione Gaifman:   {dimensione_gaifman}")
