import numpy as np
import scipy as scp

def optimisation(structure, induit = False, a = 0.5, b = 0.5, tridimensionnel = True, nb_iterations = 20, tolerance = 0.01, longueur_min = 100, longueur_max = 100):

    longueurs, angles = structure.montrer_parametres()

    theta = angles[:, 0]
    phi = angles[:, 1]

    nb_segments = np.size(longueurs)
    params = np.ndarray((nb_segments*3))
    params[0:nb_segments] = longueurs
    params[nb_segments:nb_segments*2] = theta
    params[nb_segments*2:nb_segments*3] = phi

    #borne_min = np.zeros_like(params)
    #borne_max = np.zeros_like(params)
    #borne_min[0:nb_segments] = longueur_min
    #borne_max[0:nb_segments] = longueur_max
    #borne_min[nb_segments:nb_segments*2] = 0
    #borne_max[nb_segments:nb_segments * 2] = 2*np.pi
    #borne_min[nb_segments * 2:nb_segments * 3] = -np.pi/2
    #borne_max[nb_segments * 2:nb_segments * 3] = np.pi / 2

    #bornes = scp.Bounds(lb=borne_min, ub=borne_max)



    print("Optimisation par la méthode de Nelder Mead...")
    resultats = scp.optimize.minimize(structure.redefinir_parametres, params, method='Nelder-Mead', args=(induit, a, b, tridimensionnel), options={'maxiter':nb_iterations, 'disp':False, 'xatol':tolerance})

    x = resultats.get('x')

    print("Paramètres en ce moment :")
    print(structure.montrer_parametres())
    print("Paramètres optimaux :")
    print(x)

    structure.redefinir_parametres(x, induit, a, b, tridimensionnel)

    scores = structure.montrer_performance(induit)
    score = scores[2] / (scores[0] ** a * scores[1] ** b)

    return score, structure