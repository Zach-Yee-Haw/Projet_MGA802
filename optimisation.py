import numpy as np
import scipy as scp
from functools import partial as pa
from copy import deepcopy
import streamlit as st
import plotly.graph_objects as go

# Fonction principale d'optimisation
def optimisation(structure, induit = False, a = 0.5, b = 0.5, tridimensionnel = True, nb_iterations = 20,
                 tolerance = 0.01, barre_de_progression = None, figure = None, espace = None):
    """
    Fonction pour optimiser les paramètres d'une structure donnée en utilisant l'algorithme de Nelder-Mead.

    :param structure: Structure à optimiser.
    :type structure: Structure
    :param induit: Indique si le champs magnétique est induit ou imposé.
    :type induit: bool
    :param a: Importance du critère d'encombrement.
    :type a: float
    :param b: Importance du critère de poids.
    :type b: float
    :param tridimensionnel: Indique si l'optimisation est en 3D.
    :type tridimensionnel: bool
    :param nb_iterations: Nombre maximal d'itérations.
    :type nb_iterations: int
    :param tolerance: Tolérance pour la convergence.
    :type tolerance: float
    :param barre_de_progression: Barre de progression Streamlit.
    :type barre_de_progression: barre de progression streamlit
    :param figure: Figure plotly servant à afficher la structure.
    :type figure: figure plotly
    :param espace: Espace Streamlit pour afficher la structure.
    :type espace: espace streamlit

    :return: Score final et structure optimisée.
    :rtype: tuple
    """
    # Définition des paramètres globaux
    global structure_temp
    global iter

    # Récupération des paramètres pour l'optimisation
    longueurs, angles = structure.montrer_parametres()
    iter = 0
    structure_temp = deepcopy(structure)
    nb_iter = nb_iterations
    barre = barre_de_progression

    # Extraction des angles theta et phi
    theta = angles[:, 0]
    phi = angles[:, 1]
                   
    # Préparation des paramètres sous forme d'un tableau en une ligne (requis pour scipi.optimize.minimize)
    nb_segments = np.size(longueurs)
    params = np.ndarray((nb_segments*3))
    params[0:nb_segments] = longueurs
    params[nb_segments:nb_segments*2] = theta
    params[nb_segments*2:nb_segments*3] = phi

    # Mise à jour de la barre de progression
    barre.progress(0, text="Calcul des dérivées en cours pour l'optimisation de Nelder-Mead...")

    # Définition d'un callback avec plus de paramètres pour suivre l'avancement
    mettre_bar_a_jour = pa(callback,nb_iter, barre_de_progression, figure, espace, a, b)

    # Optimisation avec l'algorithme de Nelder-Mead
    resultats = scp.optimize.minimize(structure.redefinir_parametres, params, method='Nelder-Mead', args=(induit, a, b, tridimensionnel), options={'maxiter':nb_iterations, 'disp':False, 'xatol':tolerance}, callback=mettre_bar_a_jour)

    # Récupération des nouveaux paramètres optimisés
    x = resultats.get('x')

    # Mise à jour de la structure avec les nouveaux paramètres
    structure.redefinir_parametres(x, induit, a, b, tridimensionnel)

    # Calcul des performances finales
    scores = structure.montrer_performance(induit)
    score = scores[2] / (scores[0] ** a * scores[1] ** b)

    return score, structure

# Callback pour mettre à jour les visualisations pendant l'optimisation
def callback(nb_iter, barre, figure, espace, a, b, etat):
    """
    Fonction callback appelée à chaque itération pour mettre à jour la barre de progression
    et visualiser l'état actuel de la structure.
    
    :param nb_iter: Nombre total d'itérations.
    :type nb_iter: int
    :param barre: Composant Streamlit pour afficher la progression.
    :type barre: barre de progression streamlit
    :param figure: Figure plotly pour afficher la structure.
    :type figure: figure plotly
    :param espace: Espace Streamlit pour afficher la structure.
    :type espace: espace streamlit
    :param a: Importance du critère d'encombrement.
    :type a: float
    :param b: Importance du critère de poids.
    :type b: float
    :param etat: État actuel des paramètres.
    :type etat: ndarray
    """
    global structure_temp
    global iter

    # Mise à jour des paramètres de la structure temporaire
    x = etat
    structure_temp.redefinir_parametres(x)

    # Calcul des performances actuelles
    enc, poi, force = structure_temp.montrer_performance()
    score = force / (enc**a * poi**b)

    # Mise à jour du titre avec les scores actuels
    titre = "Score : " + str(score) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) + ", force = " + str(
        force) + "."

    # Réinitialisation de la figure pour la visualisation
    figure.data = []

    # Ajout d'un point pour le satellite dans la visualisation
    figure.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        marker=dict(size=4,
                    color="red"),
        name="Satellite"))

    # Visualisation de la structure optimisée
    structure_temp.visualiser_structure(figure, titre)
    with espace:
        st.plotly_chart(figure, key="opti" + str(iter), use_container_width=False)

    # Mise à jour de la barre de progression
    barre.progress(iter/(nb_iter-1), text="Progrès de l'optimisation : "+str(iter+1)+"/"+str(nb_iter))
    iter += 1




