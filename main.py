from apprentissage import apprentissage
from optimisation import optimisation
from structure import Structure as St
import plotly.graph_objects as go

# Initialisation des objets graphiques pour les visualisations
performances_graph = go.Figure()
structure_apprentissage_graph = go.Figure(data=go.Scatter3d(
                x=[0], y=[0], z=[0],
                marker=dict(size=4,
                            color="red"),
                name="Satellite"))
structure_optimisee_graph = go.Figure(data=go.Scatter3d(
                x=[0], y=[0], z=[0],
                marker=dict(size=4,
                            color="red"),
                name="Satellite"))

# Configuration des entrées
nb_points = 31  # Nombre de points dans la structure
proportion_longueur = 1.0 # Longueur min / longueur max ----- doit être entre 0.0 et 1.0
encombrement_cible = 500.0 # Encombrement de la structure
nb_structures = 10 # Nombre de structures pas itération
nb_structures_a_garder = 4 # Nombre de structures par itération
nb_iterations = 10 # Nombre d'itérations à simuler
temperature_debut = 0.5 # Température initiale
temperature_fin = 0.2 # Température finale
tridimensionnel = True # Détermine si la structure est tridimensionnelle
induit = False # Détermine si le courant est induit ou imposé
b = 0.5 # Importance du poids dans le calcul du score
biais = 4 # Chance de conserver les meilleures structures
optimiser = True # Détermine si l'optimisation se déroule après l'apprentissage
nb_iterations_optimisation = 20 # Nombre d'itérations pendant l'optimisation
tolerance = 0.01 # Tolérance pendant l'optimisation
enregistrement = True # Détermine si la structure est enregistrée à la fin

# Initialisation des longueurs min et max
longueur_max = 100.0
longueur_min = longueur_max * proportion_longueur

# Lancer le processus d'apprentissage
score, structure = apprentissage(nb_points, longueur_max, longueur_min, nb_structures,
                nb_structures_a_garder, nb_iterations, temperature_debut,
                temperature_fin, encombrement_cible, tridimensionnel, induit, b, biais,
                plyfig=performances_graph, figure=structure_apprentissage_graph)

# Afficher les performances et la structure après apprentissage
performances_graph.show()
enc, poi, force = structure.montrer_performance()
titre = "Score : " + str(score) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) + ", force = " + str(force) + "."
structure.visualiser_structure(plyfig=structure_apprentissage_graph, titre=titre)
structure_apprentissage_graph.show()

# Si l'optimisation est activée, lancer le processus d'optimisation
if optimiser == True:
    print("Optimisation en cours...")
    score, structure_optimisee = optimisation(structure, induit=induit, b=b, tridimensionnel=tridimensionnel,
                                                nb_iterations=nb_iterations_optimisation, tolerance = tolerance,
                                                figure=structure_optimisee_graph)

    # Afficher les performances de la structure optimisée
    enc, poi, force = structure_optimisee.montrer_performance()
    titre = "Score : "+str(score) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) + ", force = " + str(force) + "."
    structure_optimisee.visualiser_structure(plyfig=structure_optimisee_graph, titre=titre)
    structure_optimisee_graph.show()


# Enregistrement de la structure
if enregistrement == True:
    structure_optimisee.sauvegarde()

# Mettre à jour la barre de progression pour indiquer la fin'
print("Terminé !")
