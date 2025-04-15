import numpy as np
import scipy as scp
from functools import partial as pa
from copy import deepcopy
import streamlit as st
import plotly.graph_objects as go

iter = 0

def optimisation(structure, induit = False, a = 0.5, b = 0.5, tridimensionnel = True, nb_iterations = 20,
                 tolerance = 0.01, longueur_min = 100, longueur_max = 100, barre_de_progression = None, figure = None, espace = None):
    global structure_temp
    global iter

    longueurs, angles = structure.montrer_parametres()


    iter = 0
    structure_temp = deepcopy(structure)
    nb_iter = nb_iterations
    barre = barre_de_progression

    theta = angles[:, 0]
    phi = angles[:, 1]

    nb_segments = np.size(longueurs)
    params = np.ndarray((nb_segments*3))
    params[0:nb_segments] = longueurs
    params[nb_segments:nb_segments*2] = theta
    params[nb_segments*2:nb_segments*3] = phi

    barre.progress(0, text="Calcul des dérivées en cours pour l'optimisation de Nelder-Mead...")


    mettre_bar_a_jour = pa(callback,nb_iter, barre_de_progression, figure, espace, a, b)

    resultats = scp.optimize.minimize(structure.redefinir_parametres, params, method='Nelder-Mead', args=(induit, a, b, tridimensionnel), options={'maxiter':nb_iterations, 'disp':False, 'xatol':tolerance}, callback=mettre_bar_a_jour)

    x = resultats.get('x')

    structure.redefinir_parametres(x, induit, a, b, tridimensionnel)

    scores = structure.montrer_performance(induit)
    score = scores[2] / (scores[0] ** a * scores[1] ** b)

    return score, structure

def callback(nb_iter, barre, figure, espace, a, b, etat):

    global structure_temp
    global iter
    x = etat
    structure_temp.redefinir_parametres(x)
    enc, poi, force = structure_temp.montrer_performance()
    score = force / (enc**a * poi**b)
    titre = "Score : " + str(score) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) + ", force = " + str(
        force) + "."

    figure.data = []

    figure.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        marker=dict(size=4,
                    color="red"),
        name="Satellite"))

    structure_temp.visualiser_structure(figure, titre)
    with espace:
        st.plotly_chart(figure, key="opti" + str(iter), use_container_width=False)

    barre.progress(iter/(nb_iter-1), text="Progrès de l'optimisation : "+str(iter+1)+"/"+str(nb_iter))
    iter += 1




