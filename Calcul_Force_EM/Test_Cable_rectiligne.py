import numpy as np
from datetime import datetime
from astropy import constants
from math import pi

import Force_Electro as fe
import ChampMagnetique as cm
import Satellite
import Cable as ca
from Materiaux import Al_2024

#%% Caractéristiques du matériau
Al = Al_2024()
rho = Al.MasseVolumique() # [kg/m^3] Masse volumique
res = Al.Resistivite()    # [Ohm.m] Résistivité électrique du matériaux

# Constantes
R_T = constants.R_earth.value # [m] Rayon de la Terre
M_T = constants.M_earth.value # [kg] Masse de la Terre
G = constants.G.value # [m^3/kg/s²] Constante Universelle de Gravitation
mu = G * M_T # [m^3/s²] Paramètre Gravitationnel Standard de la Terre

# Caractéristiques du câble
cable = np.array([[0,0,0],[-2000, 0, -3464]])
L = np.linalg.norm(cable)    # [m] Longueur du câble
d = 5                        # [mm] Diamètre du câble
S = pi*((d*10**-3)/2)**2     # [m²] Surface de la section du câble
R = ca.Resistance(L, S, res) # [Ohm] Résistance électrique du câble
Vol = ca.Volume(L,S)         # [m^3] Volume totale du câble
m = ca.Masse(Vol,rho)        # [kg] Masse du câble

np.set_printoptions(precision=9)

#%% 1er Cas : Avec la fonction ForceElectro() _________________________________

# Position du satellite
h = 800            # [km]
r = R_T*10**-3 + h # [km]
theta = 114        # [deg]
phi = 168          # [deg]
INC = 25           # [deg]
TA = 180           # [deg]
date = datetime(2020,7,15,15,20,0)

# Vitesse du satellite sur son orbite
V = np.sqrt(mu/(r*10**3)) # [m/s] Calcul de la vitesse du satellite sur son orbite

# Champ Magnétique terrestre au niveau du satellite
B = cm.ChampMagnetique(r, theta, phi, date)
B = Satellite.Earth2Sat_cm(B[0],B[1],B[2],INC,TA) # [T]

# Calcul de la force de Lorentz
F1a = fe.ForceElectro(B,cable,None,V,R) # Cas induit
F1b = fe.ForceElectro(B,cable,1.5,V,R)  # Cas imposé

#%% 2e Cas : Avec la fonction Discret() _________________________________________

# Calcul de la force de Lorentz
F2a = fe.Discret(r, theta, phi, date, INC, TA, cable, 50, None, V, R) # Cas imposé
F2b = fe.Discret(r, theta, phi, date, INC, TA, cable, 50, 1.5, V, R)  # Cas imposé

# 3e Cas : Avec la fonction Parametre() _______________________________________

# Définition de la courbe paramétrée
[x,y,z] = ca.Mat2Liste(cable, 50)

# Calcul de la force de Lorentz
F3a, B3i, F3a_i = fe.Parametre(r, theta, phi, date, INC, TA, x, y, z, None, V, R) # Cas induit
F3b, B3i, F3b_i = fe.Parametre(r, theta, phi, date, INC, TA, x, y, z, 1.5, V, R)  # Cas imposé

#%% Comparaison : _______________________________________________________________

print(' __________________________________________________________________________')
print(' Comparaisons des fonctions :')
print(' __________________________________________________________________________')
print(' Cas induit :')
print('                        F_x          F_y          F_z           ||F||')
print(' ForceElectro() :',F1a,' ',np.round(np.linalg.norm(F1a),9),' N')
print(' Discret()  :    ',F2a,' ',np.round(np.linalg.norm(F2a),9),' N')
print(' Parametre() :   ',F3a,' ',np.round(np.linalg.norm(F3a),9),'  N')
print(' __________________________________________________________________________')
print(' Cas imposé :')
print('                        F_x          F_y          F_z           ||F||')
print(' ForceElectro() :',F1b,' ',np.round(np.linalg.norm(F1b),9),' N')
print(' Discret()  :    ',F2b,' ',np.round(np.linalg.norm(F2b),9),' N')
print(' Parametre() :   ',F3b,' ',np.round(np.linalg.norm(F3b),9),' N')
print(' __________________________________________________________________________')

#%% Graphique 3D
ca.Graph(x,y,z, 'Câble paramétré : cercle, cas induit I = 1.5 A', F3b_i, B3i) # Représentation 3D de la courbe
