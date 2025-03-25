'''
Ensemble de fonctions géométriques
- Rotation de points dans l'espace
- Calcul de vecteurs normalisés
- Calcul d'angles  entre deux vecteurs en 3D
'''

import numpy as np

def rotate_via_numpy(x, y, radians):
    """Use numpy to build a rotation matrix and take the dot product."""
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])
    return float(m.T[0]), float(m.T[1])

def rotate_origin_only(xy, radians):
    """Only rotate a point around the origin (0, 0)."""
    x, y = xy
    xx = x * np.cos(radians) + y * np.sin(radians)
    yy = -x * np.sin(radians) + y * np.cos(radians)

    return xx, yy

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def angle_between_vectors_cross(u, v):
    """
    Calculate the angle between two vectors using the cross product.

    Parameters:
    u, v : array-like
        Input vectors.

    Returns:
    tuple
        The angle between the vectors in radians and degrees.
    """
    u = np.array(u)
    v = np.array(v)
    
    cross_product = np.cross(u, v)
    magnitude_u = np.linalg.norm(u)
    magnitude_v = np.linalg.norm(v)
    magnitude_cross = np.linalg.norm(cross_product)
    
    sin_theta = magnitude_cross / (magnitude_u * magnitude_v)
    sin_theta = np.clip(sin_theta, -1.0, 1.0)  # Ensure sin_theta is within the valid range
    
    angle_radians = np.arcsin(sin_theta)
    angle_degrees = np.degrees(angle_radians)
    
    return angle_radians, angle_degrees