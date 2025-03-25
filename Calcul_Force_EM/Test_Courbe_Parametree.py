import numpy as np
from datetime import datetime
from math import pi
from astropy import constants

import Force_Electro as fe
import ChampMagnetique as cm
import Cable as ca
import Satellite
from Materiaux import Al_2024

# Données______________________________________________________________________

# Constantes
R_T = constants.R_earth.value # [m] Rayon de la Terre
M_T = constants.M_earth.value # [kg] Masse de la Terre
G = constants.G.value # [m^3/kg/s²] Constante Universelle de Gravitation
mu = G * M_T # [m^3/s²] Paramètre Gravitationnel Standard de la Terre

# Caractéristiques du matériau
Al = Al_2024()
rho = Al.MasseVolumique()
res = Al.Resistivite()

# Caractéristiques du câble 
d = 5                    # [mm] Diamètre du câble
S = pi*((d*10**-3)/2)**2 # [m²] Surface de la section du câble

D = 2000 # [m] Diamètre du cercle formé par le câble
L = pi*D # [m] Longueur du câble

R = ca.Resistance(L, S, res)    # [Ohm] Résistance électrique du câble
Vol = ca.Volume(L,S)            # [m^3] Volume totale du câble
m = ca.Masse(Vol,rho)           # [kg] Masse du câble

# 1er Cas : Câble Paramétré____________________________________________________

# Définition de la courbe paramétrée
t = np.linspace(-pi,pi,50)
x = 500*(np.sin(t)-1)
y = 1000*np.cos(t)
z = 500*np.sqrt(3)*(np.sin(t)-1)

# Position du satellite
r = R_T*10**-3 + 800 # [km] 
theta = 114          # [deg]
phi = 168            # [deg]
INC = 25             # [deg]
TA = 180             # [deg]
date = datetime(2020,7,15,15,20,0)

V = np.sqrt(mu/(r*10**3)) # [m/s] Vitesse du satellite sur son orbite

# Calcul de la force de Lorentz générée
F1a, Bi1a, F1a_i = fe.Parametre(r, theta, phi, date, INC, TA, x, y, z, None, V, R) # Cas induit
F1b, Bi1b, F1b_i = fe.Parametre(r, theta, phi, date, INC, TA, x, y, z, 1.5, V, R)  # Cas imposé

print(' _________________________________________________')
print(' Cas 1 : Câble paramétré en cercle')
print('')
print(' Cas induit :')
print('   F   = ',F1a,' N')
print(' ||F|| = ',np.linalg.norm(F1a),' N')
print('')
print(' Cas imposé :')
print('   F   = ',F1b,' N')
print(' ||F|| = ',np.linalg.norm(F1b),' N')
print(' _________________________________________________')
print('')

# 2e Cas : Câble défini par morceaux__________________________________________

# Définition du câble
x1 = np.linspace(0,-1000,51)
x1 = np.delete(x1,-1)
x2 = np.linspace(-1000,0,50)
xx = np.concatenate((x1,x2))

y1 = np.linspace(0,1000,26)
y1 = np.delete(y1,-1)
y2 = np.linspace(1000,0,26)
y2 = np.delete(y2,-1)
y3 = np.linspace(0,-1000,26)
y3 = np.delete(y3,-1)
y4 = np.linspace(-1000,0,25)
yy = np.concatenate((y1,y2,y3,y4))

zz = np.sqrt(3)*xx


# Calcul de la force de Lorentz générée
F2a, Bi2a, F2a_i = fe.Parametre(r, theta, phi, date, INC, TA, xx, yy, zz, None, V, R) # Cas induit
F2b, Bi2b, F2b_i = fe.Parametre(r, theta, phi, date, INC, TA, xx, yy, zz, 1.5, V, R)  # Cas imposé

print(' ______________________________________________________________')
print(' Cas 2 : Câble définit par morceaux')
print('')
print(' Cas induit :')
print('   F   = ',F2a,' N')
print(' ||F|| = ',np.linalg.norm(F2a),' N')
print('')
print(' Cas imposé :')
print('   F   = ',F2b,' N')
print(' ||F|| = ',np.linalg.norm(F2b),' N')
print(' ______________________________________________________________')
print('')

# 3e Cas : Câble soumis à un champ magnétique uniforme_________________________

# Définition du champ magnétique
B = cm.ChampMagnetique(r, theta, phi, date)
B = Satellite.Earth2Sat_cm(B[0], B[1], B[2], INC, TA) # [T]

# Définition du câble (le même que le cas 2)
cable = np.array([xx,yy,zz])

F3 = 0 
for i in range(len(xx)-1):
    cable_i = np.array([[cable[0][i],cable[1][i],cable[2][i]],[cable[0][i+1],cable[1][i+1],cable[2][i+1]]])
    F3 = F3 + fe.ForceElectro(B, cable_i, 1.5, V, R)

print(' _____________________________________________________________')
print(' Cas 3 : Câble soumis à un champ magnétique uniforme')
print('')
print(' Cas imposé :')
print('   F   = ',F3,' N')
print(' ||F|| = ',np.linalg.norm(F3),' N')
print(' _____________________________________________________________')
print('')

#%%
ca.Graph(x,y,z, 'Câble paramétré : cercle, cas induit I = 1.5 A', F1b_i, Bi1b) # Représentation 3D de la courbe
ca.Graph(xx,yy,zz, '  Câble défini par morceaux: losange, cas induit I = 1.5 A', F2b_i, Bi2b) # Représentation 3D de la courbe