import ppigrf
import numpy as np
        
def ChampMagnetique(r, theta, phi, date):
    '''
    Permet de connaitre le champ magnétique terrestre au point de coordonnées
    sphériques (r,θ,φ), exprimé dans le repère terrestre ECEF, à la date définie
    par le paramètre 'date'
    
    Attributs :
        - r (float)         Coordonnée selon r du point de calcul            [km]
        - theta (float)     Coordonnée selon θ du point de calcul            [deg]
        - phi (float)       Coordonnée selon φ du point de calcul            [deg]
        - date (datetime)   Date de calcul
    
    Sorties :
        - B_r (float)       Composante selon r du champ magnétique terrestre [T]
        - B_theta (float)   Composante selon θ du champ magnétique terrestre [T]
        - B_phi (float)     Composante selon φ du champ magnétique terrestre [T]
    '''  
    [B_r, B_theta, B_phi] = ppigrf.igrf_gc(r, theta, phi, date) # [nT]
    B_r = np.squeeze(B_r) *10**-9         # [T]
    B_theta = np.squeeze(B_theta) *10**-9 # [T]
    B_phi = np.squeeze(B_phi) *10**-9     # [T]

    return B_r,B_theta,B_phi
