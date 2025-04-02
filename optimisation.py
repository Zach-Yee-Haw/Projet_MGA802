import scipy as scp

def optimisation(structure, induit = False, a = 0.5, b = 0.5):

    longueurs, angles = structure.montrer_parametres()

    theta = angles[:, 0]
    phi = angles[:, 1]

    params = [longueurs, theta, phi]


    scp.optimize.newton(structure.redefinir_parametres, params, args=(induit, a, b), maxiter=20, tol=1)

    return structure