import streamlit as st
from apprentissage import apprentissage
from optimisation import optimisation
from structure import Structure as St
import plotly.graph_objects as go

# Configuration de la mise en page de Streamlit
st.set_page_config(layout="wide")

# Initialisation des variables de session si elles n'existent pas
if 'score_apprentissage' not in st.session_state:
    st.session_state['score_apprentissage'] = None
if 'structure_apprentissage' not in st.session_state:
    st.session_state['structure_apprentissage'] = None

# Création de trois colonnes dans la mise en page
col1, col2, col3 = st.columns([1, 1, 2])

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

# Configuration des widgets dans la troisième colonne (col3)
with col3:
    barre_de_progression = st.progress(0, text="Prêt")  # Barre de progression
    espace_performance= st.empty()  # Espace pour afficher les performances
    espace_apprentissage = st.empty()  # Espace pour afficher les résultats d'apprentissage
    espace_optimisation = st.empty()  # Espace pour afficher les résultats d'optimisation

# Initialisation d'une instance de la classe Structure
structure = St()

# Configuration des entrées utilisateur dans la première colonne (col1)
with col1:
    nb_points = st.number_input('Nombre de points dans la structure : ', min_value=2, value=31)
    longueur_min = st.number_input('Longueur minimale des segments : ', min_value=0.0, value=100.0)
    encombrement_cible = st.number_input('Valeur cible de l\'encombrement : ', min_value=0.0, value=500.0)
    longueur_max = st.number_input('Longueur maximale des segments : ', min_value=0.0, value=100.0)
    nb_structures = st.number_input('Nombre de structures à générer par itération : ', min_value=1, value=10)
    nb_structures_a_garder = st.number_input('Nombre de structures à garder par itération : ', min_value=1, value=4)
    nb_iterations = st.number_input('Nombre d\'itérations : ', min_value=2, value=10)
    temperature_debut = st.number_input('Température initiale : ', min_value=0.0, max_value=1.0, value=0.5)
    temperature_fin = st.number_input('Température finale : ', min_value=0.0, max_value=1.0, value=0.2)
    tridimensionnel = st.checkbox('Structure tridimensionnelle', value=True)
    induit = st.checkbox('Champs induit', value=False)
    b = st.number_input('Importance du poids dans le calcul du score : ', min_value=0.0, value=0.5)
    biais = st.number_input('Biais de sélection des structures : ', min_value=1, value=4)
    optimiser = st.checkbox('Optimiser la structure après l\'apprentissage', value=True)
    if optimiser == True:  # Si l'optimisation est activée, afficher des paramètres supplémentaires
        nb_iterations_optimisation = st.number_input('Nombre d\'itérations d\'optimisation : ', min_value=2, value=20)
        tolerance = st.number_input('Tolérance : ', min_value=0.0, max_value=1.0, value=0.01)

# Gestion des actions utilisateur dans la deuxième colonne (col2)
with col2:
    if st.button('Démarrer apprentissage'):  # Bouton pour démarrer le processus d'apprentissage
        
        # Afficher le graphique d'apprentissage
        with espace_apprentissage:
            st.plotly_chart(structure_apprentissage_graph, key="appr", use_container_width=False)

        # Lancer le processus d'apprentissage
        score, structure = apprentissage(nb_points, longueur_max, longueur_min, nb_structures,
                      nb_structures_a_garder, nb_iterations, temperature_debut,
                      temperature_fin, encombrement_cible, tridimensionnel, induit, b, biais,
                      plyfig = performances_graph, barre_de_progression = barre_de_progression,
                      espace_graph=espace_performance, figure=structure_apprentissage_graph, espace_structure=espace_apprentissage)

        # Afficher les performances de la structure après apprentissage
        enc, poi, force = structure.montrer_performance()
        titre = "Score : " + str(score) + ", Encombrement = " + str(enc) + ", poids = " + str(poi) + ", force = " + str(
            force) + "."
        structure.visualiser_structure(plyfig=structure_apprentissage_graph, titre=titre)
        with espace_apprentissage:
            st.plotly_chart(structure_apprentissage_graph, use_container_width=False)

        # Si l'optimisation est activée, lancer le processus d'optimisation
        if optimiser == True:
            barre_de_progression.progress(100,text="Optimisation en cours...")
            score, structure_optimisee = optimisation(structure, induit=induit, b=b, tridimensionnel=tridimensionnel,
                                                        nb_iterations=nb_iterations_optimisation, tolerance = tolerance,
                                                        barre_de_progression=barre_de_progression, figure=structure_optimisee_graph,
                                                        espace=espace_optimisation)

            # Afficher les performances de la structure optimisée
            enc, poi, force = structure_optimisee.montrer_performance()
            titre = "Score : "+str(score)+", Encombrement = "+str(enc)+", poids = "+str(poi)+", force = "+str(force)+"."
            structure_optimisee.visualiser_structure(plyfig=structure_optimisee_graph, titre=titre)
            with espace_optimisation:
                st.plotly_chart(structure_optimisee_graph, key="opti", use_container_width=False)

        # Mettre à jour la barre de progression pour indiquer l'enregistrement'
        barre_de_progression.progress(100, text="Enregistrement en cours...")

        # Enregistrement de la structure
        structure_optimisee.sauvegarde()

        # Mettre à jour la barre de progression pour indiquer la fin'
        barre_de_progression.progress(100, text="Terminé !")
