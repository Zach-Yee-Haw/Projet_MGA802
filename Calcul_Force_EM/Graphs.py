import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np

def GraphForce(x, y, cste):
    '''
    Cette fonction permet de tracer la force électromagnétique selon un paramètre
    
    Attributs :
        - x (array) (m,)        Liste des abscisses des points du câble [m]
        - y (array) (m,)        Liste des ordonnées des points du câble [m]
        - z (array) (m,)        Liste des côtes des points du câble     [m]
        - variable (str)        Variable à analyser en x [unités variables]
    Returns
    -------
        - Graphique de la force électromagnétique en fonction de la variable analysée

    '''
    if cste == 'diam':
        label = 'Diamètre [mm]'
    elif cste == 'm':
        label = 'Masse [kg]'
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(x, y, label=label)
    ax.set_xlabel('Diamètre câble [mm]')
    ax.set_ylabel('Force EM [N]')
    ax.set_title('Câble Paramétré en 3D')
    ax.grid()
    plt.legend()
    plt.show()
    
    return