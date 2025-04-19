import numpy as np
import math
from structure import Structure as St
from extra_fonctions import *
from copy import deepcopy
from tqdm import tqdm
import plotly.graph_objects as go

def apprentissage(nb_points = 31, longueur_max = 100, longueur_min = 100, nb_structures = 10,
                  nb_structures_a_garder = 4, nb_iterations = 10, temperature_debut = 0.5,
                  temperature_fin = 0.2, encombrement_cible = 500, tridimensionnel = True, induit = False, b = 0.5, biais = 4,
                  plyfig = None, figure = None):
    """
    Fonction d'apprentissage pour optimiser des structures.

    :param nb_points: Nombre de points par structure.
    :type nb_points: int
    :param longueur_max: Longueur maximale des segments d'une structure.
    :type longueur_max: float
    :param longueur_min: Longueur minimale des segments d'une structure.
    :type longueur_min: float
    :param nb_structures: Nombre total de structures à générer.
    :type nb_structures: int
    :param nb_structures_a_garder: Nombre de structures à garder après chaque itération.
    :type nb_structures_a_garder: int
    :param nb_iterations: Nombre total d'itérations pour l'apprentissage.
    :type nb_iterations: int
    :param temperature_debut: Température initiale pour l'ajustement des paramètres.
    :type temperature_debut: float
    :param temperature_fin: Température finale pour l'ajustement des paramètres.
    :type temperature_fin: float
    :param tridimensionnel: Indique si les structures sont tridimensionnelles.
    :type tridimensionnel: bool
    :param induit: Indique si le champs magnétique est induit ou imposé.
    :type induit: bool
    :param b: Exposant pour le score (poids).
    :type b: float
    :param biais: Facteur de biais pour le choix des structures.
    :type biais: float
    :param plyfig: Figure permettant de montrer la performance à l'utilisateur
    :type plyfig: figure plotly
    :param figure: figure montrant la structure actuelle
    :type figure: figure plotly

    :return: Le meilleur score et la structure ayant obtenu ce score.
    :rtype: tuple
    """
    # Initialisation des variables pour les scores cumulés
    score_max_cumule = []
    score_min_cumule = []

    # Calcul de la proportion des structures à conserver
    proportion_structure_a_garder = nb_structures_a_garder/nb_structures
    structures = np.ndarray((nb_structures, 2), dtype=object)

    # Calcul de l'exposant pour la décroissance de la température
    exposant_temperature = math.log(temperature_fin, nb_iterations)

    print("Génération des structures...")

    # Génération des structures initiales
    for i in tqdm(range(nb_structures)):
        # print("Itération no. : 0, Progrès : "+str(i+1)+"/"+str(nb_structures))
        structure = St(nb_points, longueur_max, longueur_min, encombrement_cible, tridimensionnel, "Structure no. " + str(i))
        structures[i, 1] = structure

    # Initialisation de la meilleure structure (score et objet structure)
    meilleure_structure = [0, structures[0, 1]]

    # Boucle principale pour les itérations d'apprentissage
    for i in range(nb_iterations+1):
        # Calcul de la température pour cette itération
        temperature = temperature_debut * (i+1) ** exposant_temperature

        print("Calcul des performances...")

        # Calcul des scores pour chaque structure
        for j in range(nb_structures):
            scores = structures[j, 1].montrer_performance(induit)
            score = scores[2] / (scores[1] ** b)
            structures[j, 0] = score

        # Enregistrement des scores maximum et minimum
        score_max = max(structures[:, 0])
        score_min = min(structures[:, 0])
        score_max_cumule.append(score_max)
        score_min_cumule.append(score_min)

        print("Itération : ", str(i), ", score max : ", str(score_max), ", score_min : ", str(score_min))

        # Tri des structures en fonction des scores
        structures_triees = trier(structures, nb_structures)

        # Mise à jour de la meilleure structure si une meilleure est trouvée
        if meilleure_structure[0] <= structures_triees[nb_structures-1, 0]:
            meilleure_structure = structures_triees[nb_structures-1, :]

        # Mise à jour du titre pour la visualisation
        enc, poi, force = meilleure_structure[1].montrer_performance()
        titre = ("Score : " + str(meilleure_structure[0]) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) +
                 ", force = " + str(force) + ".")

        # Ajout de la structure dans la figure
        meilleure_structure[1].visualiser_structure(figure, titre)

        # Affichage des performances cumulées si demandé
        if plyfig != None:
            # Réinitialisation de la figure
            plyfig.data = []
            # Ajout du score maximum dans la figure
            plyfig.add_trace(go.Scatter(
                x=list(range(nb_iterations + 1)), y=score_max_cumule,
                marker=dict(size=4, color="red"),
                line=dict(color="red", width=2),
                name="Score maximum par itération"))
            # Ajout du score minimum dans la figure
            plyfig.add_trace(go.Scatter(
                x=list(range(nb_iterations + 1)), y=score_min_cumule,
                marker=dict(size=4, color="blue"),
                line=dict(color="blue", width=2),
                name="Score minimum par itération"))

            # Affichage de la figure
            plyfig.update_traces()

        # Si l'apprentissage n'est pas terminé, on prépare la prochaine itération
        if i < nb_iterations:
            # Sélection des meilleures structures avec biais
            structures_a_garder = choix_biaises(structures_triees, nb_structures_a_garder, biais)

            # Remplissage des structures pour la nouvelle itération
            for j in range(nb_structures):
                structures[j, 1] = structures_a_garder[int(j*proportion_structure_a_garder)].copy()[1]

            # Modification des paramètres des structures pour la nouvelle itération
            for j in tqdm(range(nb_structures)):
                # print("Itération no. : "+str(i+1)+", Progrès : "+str(j+1)+"/"+str(nb_structures))
                structure = deepcopy(structures[j, 1])
                structure.modifier_parametres(temperature, True, True, str(j))
                structures[j, 1] = structure

            # Mélange des structures pour diversifier les configurations
            structures = melanger_structures(structures, nb_structures)


    # Retourne le meilleur score et la structure associée
    return meilleure_structure[0], meilleure_structure[1]




