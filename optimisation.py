import numpy as np
import scipy as scp
from functools import partial as pa

iter = 0

def optimisation(structure, induit = False, a = 0.5, b = 0.5, tridimensionnel = True, nb_iterations = 20,
                 tolerance = 0.01, longueur_min = 100, longueur_max = 100, barre_de_progression = None):

    longueurs, angles = structure.montrer_parametres()


    iter = 0
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


    mettre_bar_a_jour = pa(callback,nb_iter, barre_de_progression)

    resultats = scp.optimize.minimize(structure.redefinir_parametres, params, method='Nelder-Mead', args=(induit, a, b, tridimensionnel), options={'maxiter':nb_iterations, 'disp':False, 'xatol':tolerance}, callback=mettre_bar_a_jour)

    x = resultats.get('x')

    structure.redefinir_parametres(x, induit, a, b, tridimensionnel)

    scores = structure.montrer_performance(induit)
    score = scores[2] / (scores[0] ** a * scores[1] ** b)

    return score, structure

def callback(nb_iter, barre, etat):

    global iter

    print(str(iter), "\n", str(nb_iter))
    barre.progress(iter/(nb_iter-1), text="Itération : "+str(iter+1)+"/"+str(nb_iter))
    iter += 1




