import numpy as np
import math
from structure import Structure as St
from extra_fonctions import *
from copy import deepcopy
from matplotlib import pyplot as plt
from tqdm import tqdm

def apprentissage(nb_points = 31, longueur_max = 100, longueur_min = 100, nb_structures = 10,
                  nb_structures_a_garder = 4, nb_iterations = 20, temperature_debut = 0.5,
                  temperature_fin = 0.2, tridimensionnel = True, induit = False, a = 0.5, b = 0.5, biais = 4,
                  montrer_perf = True):

    score_max_cumule = []
    score_min_cumule = []

    proportion_structure_a_garder = nb_structures_a_garder/nb_structures
    nb_structures = int(nb_structures_a_garder/proportion_structure_a_garder)
    structures = np.ndarray((nb_structures, 2), dtype=object)

    exposant_temperature = math.log(temperature_fin, nb_iterations)

    print("Génération des structures...")

    for i in tqdm(range(nb_structures)):

        structure = St(nb_points, longueur_max, longueur_min, tridimensionnel, "Structure no. " + str(i))
        structures[i, 1] = structure

    meilleure_structure = [0, structures[0, 1]]

    for i in range(nb_iterations):

        temperature = temperature_debut * (i+1) ** exposant_temperature

        print("Calcul des performances...")

        for j in tqdm(range(nb_structures)):
            scores = structures[j, 1].montrer_performance(induit)
            score = scores[2] / (scores[0] ** a * scores[1] ** b)

            structures[j, 0] = score

        score_max = max(structures[:, 0])
        score_min = min(structures[:, 0])

        score_max_cumule.append(score_max)
        score_min_cumule.append(score_min)

        print("Itération : ", str(i), ", score max : ", str(score_max), ", score_min : ", str(score_min))

        structures_triees = trier(structures, nb_structures)

        if meilleure_structure[0] <= structures_triees[nb_structures-1, 0]:

            meilleure_structure = structures_triees[nb_structures-1, :]

        structures_a_garder = choix_biaises(structures_triees, nb_structures_a_garder, biais)

        for j in range(nb_structures):

            structures[j, 1] = structures_a_garder[int(j*proportion_structure_a_garder)].copy()[1]

        for j in tqdm(range(nb_structures)):

            structure = deepcopy(structures[j, 1])
            structure.modifier_parametres(temperature, True, True, str(j))
            structures[j, 1] = structure

        structures = melanger_structures(structures, nb_structures)


    print("Itération : ", str(i+1), ", score max : ", str(score_max), ", score_min : ", str(score_min))

    if montrer_perf:

        plt.plot(range(nb_iterations), score_max_cumule, "-r")
        plt.plot(range(nb_iterations), score_min_cumule, "-b")

        plt.show()


    return meilleure_structure[0], meilleure_structure[1]




