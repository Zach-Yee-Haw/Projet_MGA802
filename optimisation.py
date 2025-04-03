import scipy as scp

def optimisation(structure, induit = False, a = 0.5, b = 0.5, tridimensionnel = True):

    longueurs, angles = structure.montrer_parametres()

    theta = angles[:, 0]
    phi = angles[:, 1]


    params = [longueurs, theta, phi]

    print("Optimisation par la méthode de Newton en cours...")

    x, converged, zero_der = scp.optimize.newton(structure.redefinir_parametres, params, args=(induit, a, b, tridimensionnel), maxiter=20, rtol=0.01, full_output=True)

    print("Paramètres en ce moment :")
    print(structure.montrer_parametres())
    print("Paramètres optimaux :")
    print(x)
    print("Convergé :")
    print(converged)
    print("Zero_der :")
    print(zero_der)

    structure.redefinir_parametres(x, induit, a, b, tridimensionnel)

    scores = structure.montrer_performance(induit)
    score = scores[2] / (scores[0] ** a * scores[1] ** b)

    return score, structure