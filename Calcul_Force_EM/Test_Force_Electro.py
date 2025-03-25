import numpy as np
from math import pi
import Force_Electro as fe
import Cable as ca
from Materiaux import Al_7075

# Caractéristiques du matériau 
Al = Al_7075()
rho = Al.MasseVolumique() # [kg/m^3] Masse volumique
res = Al.Resistivite()    # [Ohm.m] Résistivité électrique du matériaux

# Caractéristiques du câble
cable = np.array([[0,0,0],[-20*np.sqrt(3), 0, -20]]) # Pour avoir L = 40
L = np.linalg.norm(cable) # [m] Longueur du câble

d = 5 # [mm] Diamètre du câble
S = pi*((d*10**-3)/2)**2 # [m²] Surface de la section du câble

R = ca.Resistance(L, S, res) # [Ohm] Résistance électrique du câble

Vol = ca.Volume(L,S)  # [m^3] Volume totale du câble
m = ca.Masse(Vol,rho) # [kg] Masse du câble

V = 7.5 # [m/s] Vitesse de déplacement

B = np.array([0,1,0])*10**-3 # [T] Champ magnétique

I = 1.5 # [A] Intensité du courant

# Calcul de la force électrodynamique dans le cas d'un courant imposé
F1 = fe.ForceElectro(B, cable, I, V, R) 
# Calcul de la force électro dynamique dans le cas d'un courant induit
F2 = fe.ForceElectro(B, cable, None, V, R) 

print(' ________________________________________')
print(' Cas induit : F =')
print('')
print('',F2,' N')
print(' Norme = ',np.linalg.norm(F2))
print(' ________________________________________')
print(' Cas imposé : F =')
print('')
print('',F1,' N')
print(' Norme = ',np.linalg.norm(F1))
print(' ________________________________________')
