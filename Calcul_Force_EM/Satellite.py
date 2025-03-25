import numpy as np
from math import cos, sin, pi

def Sat2Earth(X, Y, Z, INC, TA, Sat):
    '''
    Permet d'effectuer un changement de coordonnées entre les coordonnées
    cartésiennes du repère du satellite et les coordonnées sphériques du repère
    ECEF. 
    
    - Fonctionne pour des coordonnées de points
    
    - Cette fonction est la réciproque de Earth2Sat()
    
    Attributs :
        - X (float)         Abscisse du point dans le repère du satellite    [m]
        - Y (float)         Ordonnée du point dans le repère du satellite    [m]
        - Z (float)         Côte du point dans le repère du satellite        [m]
        - INC (float)       Inclinaison de l'orbite du satellite             [deg]
        - TA (float)        Anomalie vraie du satellite                      [deg]
        - Sat (array) (3,1) Vecteur position du satellite dans ECEF 
                            (coordonnées sphérique) (r,θ,φ)       [km],[deg],[deg]
        
    Sorties :
        - r (float)         Coordonnée selon r du point dans le repère ECEF  [km]
        - theta (float)     Coordonnée selon θ du point dans le repère ECEF  [deg]
        - phi (float)       Coordonnée selon φ du point dans le repère ECEF  [deg]
    '''
    INC = INC*pi/180 # [rad]
    TA = TA*pi/180   # [rad]
        
    P = np.array([[X*10**-3],[Y*10**-3],[Z*10**-3]]) # [km] Vecteur position du point dans le repère du satellite
        
    # Matrice de passage Sphérique vers Cartésien Sat
    R = np.array([[0, -sin(-INC*sin(TA)), cos(-INC*sin(TA))],
                  [0, -cos(-INC*sin(TA)), -sin(-INC*sin(TA))],
                  [1, 0, 0]])
    R2 = np.linalg.inv(R) # Matrice de passage Cartésien Sat vers Sphérique
        
    # Coordonnées du point P dans le repère Sphérique 
    [[r],[theta],[phi]] = np.dot(R2,P) + Sat # [km] Vecteur position du point dans le repère terrestre fixe
        
    return r, theta, phi

#______________________________________________________________________________

def Earth2Sat(r, theta, phi, INC, TA, Sat):
    '''
    Permet d'effectuer un changement de coordonnées entre les coordonnées
    sphériques du repère ECEF et les coordonnées cartésiennes du repère du satellite. 
    
    - Fonctionne pour des coordonnées de points
    
    - Cette fonction est la réciproque de Sat2Earth()
    
    Attributs :
        - r (float)         Coordonnée selon r du point dans le repère ECEF  [km]
        - theta (float)     Coordonnée selon θ du point dans le repère ECEF  [deg]
        - phi (float)       Coordonnée selon φ du point dans le repère ECEF  [deg]
        - INC (float)       Inclinaison de l'orbite du satellite             [deg]
        - TA (float)        Anomalie vraie du satellite                      [deg]
        - Sat (array) (3,1) Vecteur position du satellite dans ECEF 
                            (coordonnées sphérique) (r,θ,φ)       [km],[deg],[deg]
        
    Sorties :
        - X (float)         Abscisse du point dans le repère du satellite    [m]
        - Y (float)         Ordonnée du point dans le repère du satellite    [m]
        - Z (float)         Côte du point dans le repère du satellite        [m]
    '''
    INC = INC*pi/180 # [rad]
    TA = TA*pi/180   # [rad]

    P = np.array([[r],[theta],[phi]]) # Vecteur position du point dans le repère terrestre fixe
        
    # Matrice de passage Sphérique vers Cartésien Sat
    R = np.array([[0, -sin(-INC*sin(TA)), cos(-INC*sin(TA))],
                  [0, -cos(-INC*sin(TA)), -sin(-INC*sin(TA))],
                  [1, 0, 0]])
        
    # Coordonnées du point P dans le repère du satellite
    [[X],[Y],[Z]] = np.dot(R,P-Sat)

    return X*10**-3, Y*10**-3, Z*10**-3 # [m]

#______________________________________________________________________________

def Earth2Sat_cm(r, theta, phi, INC, TA):
    '''
    Permet d'effectuer un changement de coordonnées entre les coordonnées
    sphériques du repère ECEF et les coordonnées cartésiennes du repère du satellite. 
    
    - Fonctionne pour des coordonnées de vecteur
    
    - Cette fonction est la réciproque de Sat2Earth_cm()
    
    Attributs :
        - r (float)         Coordonnée selon r du point dans le repère ECEF  [km]
        - theta (float)     Coordonnée selon θ du point dans le repère ECEF  [deg]
        - phi (float)       Coordonnée selon φ du point dans le repère ECEF  [deg]
        - INC (float)       Inclinaison de l'orbite du satellite             [deg]
        - TA (float)        Anomalie vraie du satellite                      [deg]
        
    Sorties :
        - X (float)         Abscisse du point dans le repère du satellite    [m]
        - Y (float)         Ordonnée du point dans le repère du satellite    [m]
        - Z (float)         Côte du point dans le repère du satellite        [m]
    '''
    INC = INC*pi/180 # [rad]
    TA = TA*pi/180   # [rad]

    P = np.array([[r],[theta],[phi]]) # Vecteur position du point dans le repère terrestre fixe
        
    # Matrice de passage Sphérique vers Cartésien Sat
    R = np.array([[0, -sin(-INC*sin(TA)), cos(-INC*sin(TA))],
                  [0, -cos(-INC*sin(TA)), -sin(-INC*sin(TA))],
                  [1, 0, 0]])

    # Coordonnées du point P dans le repère du satellite
    [[X],[Y],[Z]] = np.dot(R,P)

    return X, Y, Z # [m]

#______________________________________________________________________________

def Sat2Earth_cm(X, Y, Z, INC, TA):
    '''
    Permet d'effectuer un changement de coordonnées entre les coordonnées
    cartésiennes du repère du satellite et les coordonnées sphériques du repère
    ECEF. 
    
    - Fonctionne pour des coordonnées de points
    
    - Cette fonction est la réciproque de Earth2Sat()
    
    Attributs :
        - X (float)         Abscisse du point dans le repère du satellite    [m]
        - Y (float)         Ordonnée du point dans le repère du satellite    [m]
        - Z (float)         Côte du point dans le repère du satellite        [m]
        - INC (float)       Inclinaison de l'orbite du satellite             [deg]
        - TA (float)        Anomalie vraie du satellite                      [deg]
        
    Sorties :
        - r (float)         Coordonnée selon r du point dans le repère ECEF  [km]
        - theta (float)     Coordonnée selon θ du point dans le repère ECEF  [deg]
        - phi (float)       Coordonnée selon φ du point dans le repère ECEF  [deg]
    '''  
    INC = INC*pi/180 # [rad]
    TA = TA*pi/180   # [rad]
        
    P = np.array([[X*10**-3],[Y*10**-3],[Z*10**-3]]) # [km] Vecteur position du point dans le repère du satellite
        
    # Matrice de passage Sphérique vers Cartésien Sat
    R = np.array([[0, -sin(-INC*sin(TA)), cos(-INC*sin(TA))],
                  [0, -cos(-INC*sin(TA)), -sin(-INC*sin(TA))],
                  [1, 0, 0]])
    R2 = np.linalg.inv(R) # Matrice de passage Cartésien Sat vers Sphérique
        
    # Coordonnées du point P dans le repère Sphérique 
    [[r],[theta],[phi]] = np.dot(R2,P) # [km] Vecteur position du point dans le repère terrestre fixe
        
    return r, theta, phi

