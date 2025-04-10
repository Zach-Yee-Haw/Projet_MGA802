import numpy as np
import math
from structure import Structure as St
import streamlit as st
from extra_fonctions import *
from copy import deepcopy
from matplotlib import pyplot as plt
from tqdm import tqdm
import plotly.graph_objects as go

def apprentissage(nb_points = 31, longueur_max = 100, longueur_min = 100, nb_structures = 10,
                  nb_structures_a_garder = 4, nb_iterations = 10, temperature_debut = 0.5,
                  temperature_fin = 0.2, tridimensionnel = True, induit = False, a = 0.5, b = 0.5, biais = 4,
                  plyfig = None, barre_de_progression = None, espace_graph = None):

    """
    Fonction d'apprentissage pour optimiser des structures.

    Paramètres:
    nb_points (int): Nombre de points par structure.
    longueur_max (int): Longueur maximale des segments d'une structure.
    longueur_min (int): Longueur minimale des segments d'une structure.
    nb_structures (int): Nombre total de structures à générer.
    nb_structures_a_garder (int): Nombre de structures à garder après chaque itération.
    nb_iterations (int): Nombre total d'itérations pour l'apprentissage.
    temperature_debut (float): Température initiale pour l'ajustement des paramètres.
    temperature_fin (float): Température finale pour l'ajustement des paramètres.
    tridimensionnel (bool): Indique si les structures sont tridimensionnelles.
    induit (bool): Indique si le champs magnétique est induit ou imposé.
    a (float): Exposant pour le score (encombrement).
    b (float): Exposant pour le score (poids).
    biais (int): Facteur de biais pour le choix des structures.
    montrer_perf (bool): Indique si les performances doivent être affichées.

    Retourne:
    tuple: Le meilleur score et la structure ayant obtenu ce score.
    """



    # On initialise nos cumuls de score
    score_max_cumule = []
    score_min_cumule = []

    if espace_graph != None:
        with espace_graph:
            st.plotly_chart(plyfig, key="perf")

    # On calcule la proportion de structures à garder
    proportion_structure_a_garder = nb_structures_a_garder/nb_structures
    nb_structures = int(nb_structures_a_garder/proportion_structure_a_garder)
    structures = np.ndarray((nb_structures, 2), dtype=object)

    # On calcule l'exposant pour la décroissance de la température
    exposant_temperature = math.log(temperature_fin, nb_iterations)

    print("Génération des structures...")

    # On génère les structures initiales
    for i in tqdm(range(nb_structures)):

        barre_de_progression.progress(i/(nb_structures-1), text="Itération no. : 0, Progrès : "+str(i+1)+"/"+str(nb_structures))
        structure = St(nb_points, longueur_max, longueur_min, tridimensionnel, "Structure no. " + str(i))
        structures[i, 1] = structure

    # On initialise la meilleure structure
    meilleure_structure = [0, structures[0, 1]]

    # Boucle principale d'optimisation
    for i in range(nb_iterations+1):

        # On calcule la température à utiliser
        temperature = temperature_debut * (i+1) ** exposant_temperature

        print("Calcul des performances...")

        # On calcule le score pour chaque structure
        for j in range(nb_structures):
            scores = structures[j, 1].montrer_performance(induit)
            score = scores[2] / (scores[0] ** a * scores[1] ** b)

            structures[j, 0] = score

        # On enregistre les scores maximum et minimum
        score_max = max(structures[:, 0])
        score_min = min(structures[:, 0])

        score_max_cumule.append(score_max)
        score_min_cumule.append(score_min)

        print("Itération : ", str(i), ", score max : ", str(score_max), ", score_min : ", str(score_min))

        # On tri les structures par score
        structures_triees = trier(structures, nb_structures)

        # On met la meilleure structure trouvée jusqu'à présent à jour
        if meilleure_structure[0] <= structures_triees[nb_structures-1, 0]:

            meilleure_structure = structures_triees[nb_structures-1, :]

        # On affiche les performances si demandées
        if espace_graph != None and plyfig != None:

            plyfig.data = []

            plyfig.add_trace(go.Scatter(
                x=list(range(nb_iterations + 1)), y=score_max_cumule,
                marker=dict(size=4, color="red"),
                line=dict(color="red", width=2),
                name="Score maximum par itération"))

            plyfig.add_trace(go.Scatter(
                x=list(range(nb_iterations + 1)), y=score_min_cumule,
                marker=dict(size=4, color="blue"),
                line=dict(color="blue", width=2),
                name="Score minimum par itération"))


            with espace_graph:
                st.plotly_chart(plyfig)

        if i < nb_iterations:
            # On sélectionne les meilleures structures avec biais
            structures_a_garder = choix_biaises(structures_triees, nb_structures_a_garder, biais)

            # On copie les structures conservées jusqu'à ce qu'il y ait autant de structures par rapport à ce qu'on devrait avoir à chaque itération.
            for j in range(nb_structures):

                structures[j, 1] = structures_a_garder[int(j*proportion_structure_a_garder)].copy()[1]

            # On modifie les paramètres des structures selon la température définie pour la nouvelle itération
            for j in tqdm(range(nb_structures)):

                barre_de_progression.progress((j) / (nb_structures-1), text="Itération no. : "+str(i+1)+", Progrès : "+str(j+1)+"/"+str(nb_structures))
                structure = deepcopy(structures[j, 1])
                structure.modifier_parametres(temperature, True, True, str(j))
                structures[j, 1] = structure

            # On mélange les structures
            structures = melanger_structures(structures, nb_structures)



    return meilleure_structure[0], meilleure_structure[1]




