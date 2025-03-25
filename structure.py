import numpy as np
from random import random as ran

class Structure:

    def __init__(self, nombre_points=10, longueur_segments_max=1, longueur_segments_min=1, tridimentionnel = True):

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
        self.tridimentionnel = tridimentionnel

        # On initialise nos arrays.
        self.points = np.ndarray((self.nombre_points, 3))
        self.angles = np.ndarray((self.nombre_points - 1, 2))
        self.longueur_segments = np.ndarray(self.nombre_points - 1)

        # Si l'utilisateur n'entre pas de bonnes valeurs limites, on lève une erreur.
        if self.longueur_segments_min > self.longueur_segments_max or self.longueur_segments_min <= 0:

            raise Exception("La longueur minimale doit être plus grande que zéro et elle doit être plus courte ou égale à la longueur maximale.")

        # On définit une valeur aléatoire de théta (0 < theta < 2*pi) et phi (–pi/2 < phi < pi/2) pour chaque segment.
        self.angles[:, 0] = np.random.rand(self.nombre_points - 1) * 2 * np.pi
        self.angles[:, 1] = (np.random.rand(self.nombre_points - 1) - 0.5) * np.pi * self.tridimentionnel

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
        '''

        for i in range(self.nombre_points-1):

            self.points[i+1, :] = [self.points[i, 0] + self.longueur_segments[i] * np.sin(self.angles[i, 0]) * np.cos(self.angles[i, 1]),
                                   self.points[i, 1] + self.longueur_segments[i] * np.sin(self.angles[i, 0]) * np.sin(self.angles[i, 1]),
                                   self.points[i, 2] + self.longueur_segments[i] * np.cos(self.angles[i, 0])]

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
            self.angles[:, 1] = self.angles[:, 1] + (np.random.rand(self.nombre_points-1) - 0.5) * np.pi * temperature * self.tridimentionnel

        # On génère la structure à partir des longueurs et des angles modifiés
        self.generation_structure()

    def montrer_points(self):

        """
        On retourne les points composant notre structure.
        :return: Les points composant notre structure.
        """
        return self.points
