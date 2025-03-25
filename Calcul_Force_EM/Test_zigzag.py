import numpy as np
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from math import pi
from astropy import constants

import Force_Electro as fe
import ChampMagnetique as cm
import Cable as ca
import Satellite
from Materiaux import Al_2024
from Cable import *
from Geometrie_fct import *
#%% Données____________________________________________________________________

# Constantes
R_T = constants.R_earth.value # [m] Rayon de la Terre
M_T = constants.M_earth.value # [kg] Masse de la Terre
G = constants.G.value # [m^3/kg/s²] Constante Universelle de Gravitation
mu = G * M_T # [m^3/s²] Paramètre Gravitationnel Standard de la Terre

# Caractéristiques du matériau
Al = Al_2024()
rho = Al.MasseVolumique()
res = Al.Resistivite()

#%% Géométrie - Paramétrisation de la courbe___________________________________
#Forme Zig-Zag (hardcoded)
cable = np.array([[0,0,0],
                  [0, 0, -50],
                  [0, 0, -100],
                  [0, -250, -100],
                  [0, -500, -100],
                  [0, -500, -150],
                  [0, -500, -200],
                  [0, -250, -200],
                  [0, 0, -200],
                  [0, 250, -200],
                  [0, 500, -200],
                  [0, 500, -250],
                  [0, 500, -300],
                  [0, 250, -300],
                  [0, 0, -300],
                  
                  [0, -250, -300],
                  [0, -500, -300],
                  [0, -500, -350],
                  [0, -500, -400],
                  [0, -250, -400],
                  [0, 0, -400],
                  [0, 250, -400],
                  [0, 500, -400],
                  [0, 500, -450],
                  [0, 500, -500],
                  [0, 250, -500],
                  [0, 0, -500], 
                  
                  [0, -250, -500],
                  [0, -500, -500],
                  [0, -500, -550],
                  [0, -500, -600],
                  [0, -250, -600],
                  [0, 0, -600],
                  [0, 250, -600],
                  [0, 500, -600],
                  [0, 500, -650],
                  [0, 500, -700],
                  [0, 250, -700],
                  [0, 0, -700],
                  
                  [0, 0, -750],
                  [0, 0, -800]])

#Initialisation des points
x = []
y = []
z = []
L = 0

#Initialisation des vecteurs entre les points
#Vecteurs cartésiens normalisés
x_vect = np.array([1,0,0])
y_vect = np.array([0,1,0])
z_vect = np.array([0,0,1])
vect_cable_i = []

#Initialisation des angles entre les points
alpha_xy_range = []
alpha_xz_range = []
alpha_yz_range = []

#Rotation du cable à partir de l'origine (satellite: [0,0,0]), selon Ry
alpha = 30*pi/180 #rad

#Réécriture des points selon l'angle alpha
for i in range(len(cable)):
    x_i,z_i = rotate_origin_only(np.array([cable[i][0], cable[i][2]]), alpha)
    x.append(x_i)
    y.append(cable[i][1])
    z.append(z_i)
cable = np.transpose(np.array([x,y,z]))

#Calcul des vecteurs du câble et des angles entre les L_i
for i in range(len(cable) - 1):
      vect_i = cable[i+1] - cable[i]
      vect_cable_i.append(vect_i)
      #Norme du câble
      L += np.linalg.norm(vect_i)
      alpha_xy = angle_between(y_vect, vect_i)
      alpha_xy_range.append(np.degrees(alpha_xy))
      alpha_xz = angle_between(x_vect, vect_i)
      alpha_xz_range.append(np.degrees(alpha_xz))
      alpha_yz = angle_between(z_vect, vect_i)
      alpha_yz_range.append(np.degrees(alpha_yz))

#Affichage des vecteurs pour vérifier leur sens pour le calcul d'angle
vect_cable_i.append([0,0,0]) # Ajout d'un vecteur nul pour avoir mm nb de vecteurs que de points
vect_cable_i = np.array(vect_cable_i)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
# ax.scatter(0,0,0,'r')
ax.scatter(x,y,z,'b')
plt.quiver(x,y,z, vect_cable_i[:,0], vect_cable_i[:,1], vect_cable_i[:,2], length=1.0, normalize=False, color = 'blue', label = r'$-\vec{I}$ [A]')
plt.legend()

# Physique du câble
d = 5                        # [mm] Diamètre du câble
S = pi*((d*10**-3)/2)**2     # [m²] Surface de la section du câble
R = ca.Resistance(L, S, res) # [Ohm] Résistance électrique du câble
Vol = ca.Volume(L,S)         # [m^3] Volume totale du câble
m = ca.Masse(Vol,rho)        # [kg] Masse du câble

np.set_printoptions(precision=9)

#%% Paramètres orbitaux - Position du satellite
h = 800              # Altitude [km] 
r = R_T*10**-3 + h   # [km] 
theta = 114          # [deg]
phi = 168            # [deg]
INC = 25             # [deg]
TA = 180             # [deg]
date = datetime(2020,7,15,15,20,0)  

V = np.sqrt(mu/(r*10**3)) # [m/s] Vitesse du satellite sur son orbite

#%% Calcul de la force de Lorentz générée
F1a_norm_vector = []
F1b_norm_vector = []
I = 1.5 # Courant imposé dans la câble [A]

# Diamètre qui varie
F1a, B1a, F1a_i = fe.Parametre(r, theta, phi, date, INC, TA, x, y, z, None, V, R) # Cas induit
F1a_norm_vector.append(np.linalg.norm(F1a)) # Pour chaque 
F1b, B1b, F1b_i = fe.Parametre(r, theta, phi, date, INC, TA, x, y, z, I, V, R)  # Cas imposé
F1b_norm_vector.append(np.linalg.norm(F1b))


print(' _________________________________________________')
print(' Cas 1 : Câble paramétré ')
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

#%% Génération des graphiques
# Force EM en 3D
ca.Graph(x,y,z,'Câble paramétré: Zig-Zag, cas imposé I = 1.5 A', F1b_i, B1b) # Représentation 3D de la courbe
