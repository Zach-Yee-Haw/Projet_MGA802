import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from math import pi
from astropy import constants

import Calcul_Force_EM.Force_Electro as fe
import Calcul_Force_EM.Cable as ca
from Calcul_Force_EM.Materiaux import Al_2024
from Calcul_Force_EM.Geometrie_fct import *

class Structure:

    def __init__(self, nombre_points=10, longueur_segments_max=100, longueur_segments_min=100, encombrement_cible=500, tridimensionnel = True, nom = ""):
        """
        Initialisation de la classe Structure.
        Cette classe représente les structures que nous voulons générer, puis évaluer.

        :param nombre_points: Nombre de nœuds dans la structure.
        :type nombre_points: int
        :param longueur_segments_max: Longueur maximale des segments.
        :type longueur_segments_max: float
        :param longueur_segments_min: Longueur minimale des segments.
        :type longueur_segments_min: float
        :param tridimensionnel: Indique si la structure est en 3D ou non.
        :type tridimensionnel: bool
        :param nom: Nom de l'instance de la structure.
        :type nom: str
        """

        # Initialisation des paramètres principaux de la structure
        self.nombre_points = nombre_points
        self.longueur_segments_max = longueur_segments_max
        self.longueur_segments_min = longueur_segments_min
        self.encombrement_cible = encombrement_cible
        self.tridimensionnel = tridimensionnel
        self.poids = 0
        self.force_induit = 0
        self.force_impose = 0
        self.encombrement_max = 0
        self.nom = nom
        self.Fx_induit = 0
        self.Fx_impose = 0

        # Initialisation des tableaux pour stocker les propriétés géométriques
        self.points = np.ndarray((self.nombre_points, 3))
        self.angles = np.ndarray((self.nombre_points - 1, 2))
        self.longueur_segments = np.ndarray(self.nombre_points - 1)
        self.encombrements = np.zeros_like(self.longueur_segments)

        # Validation des longueurs minimales et maximales
        if self.longueur_segments_min > self.longueur_segments_max or self.longueur_segments_min <= 0:

            raise Exception("La longueur minimale doit être plus grande que zéro et elle doit être plus courte ou égale à la longueur maximale.")

        # Génération aléatoire des angles theta (azimutal) et phi (élévation)
        self.angles[:, 0] = np.random.rand(self.nombre_points - 1) * 2 * np.pi
        self.angles[:, 1] = (np.random.rand(self.nombre_points - 1) - 0.5) * np.pi * self.tridimensionnel

        # Génération aléatoire des longueurs de segments dans les limites définies
        self.longueur_segments[:] = np.random.rand(self.nombre_points - 1) * (self.longueur_segments_max - self.longueur_segments_min) + self.longueur_segments_min

        # Initialisation du premier point à l'origine
        self.points[0, :] = [0, 0, 0]

        # Génération de la structure
        self.generation_structure()

    def __str__(self):
        """
        Permet de représenter une instance par son nom dans les impressions.
        """
        return self.nom

    def __repr__(self):
        """
        Représentation concise pour les impressions.
        """
        return self.nom

    def __copy__(self):
        """
        Sert à copier la structure. En fait, on utilise deepcopy pour faire cela, mais bon c'est bien d'avoir l'option, au cas où.

        :return: La structure
        :rtype: Structure
        """
        return self

    def generation_structure(self):
        """
        À partir des angles et des longueurs de segments que nous avons générés, nous trouvons les points qui les composent.

        :return: Une liste de points composant notre structure.
        :rtype: ndarray
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
        self.points = self.points * self.encombrement_cible / self.encombrement_max
        self.longueur_segments = self.longueur_segments * self.encombrement_cible / self.encombrement_max
        self.poids = self.longueur_segments.sum()
        self.encombrement_max = self.encombrement_cible
        self.evaluer_force()

    def montrer_performance(self, induit = False):
        """
        Cette fonction sert à fournir les indices de performance de notre structure.

        :param induit: Détermine si notre calcul de force est induit ou imposé
        :type induit: bool

        :return: Nos indices de performance
        :rtype: tuple
        """
        if induit:
            return self.encombrement_max, self.poids, self.Fx_induit
        else:
            return self.encombrement_max, self.poids, self.Fx_impose

    def appliquer_limites(self, valeur, limite_min, limite_max):
        """
        Cette fonction sert à prendre une fonction en entrée, à vérifier si elle entre dans le limites et si ce n'est
        pas le cas, à changer cette valeur afin qu'elle entre dans les limite avec la même différence qu'elle avait en
        y sortant.

        :param valeur: Notre valeur à tester.
        :type valeur: float
        :param limite_min: Notre limite inférieure.
        :type limite_min: float
        :param limite_max: Notre limite supérieure.
        :type limite_max: float

        :return: Notre valeur qui rentre désormais dans nos limites.
        :rtype: float
        """
        if valeur > limite_max:

            valeur = 2 * limite_max - valeur

        elif valeur < limite_min:

            valeur = 2 * limite_min - valeur

        return valeur

    def appliquer_limites_aggressif(self, valeur, limite_min, limite_max):
        """
        Cette fonction sert à prendre une fonction en entrée, à vérifier si elle entre dans le limites et si ce n'est
        pas le cas, à changer cette valeur afin qu'elle soit égale à la limite.

        :param valeur: Notre valeur à tester.
        :type valeur: float
        :param limite_min: Notre limite inférieure.
        :type limite_min: float
        :param limite_max: Notre limite supérieure.
        :type limite_max: float

        :return: Notre valeur qui rentre désormais dans nos limites.
        :rtype: float
        """
        if valeur > limite_max:

            valeur = limite_max

        elif valeur < limite_min:

            valeur = limite_min

        return valeur

    def modifier_parametres(self, temperature=0.05, longueur = True, angle = True, plus_nom = None):
        """
        Cette fonction permet de modifier les caractéristiques de notre structure selon une température définit.

        :param temperature: Cette variable permet de choisir l'ampleur de la variation selon laquelle nos structures vont changer.
        :type temperature: float
        :param longueur: Cette variable décide si l'on veut faire varier les longueurs.
        :type longueur: bool
        :param angle: Cette variable décide si l'on veut faire varier les angles.
        :type angle: bool
        :param plus_nom: ajout au nom de la structure.
        :type plus_nom: str
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

            self.angles[:, 0] = np.mod(self.angles[:, 0] + (np.random.rand(self.nombre_points-1) - 0.5) * 2 * np.pi * temperature, 2 * np.pi) * self.tridimensionnel
            self.angles[:, 1] = self.angles[:, 1] + (np.random.rand(self.nombre_points-1) - 0.5) * np.pi * temperature


        # On ajoute une partie au nom pour identifier les racines
        if plus_nom != None: self.nom = self.nom + "." + str(plus_nom)

        # On génère la structure à partir des longueurs et des angles modifiés
        self.generation_structure()

    def montrer_parametres(self):
        """
        Cette fonction sert à montrer les paramètres de la structure afin d'obtenir un point initial pour l'optimisation.

        :return: les longueurs et les angles des éléments de notre structure.
        :rtype: numpy ndarray
        """
        return self.longueur_segments, self.angles

    def redefinir_parametres(self, params, induit = False, b = 1, tridimensionnel = True, biais = 5):
        """
        Cette fonction sert à prendre des paramètres en entrée, à générer la structure à partir de ces paramètres puis à
        l'évaluer selon les critères choisis.

        :return: le score de la structure
        :rtype: float
        """
        # On extrait nos ndarrays de longueurs et d'angles à partir des paramètres.
        nb_segments = self.nombre_points - 1

        self.longueur_segments = params[0:nb_segments]
        self.angles[:, 0] = tridimensionnel*params[nb_segments:nb_segments * 2]
        self.angles[:, 1] = params[nb_segments * 2:nb_segments * 3]

        # On s'assure que les longueurs de segments conviennent aux limites que nous avons définies.
        for i in range(self.nombre_points-1):
            self.longueur_segments[i] = self.appliquer_limites_aggressif(self.longueur_segments[i],
                                                                         self.longueur_segments_min,
                                                                         self.longueur_segments_max)

        # On génère la structure, puis on évalue son score.
        self.generation_structure()
        encombrement, poids, force = self.montrer_performance(induit)
        score = (force/(poids**b))**-biais

        return score

    def montrer_points(self):
        """
        On retourne les points composant notre structure.

        :return: Les points [x, y, x] composant notre structure.
        :rtype: ndarray
        """
        return self.points

    def evaluer_force(self):
        """
        Calcule la force générée par la structure.
        """
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
        I = 1.5  # Courant imposé dans le câble [A]

        # Diamètre qui varie
        F1a, B1a, F1a_i = fe.Parametre(r, theta, phi, date, INC, TA, self.x, self.y, self.z, None, V, R)  # Cas induit
        F1a_norm_vector.append(np.linalg.norm(F1a))  # Pour chaque
        F1b, B1b, F1b_i = fe.Parametre(r, theta, phi, date, INC, TA, self.x, self.y, self.z, I, V, R)  # Cas imposé
        F1b_norm_vector.append(np.linalg.norm(F1b))

        self.force_induite = np.linalg.norm(F1a)
        self.force_impose = np.linalg.norm(F1b)
        self.Fx_induit = -F1a[0]
        self.Fx_impose = -F1b[0]

        self.F1b_i = F1b_i
        self.B1b = B1b
        self.vect_cable_i = vect_cable_i

    def visualiser_structure(self, plyfig = None, titre = None):
        """
        On ajoute un tracé 3D de notre structure à la figure désirée.

        :param plyfig: Figure sur laquelle nous voulons tracer.
        :type plyfig: Figure plotly
        :param titre: Titre que nous voulons donner à notre structure.
        :type titre: str
        """
        if plyfig != None:
            # Réinitialisation de la figure
            plyfig.data = []
            # Ajout du satellite dans la figure
            plyfig.add_trace(go.Scatter3d(
                x=[0], y=[0], z=[0],
                marker=dict(size=4,
                            color="red"),
                name="Satellite"))
            # Ajout de la structure dans la figure
            plyfig.add_trace(go.Scatter3d(
                x=self.x, y=self.y, z=self.z,
                marker=dict(size=1,
                            color="cyan"),
                line=dict(color="cyan",
                          width=2),
                name="Câble"))
            # On ajoute le titre
            plyfig.update_layout(title=titre)

    def sauvegarde(self, nom_a_donner = None, delimiteur = ","):
        """
        Sert à sauvegarder les points définissant la structure.

        :param nom_a_donner: nom que le fichier va avoir.
        :type nom_a_donner: str
        :param delimiteur: séparateur entre les données
        :type delimiteur: str
        """
        # Initialisation du nom
        fichier = nom_a_donner


        # Si aucun nom n'est donné, on en génère un
        if fichier == None:
            date = str(datetime.now())
            date = date.replace(" ", "_")
            date = date.replace(".", "_")
            date = date.replace(":", "-")
            fichier = "Structures\\Structure_" + date

        # Génération des noms
        nom_points = fichier + "_points.csv"
        nom_parametres = fichier + "_parametres.csv"

        # Génération des points
        points = self.montrer_points()
        parametres = np.ndarray((self.nombre_points - 1, 3))
        parametres[:, 0] = self.longueur_segments[:]
        parametres[:, 1] = self.angles[:, 0]
        parametres[:, 2] = self.angles[:, 1]

        # Sauvegarde de la structure
        np.savetxt(nom_points, points, delimiter=delimiteur)
        np.savetxt(nom_parametres, parametres, delimiter=delimiteur)
