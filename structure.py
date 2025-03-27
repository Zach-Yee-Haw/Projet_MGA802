import numpy as np
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from math import pi
from astropy import constants

import Calcul_Force_EM.Force_Electro as fe
import Calcul_Force_EM.ChampMagnetique as cm
import Calcul_Force_EM.Cable as ca
import Calcul_Force_EM.Satellite
from Calcul_Force_EM.Materiaux import Al_2024
from Calcul_Force_EM.Cable import *
from Calcul_Force_EM.Geometrie_fct import *

class Structure:

    def __init__(self, nombre_points=10, longueur_segments_max=1, longueur_segments_min=1, tridimensionnel = True):

        """
        Cette classe représente les structures que nous voulons générer, puis évaluer.
        :param nombre_points: On choisit le nombre de nœuds que nous voulons trouver dans la structure.
        :param longueur_segments_max: On choisit la longueur maximale que nos segments pourront prendre.
        :param longueur_segments_min:  On choisit la longueur minimale que nos segments pourront prendre.
        """

        # On définit nos paramètres.
        self.nombre_points = nombre_points
        self.longueur_segments_max = longueur_segments_max
        self.longueur_segments_min = longueur_segments_min
        self.tridimensionnel = tridimensionnel
        self.poids = 0
        self.force_induit = 0
        self.force_impose = 0
        self.encombrement_max = 0

        # On initialise nos arrays.
        self.points = np.ndarray((self.nombre_points, 3))
        self.angles = np.ndarray((self.nombre_points - 1, 2))
        self.longueur_segments = np.ndarray(self.nombre_points - 1)
        self.encombrements = np.zeros_like(self.longueur_segments)

        # Si l'utilisateur n'entre pas de bonnes valeurs limites, on lève une erreur.
        if self.longueur_segments_min > self.longueur_segments_max or self.longueur_segments_min <= 0:

            raise Exception("La longueur minimale doit être plus grande que zéro et elle doit être plus courte ou égale à la longueur maximale.")

        # On définit une valeur aléatoire de théta (0 < theta < 2*pi) et phi (–pi/2 < phi < pi/2) pour chaque segment.
        self.angles[:, 0] = np.random.rand(self.nombre_points - 1) * 2 * np.pi
        self.angles[:, 1] = (np.random.rand(self.nombre_points - 1) - 0.5) * np.pi * self.tridimensionnel

        # On définit une valeur aléatoire de longueur pour chaque segment.
        self.longueur_segments[:] = np.random.rand(self.nombre_points - 1) * (self.longueur_segments_max - self.longueur_segments_min) + self.longueur_segments_min

        # On initialise notre point initial à [0, 0, 0].
        self.points[0, :] = [0, 0, 0]

        # On génère la structure à partir des longueurs et des angles générés.
        self.generation_structure()

    def generation_structure(self):

        """
        À partir des angles et des longueurs de segments que nous avons générés, nous trouvons les points qui les composent.
        :return: Une liste de points composant notre structure.
        """

        '''
        À partir de [0, 0, 0], on additionne les coordonnées sphériques calculées à partir des longueurs et les angles générés.
        
        X(n+1) = X(n) + R * sin(theta) * cos(phi)
        Y(n+1) = Y(n) + R * sin(theta) * sin(phi)
        Z(n+1) = Z(n) + R * cos(theta)
        
        On boucle jusqu'à ce qu'on calcule tous nos points.
        
        À chaque point, on vérifie la distance par rapport à l'origine afin de trouver l'encombrement de chaque point.
        '''

        for i in range(self.nombre_points-1):

            self.points[i+1, :] = [self.points[i, 0] + self.longueur_segments[i] * np.sin(self.angles[i, 0]) * np.cos(self.angles[i, 1]),
                                   self.points[i, 1] + self.longueur_segments[i] * np.sin(self.angles[i, 0]) * np.sin(self.angles[i, 1]),
                                   self.points[i, 2] + self.longueur_segments[i] * np.cos(self.angles[i, 0])]

            self.encombrements[i] = (self.points[i+1, 0]**2 + self.points[i+1, 1]**2 +self.points[i+1, 2]**2)**0.5

        # À partir de l'encombrement de chaque point et des longueurs, nous trouvons l'encombrement max et le poids de la structure.
        self.encombrement_max = self.encombrements.max()
        self.poids = self.longueur_segments.sum()
        self.evaluer_force()

    def montrer_performance(self, induit = True):

        if induit:
            return self.encombrement_max, self.poids, self.force_induit
        else:
            return self.encombrement_max, self.poids, self.force_impose

    def appliquer_limites(self, valeur, limite_min, limite_max):

        """
        Cette fonction sert à prendre une fonction en entrée, à vérifier si elle entre dans le limites et si ce n'est
        pas le cas, à changer cette valeur afin qu'elle entre dans les limite avec la même différence qu'elle avait en
        y sortant.
        :param valeur: Notre valeur à tester.
        :param limite_min: Notre limite inférieure.
        :param limite_max: Notre limite supérieure.
        :return: Notre valeur qui rentre désormais dans nos limites.
        """

        if valeur > limite_max:

            valeur = 2 * limite_max - valeur

        elif valeur < limite_min:

            valeur = 2 * limite_min - valeur

        return valeur

    def modifier_parametres(self, temperature=0.05, longueur = True, angle = True):

        """
        Cette fonction permet de modifier les caractéristiques de notre structure selon une température définit.
        :param temperature: Cette variable permet de choisir l'ampleur de la variation selon laquelle nos structures vont changer.
        :param longueur: Cette variable décide si l'on veut faire varier les longueurs.
        :param angle: Cette variable décide si l'on veut faire varier les angles.
        """

        # Si on veut modifier la longueur, on applique une différence égale à (-1 à 1) * (max-min) * température
        if longueur:

            self.longueur_segments[:] = self.longueur_segments[:] + (np.random.rand(self.nombre_points-1) - 0.5) * 2 * (self.longueur_segments_max - self.longueur_segments_min) * temperature

            # Si notre longueur sort de ses bornes, on la ramène avec la même marge qu'elle dépassait.
            appliquer_limites_vectorise = np.vectorize(self.appliquer_limites)
            appliquer_limites_vectorise(self.longueur_segments, self.longueur_segments_min, self.longueur_segments_max)

        # Si on veut modifier les angles, on applique une différence égale à (-pi à pi) * température pour théta
        #                                                                 et (-pi/2 à pi/2) * température pour phi.
        if angle:

            self.angles[:, 0] = np.mod(self.angles[:, 0] + (np.random.rand(self.nombre_points-1) - 0.5) * 2 * np.pi * temperature, 2 * np.pi)
            self.angles[:, 1] = self.angles[:, 1] + (np.random.rand(self.nombre_points-1) - 0.5) * np.pi * temperature * self.tridimensionnel

        # On génère la structure à partir des longueurs et des angles modifiés
        self.generation_structure()

    def montrer_points(self):

        """
        On retourne les points composant notre structure.
        :return: Les points [x, y, x] composant notre structure.
        """
        return self.points

    def evaluer_force(self):

        #Rédigé par Dorian Stefan Dumitru

        # %% Données____________________________________________________________________

        # Constantes
        R_T = constants.R_earth.value  # [m] Rayon de la Terre
        M_T = constants.M_earth.value  # [kg] Masse de la Terre
        G = constants.G.value  # [m^3/kg/s²] Constante Universelle de Gravitation
        mu = G * M_T  # [m^3/s²] Paramètre Gravitationnel Standard de la Terre

        # Caractéristiques du matériau
        Al = Al_2024()
        rho = Al.MasseVolumique()
        res = Al.Resistivite()

        # %% Géométrie - Paramétrisation de la courbe___________________________________
        # Forme générée
        cable = self.points

        # Initialisation des points
        self.x = []
        self.y = []
        self.z = []
        L = 0

        # Initialisation des vecteurs entre les points
        # Vecteurs cartésiens normalisés
        x_vect = np.array([1, 0, 0])
        y_vect = np.array([0, 1, 0])
        z_vect = np.array([0, 0, 1])
        vect_cable_i = []

        # Initialisation des angles entre les points
        alpha_xy_range = []
        alpha_xz_range = []
        alpha_yz_range = []

        # Rotation du cable à partir de l'origine (satellite : [0,0,0]), selon Ry
        alpha = 30 * pi / 180  # rad

        # Réécriture des points selon l'angle alpha
        for i in range(len(cable)):
            x_i, z_i = rotate_origin_only(np.array([cable[i][0], cable[i][2]]), alpha)
            self.x.append(x_i)
            self.y.append(cable[i][1])
            self.z.append(z_i)
        cable = np.transpose(np.array([self.x, self.y, self.z]))

        # Calcul des vecteurs du câble et des angles entre les L_i
        for i in range(len(cable) - 1):
            vect_i = cable[i + 1] - cable[i]
            vect_cable_i.append(vect_i)
            # Norme du câble
            L += np.linalg.norm(vect_i)
            alpha_xy = angle_between(y_vect, vect_i)
            alpha_xy_range.append(np.degrees(alpha_xy))
            alpha_xz = angle_between(x_vect, vect_i)
            alpha_xz_range.append(np.degrees(alpha_xz))
            alpha_yz = angle_between(z_vect, vect_i)
            alpha_yz_range.append(np.degrees(alpha_yz))

        # Affichage des vecteurs pour vérifier leur sens pour le calcul d'angle
        vect_cable_i.append([0, 0, 0])  # Ajout d'un vecteur nul pour avoir mm nb de vecteurs que de points
        vect_cable_i = np.array(vect_cable_i)

        # Physique du câble
        d = 5  # [mm] Diamètre du câble
        S = pi * ((d * 10 ** -3) / 2) ** 2  # [m²] Surface de la section du câble
        R = ca.Resistance(L, S, res)  # [Ohm] Résistance électrique du câble
        Vol = ca.Volume(L, S)  # [m^3] Volume totale du câble
        m = ca.Masse(Vol, rho)  # [kg] Masse du câble

        # np.set_printoptions(precision=9)

        # %% Paramètres orbitaux - Position du satellite
        h = 800  # Altitude [km]
        r = R_T * 10 ** -3 + h  # [km]
        theta = 114  # [deg]
        phi = 168  # [deg]
        INC = 25  # [deg]
        TA = 180  # [deg]
        date = datetime(2020, 7, 15, 15, 20, 0)

        V = np.sqrt(mu / (r * 10 ** 3))  # [m/s] Vitesse du satellite sur son orbite

        # %% Calcul de la force de Lorentz générée
        F1a_norm_vector = []
        F1b_norm_vector = []
        I = 1.5  # Courant imposé dans la câble [A]

        # Diamètre qui varie
        F1a, B1a, F1a_i = fe.Parametre(r, theta, phi, date, INC, TA, self.x, self.y, self.z, None, V, R)  # Cas induit
        F1a_norm_vector.append(np.linalg.norm(F1a))  # Pour chaque
        F1b, B1b, F1b_i = fe.Parametre(r, theta, phi, date, INC, TA, self.x, self.y, self.z, I, V, R)  # Cas imposé
        F1b_norm_vector.append(np.linalg.norm(F1b))

        self.force_induite = np.linalg.norm(F1a)
        self.force_impose = np.linalg.norm(F1b)

        self.F1b_i = F1b_i
        self.B1b = B1b
        self.vect_cable_i = vect_cable_i

    def visualiser_structure(self):

        # Rédigé par Dorian Stefan Dumitru

        # %% Génération des graphiques
        # Force EM en 3D
        ca.Graph(self.x, self.y, self.z, 'Câble paramétré: Structure générée, cas imposé I = 1.5 A', self.F1b_i,
                 self.B1b)  # Représentation 3D de la courbe

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')
        # ax.scatter(0,0,0,'r')
        ax.scatter(self.x, self.y, self.z, 'b')
        plt.quiver(self.x, self.y, self.z, self.vect_cable_i[:, 0], self.vect_cable_i[:, 1], self.vect_cable_i[:, 2], length=1.0, normalize=False,
                   color='blue', label=r'$-\vec{I}$ [A]')
        plt.legend()
