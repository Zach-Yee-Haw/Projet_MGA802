#scikit sklearn-genetic-opt?
import streamlit as st
from apprentissage import apprentissage
from optimisation import optimisation
from structure import Structure as St
import plotly as ply
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Initialiser les variables de session si elles n'existent pas
if 'score_apprentissage' not in st.session_state:
    st.session_state['score_apprentissage'] = None
if 'structure_apprentissage' not in st.session_state:
    st.session_state['structure_apprentissage'] = None


col1, col2, col3 = st.columns([1, 1, 2])

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

with col3:
    barre_de_progression = st.progress(0, text="Prêt")

    espace_performance= st.empty()
    espace_apprentissage = st.empty()
    espace_optimisation = st.empty()

structure = St()

with col1:
    nb_points = st.number_input('Nombre de points dans la structure : ', min_value=2, value=31)
    longueur_min = st.number_input('Longueur minimale des segments : ', min_value=0.0, value=100.0)
    longueur_max = st.number_input('Longueur maximale des segments : ', min_value=0.0, value=100.0)
    nb_structures = st.number_input('Nombre de structures à générer par itération : ', min_value=1, value=10)
    nb_structures_a_garder = st.number_input('Nombre de structures à garder par itération : ', min_value=1, value=4)
    nb_iterations = st.number_input('Nombre d\'itérations : ', min_value=2, value=10)
    temperature_debut = st.number_input('Température initiale : ', min_value=0.0, max_value=1.0, value=0.5)
    temperature_fin = st.number_input('Température finale : ', min_value=0.0, max_value=1.0, value=0.2)
    tridimensionnel = st.checkbox('Structure tridimensionnelle', value=True)
    induit = st.checkbox('Champs induit', value=False)
    a = st.number_input('Importance de l\'encombrement dans le calcul du score : ', min_value=0.0, value=0.5)
    b = st.number_input('Importance du poids dans le calcul du score : ', min_value=0.0, value=0.5)
    biais = st.number_input('Biais de sélection des structures : ', min_value=1, value=4)
    optimiser = st.checkbox('Optimiser la structure après l\'apprentissage', value=False)
    if optimiser == True:
        nb_iterations_optimisation = st.number_input('Nombre d\'itérations d\'optimisation : ', min_value=2, value=20)
        tolerance = st.number_input('Tolérance : ', min_value=0.0, max_value=1.0, value=0.01)

with col2:
    if st.button('Démarrer apprentissage'):
        score, structure = apprentissage(nb_points, longueur_max, longueur_min, nb_structures,
                      nb_structures_a_garder, nb_iterations, temperature_debut,
                      temperature_fin, tridimensionnel, induit, a, b, biais,
                      plyfig = performances_graph, barre_de_progression = barre_de_progression,
                      espace_graph=espace_performance)

        with espace_performance:
            st.plotly_chart(performances_graph, key="perf")

        print("Score : ", score)
        enc, poi, force = structure.montrer_performance()
        print("Encombrement = ", enc, " m, poids = ", poi, " N, force = ", force, "N.")
        structure.visualiser_structure(plyfig=structure_apprentissage_graph)

        with espace_apprentissage:
            st.plotly_chart(structure_apprentissage_graph, key="appr", use_container_width=False)


        if optimiser == True:
            barre_de_progression.progress(100,text="Optimisation en cours...")

            score, structure_optimisee = optimisation(structure, induit, a, b, tridimensionnel, nb_iterations = nb_iterations_optimisation, tolerance = tolerance)
            print("Score : ", score)

            enc, poi, force = structure_optimisee.montrer_performance()

            print("Encombrement = ", enc, " m, poids = ", poi, " N, force = ", force, "N.")

            structure_optimisee.visualiser_structure(plyfig=structure_optimisee_graph)

            with espace_optimisation:
                st.plotly_chart(structure_optimisee_graph, key="appr", use_container_width=False)

        barre_de_progression.progress(100, text="Terminé !")