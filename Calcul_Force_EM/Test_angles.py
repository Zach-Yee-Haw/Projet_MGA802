"""
Code qui peremt de vérifier les résultats des différentes fonctions de rotation 
d'angle définies dans 'Geometrie_fct.py'
"""

import numpy as np
from Geometrie_fct import *

#Vecteurs cartésiens normalisés
x_vect = np.array([1,0,0])
y_vect = np.array([0,1,0])
z_vect = np.array([0,0,1])

#Vecteur quelconque (qui peut être changé)
v_vect = -np.array([1,1,0])

alpha_xy = angle_between(x_vect, v_vect)
alpha_xy_2 = angle_between_vectors_cross(x_vect, v_vect)

alpha_xz = angle_between(y_vect, v_vect)
alpha_xz_2= angle_between_vectors_cross(y_vect, v_vect)

alpha_yz = angle_between(z_vect, v_vect)
alpha_yz_2 = angle_between_vectors_cross(z_vect, v_vect)

'''
angle_between() permet d'avoir des angles plus grands que pi/2, soit ce qu'on veut 
'''