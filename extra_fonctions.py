from random import random as rd
import numpy as np

def choix_biaises(liste_de_choix, nb_de_choix, biais):

    """
    Sélectionne un certain nombre d'éléments d'une liste avec un biais donné.
    
    
    :param liste_de_choix: Liste des éléments parmi lesquels choisir.
    :param nb_de_choix: Nombre d'éléments à sélectionner.
    :param biais: Facteur de biais pour influencer les choix (plus bas, plus les premiers éléments sont favorisés).
    
    Returns:
        choix: Liste des éléments sélectionnés avec biais.
    """
    choix = []  # Liste pour stocker les choix effectués
    liste_de_choix_modifiee = []  # Copie modifiable de la liste de choix

    # Crée une copie de la liste initiale
    for i in range(len(liste_de_choix)):
        liste_de_choix_modifiee.append(liste_de_choix[i])

    # Sélection des éléments avec biais
    for i in range(nb_de_choix):
        # Calcul de la position dans la liste en fonction du biais
        position = int((rd()**(1/biais))*len(liste_de_choix_modifiee))

        # Ajout de l'élément sélectionné à la liste des choix
        choix.append(liste_de_choix_modifiee[position])
        # Suppression de l'élément sélectionné pour éviter les doublons
        liste_de_choix_modifiee.pop(position)

    return choix

def trier(structures, nb_structures):

    """
    Trie une liste de structures en fonction de leurs scores dans l'ordre croissant.
    
    :param structures: Tableau contenant les scores et les structures associées.
    :param nb_structures: Nombre de structures à trier.
    
    Returns:
        structures_triees: Tableau trié des structures.
    """
    # Obtient les indices pour trier les structures par score croissant
    triage = structures[:, 0].argsort()

    # Crée un nouveau tableau pour les structures triées
    structures_triees = np.zeros_like(structures)

    # Remplit le tableau avec les structures triées
    for j in range(nb_structures):
        structures_triees[j, 0] = structures[triage[j], 0]  # Score
        structures_triees[j, 1] = structures[triage[j], 1]  # Structure associée

    return structures_triees

def melanger_structures(structures, nb_structures):

    """
    Mélange les structures de manière aléatoire.
    
    :param structures: Tableau contenant les structures et leurs scores.
    :param nb_structures: Nombre de structures à mélanger.
    
    Returns:
        nouvelle_liste: Nouveau tableau contenant les structures mélangées.
    """
    # Génère des indices aléatoires pour mélanger les structures
    indices_aleatoires = choix_biaises(range(nb_structures), nb_structures, 1)

    # Crée une copie du tableau des structures pour le mélange
    nouvelle_liste = structures.copy()

    # Réorganise les structures selon les indices aléatoires générés
    for i in range(nb_structures):
        nouvelle_liste[i, :] = structures[indices_aleatoires[i], :]

    return nouvelle_liste
