import random
import json
import string
print('Réponse de la question 1 : ')
def BronKerbosch(K, P, X, graphe, max_cliques, taille_clique):
    if not P and not X:
        max_cliques.append(K)
        taille_clique.append(len(K))
        return
    for v in list(P):
        BronKerbosch(K.union({v}), P.intersection(graphe[v]), X.intersection(graphe[v]), graphe, max_cliques,taille_clique)
        P.remove(v)
        X.add(v)

def trouver_cliques_maximales(graphe,fichier):
    max_cliques = []
    tailles_cliques = []
    BronKerbosch(set(), set(graphe.keys()), set(), graphe, max_cliques, tailles_cliques)
    taille_maximale = max(tailles_cliques)
    print('Taille de la clique maximale :', taille_maximale)

    with open(fichier, 'w') as fichier:
        for clique in max_cliques:
            fichier.write(str(clique) + '\n')


graphe = {
    'A': {'B', 'C', 'D', 'E', 'F'},
    'B': {'A', 'G'},
    'C': {'A', 'E', 'D'},
    'D': {'A', 'C', 'F'},
    'E': {'A', 'C', 'F', 'G'},
    'F': {'A', 'D', 'E', 'G', 'H', 'I'},
    'G': {'B', 'E', 'F', 'H'},
    'H': {'G', 'F', 'I'},
    'I': {'H', 'F'}
}
trouver_cliques_maximales(graphe,'fichier_cliques_max')

print('Réponse de la question 2 : ')
def generer_graphe_aleatoire_lettres(n, probabilite):
    graphe = {}
    sommets = []

    for i in range(n):
        sommets.append(chr(65 + i))

    for sommet in sommets:
        graphe[sommet] = set()

    for i, sommet1 in enumerate(sommets):
        for j, sommet2 in enumerate(sommets):
            if random.randint(1,100) <= probabilite and i != j:
                graphe[sommet1].add(sommet2)
                graphe[sommet2].add(sommet1)
    return graphe
def taille_clique_max(graphe):
    max_cliques = []
    taille_cliqe = []
    BronKerbosch(set(), set(graphe.keys()), set(), graphe, max_cliques, taille_cliqe)
    return max(taille_cliqe)
def tester_graphes_aleatoires(nb_graphe,sommets,probabilités ):
    moyenne_aléatoires = {}
    for n in sommets:
        for p in probabilités:
            moyenne_taille_max_clique = 0
            for j in range(nb_graphe):
                graphe = generer_graphe_aleatoire_lettres(n, p)
                moyenne_taille_max_clique += taille_clique_max(graphe)
            moyenne_taille_max_clique /= nb_graphe
            moyenne_aléatoires[(n, p)] = moyenne_taille_max_clique
    return moyenne_aléatoires

nbr_graphes = 10
sommets = [10, 20, 30]
probabilités = [10, 30, 50]
moyenne_aléatoires = tester_graphes_aleatoires(nbr_graphes, sommets, probabilités)
# Affichage des résultats
print("Taille moyenne de la clique maximale en fonction de n et p :")
print("-----------------------------------------------------------")
print(f"|{' n ':^9}|{' p ':^9}|{' Taille moyenne de clique maximale ':^37}|")
print("-----------------------------------------------------------")
for n in sommets:
    for p in probabilités:
        taille_moyenne = moyenne_aléatoires[(n, p)]
        print(f"|  {n:^5}  |  {p:^5}  |  {taille_moyenne:^33.2f}  |")
        print("-----------------------------------------------------------")


print('Réponse de la question 3 : ')
def BronKerbosch_KQuasi(K, P, X, graphe,quasi,q):
    if not P and not X:  # Condition d'arrêt modifiée
        if quasi > 0:
            est_valide(K, 1, graphe,quasi,q)
        elif quasi == 0:
            quasi_clique.append(K)
        return

    for v in list(P):
        K_nv = K.union({v})
        P_nv = P.intersection(graphe[v])
        X_nv = X.intersection(graphe[v])
        BronKerbosch_KQuasi(K_nv, P_nv,X_nv, graphe, quasi,q)
        P.remove(v)
        X.add(v)

def est_valide(K, a, graphe, quasi,q):
    if a <= quasi:
        for s in graphe.keys():
            count = 0
            for v in K:
                if s not in K and s in graphe[v]:
                    count += 1
            if len(K) - count == q:
                if K.union({s}) not in quasi_clique and a == quasi:
                    quasi_clique.append(K.union({s}))
                est_valide(K.union({s}), a+1, graphe, quasi,q)
                est_valide(K.union({s}), a +2, graphe, quasi,q+1)
    else:
        return


def trouver_max_KQuasi_cliques(graphe, fichier_sortie, quasi,q):
    BronKerbosch_KQuasi(set(), set(graphe.keys()), set(), graphe, quasi,q)
    m = len(quasi_clique[0])
    for i in range(1, len(quasi_clique)):
        if len(quasi_clique[i]) > m:
            m = len(quasi_clique[i])
    print(f'la taille de {quasi}-quasi clique maximum {m}')
    # Écrire les résultats dans le fichier
    with open(fichier_sortie, 'w') as f:
        for clique in quasi_clique:
            f.write(str(clique) + '\n')
graph = {
    'A': {'B', 'C', 'D', 'E', 'F'},
    'B': {'A', 'G'},
    'C': {'A', 'E', 'D'},
    'D': {'A', 'C', 'F'},
    'E': {'A', 'C', 'F', 'G'},
    'F': {'A', 'D', 'E', 'G', 'H', 'I'},
    'G': {'B', 'E', 'F', 'H'},
    'H': {'G', 'F', 'I'},
    'I': {'H', 'F'}
}

quasi_clique=[]
trouver_max_KQuasi_cliques(graph, 'quasi.txt',1,1)

print('Réponse de la question 4 : ')
def evaluer_quasi_cliques_sur_graphes_aleatoires(nb_graphes, sommets, probabilites, k_max):
    evaluations = {}
    for n in sommets:
        for p in probabilites:
            tailles_moyennes_max_quasi_clique = {}
            for k in range(0, k_max + 1):
                taille_moyenne = 0
                for i in range(nb_graphes):
                    graphe = generer_graphe_aleatoire_lettres(n, p)
                    quasi_clique.clear()
                    BronKerbosch_KQuasi(set(), set(graphe.keys()), set(), graphe, k, 1)
                    if quasi_clique:
                        taille_max = len(quasi_clique[0])
                        for j in range(1, len(quasi_clique)):
                            if len(quasi_clique[j]) > taille_max:
                                taille_max = len(quasi_clique[j])
                        taille_moyenne += taille_max
                tailles_moyennes_max_quasi_clique[k] = taille_moyenne / nb_graphes
            evaluations[(n, p)] = tailles_moyennes_max_quasi_clique

    return evaluations

nbr_graphe2 = 2
sommets_2 = [9,8,7]
probabilités_2 = [10,30,50]
k_maxQ4 = 3
evaluation_k_quasi_cliques = evaluer_quasi_cliques_sur_graphes_aleatoires(nbr_graphe2, sommets_2 , probabilités_2, k_maxQ4)
print("Taille moyenne de la plus grande k-quasi-clique en fonction de n, p et k :")
print("-----------------------------------------------------------------------------")
print(f"|{' n ':^9}|{' p ':^9}|{' k ':^7}|{'Taille moyenne de la plus grande k-quasi-clique':^39}|")
print("-----------------------------------------------------------------------------")
for n in sommets_2:
    for p in probabilités_2:
        for k in range(0, k_maxQ4 + 1):
            avg_size = evaluation_k_quasi_cliques[(n, p)][k]
            print(f"|  {n:^5}  |  {p:^5}  |  {k:^3}  |  {avg_size:^43.2f}  |")
print("-----------------------------------------------------------------------------")

print('Réponse de la question 5 (SNAP ET KONNECT) : ')
quasi_clique.clear()
#TEST SNAP
def diviser_dictionnaire(data_set):
    return list(dataSet.values())

try:
    # Ouvrir le fichier JSON en mode lecture
    with open('graphe_Snap.json', 'r') as file:
        # Charger le contenu JSON
        dataSet = json.load(file)
       # print(dataSet)

    graphes_divises = diviser_dictionnaire(dataSet)

    #for i, graphe in enumerate(graphes_divises, 1):
        #print(f"Graphe {i}:")
        #print(graphe)
        #print("-----------")

except FileNotFoundError:
    print("Le fichier graphs.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Le fichier graphs.json n'est pas un fichier JSON valide.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")


# On convertie les sous-listes en dictionnaire afin de réutiliser les fonctions déjà développer précedament
def toDict(sublists):
    graphes_dicts = []
    for graphe in graphes_divises:
        graphe_dict = {}
        for edge in graphe:
            u, v = edge
            if u not in graphe_dict:
                graphe_dict[u] = []
            if v not in graphe_dict:
                graphe_dict[v] = []
            graphe_dict[u].append(v)
            graphe_dict[v].append(u)
        graphes_dicts.append(graphe_dict)
    return graphes_dicts


# On récupère la data set
dataSet = toDict(graphes_divises)
graph_Snap = toDict(graphes_divises)
# print(graph)
print("Test SNAP :")
print(graph_Snap[9998])
trouver_max_KQuasi_cliques(graph_Snap[9998], 'Snap.txt', 1, 1)
#TEST KONNECT
graph_konnect = {}
with open("graphe_Konnect.hiv", "r") as file:
    for line in file:
        if not line.startswith("#"):
            parts = line.strip().split("\t")
            source = int(parts[0])
            target = int(parts[1])
            if source not in graph_konnect:
                graph_konnect[source] = []
            if target != source:
                graph_konnect[source].append(target)

print("Test KONNECT :")
print(graph_konnect)
trouver_max_KQuasi_cliques(graph_konnect, 'konnect.txt', 3, 1)

