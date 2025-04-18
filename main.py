from apprentissage import apprentissage
from optimisation import optimisation
from structure import Structure as St
import plotly.graph_objects as go

# Initialisation des objets graphiques pour les visualisations
performances_graph = go.FigureWidget(go.Figure())
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

performances_graph.show()
structure_apprentissage_graph.show()
structure_optimisee_graph.show()

# Configuration des entrées
nb_points = 31
longueur_min = 100.0
encombrement_cible = 500.0
longueur_max = 100.0
nb_structures = 10
nb_structures_a_garder = 4
nb_iterations = 10
temperature_debut = 0.5
temperature_fin = 0.2
tridimensionnel = True
induit = False
b = 0.5
biais = 4
optimiser = True
nb_iterations_optimisation = 20
tolerance = 0.01
enregistrement = True

# Lancer le processus d'apprentissage
score, structure = apprentissage(nb_points, longueur_max, longueur_min, nb_structures,
                nb_structures_a_garder, nb_iterations, temperature_debut,
                temperature_fin, encombrement_cible, tridimensionnel, induit, b, biais,
                plyfig = performances_graph, figure=structure_apprentissage_graph)

# Afficher les performances de la structure après apprentissage
enc, poi, force = structure.montrer_performance()
titre = "Score : " + str(score) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) + ", force = " + str(force) + "."
structure.visualiser_structure(plyfig=structure_apprentissage_graph, titre=titre)
# AFFICHER GRAPHIQUE STRUCTURE

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


# Enregistrement de la structure
if enregistrement == True:
    structure_optimisee.sauvegarde()

# Mettre à jour la barre de progression pour indiquer la fin'
print("Terminé !")
