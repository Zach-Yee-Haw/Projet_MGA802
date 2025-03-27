from random import random as rd
import numpy as np

def choix_biaises(liste_de_choix, nb_de_choix, biais):

    choix = []
    liste_de_choix_modifiee = []

    for i in range(len(liste_de_choix)):

        liste_de_choix_modifiee.append(liste_de_choix[i])

    for i in range(nb_de_choix):

        position = int((rd()**(1/biais))*len(liste_de_choix_modifiee))

        choix.append(liste_de_choix_modifiee[position])
        liste_de_choix_modifiee.pop(position)

    return choix

def trier(structures, nb_structures):

    triage = structures[:, 0].argsort()

    structures_triees = np.zeros_like(structures)

    for j in range(nb_structures):
        structures_triees[j, 0] = structures[triage[j], 0]
        structures_triees[j, 1] = structures[triage[j], 1]

    return structures_triees

def calculer_score(structures, nb_structures, induit, a, b):

    """
    Pour toutes les structures, on calcule le score total selon les critères de pondération sélectionnés.
    :param structures: Ndarray contenant les scores et les structures
    :param nb_structures: Nombre de structures dont le score doit être calculé.
    :param induit: Choix de la méthode de calcul de la force (induit ou imposé)
    :param a: Pondération exponentielle de l'encombrement de la structure
    :param b: Pondération exponentielle du poids de la structure
    :return:
    """

    for i in range(nb_structures):

        scores = structures[i, 1].montrer_performance(induit)
        score = scores[2]/(scores[0]**a * scores[1]**b)

        structures[i, 0] = score

def melanger_structures(structures, nb_structures):

    indices_aleatoires = choix_biaises(range(nb_structures), nb_structures, 1)

    nouvelle_liste = structures.copy()

    for i in range(nb_structures):

        nouvelle_liste[i, :] = structures[indices_aleatoires[i], :]

    return nouvelle_liste