#scikit sklearn-genetic-opt?
import streamlit as st
from apprentissage import apprentissage
from optimisation import optimisation

"""À votre information : les barres de progrès fonctionnent moins bien dans un environnement de programmation
comme Pycharm par rapport à la console de windows."""

col1, col2, col3 = st.columns(3)

with col1:
    nb_points = st.number_input('Nombre de points dans la structure : ', min_value=2, value=31)
    longueur_min = st.number_input('Longueur minimale des segments : ', min_value=0.0, value=100.0)
    longueur_max = st.number_input('Longueur maximale des segments : ', min_value=longueur_min, value=100.0)
    nb_structures = st.number_input('Nombre de structures à générer par itération : ', min_value=1, value=10)
    nb_structures_a_garder = st.number_input('Nombre de structures à garder par itération : ', min_value=1, value=4)
    nb_iterations = st.number_input('Nombre d\'itérations : ', min_value=1, value=10)
    temperature_debut = st.number_input('Température initiale : ', min_value=0.0, max_value=1.0, value=0.5)
    temperature_fin = st.number_input('Température finale : ', min_value=0.0, max_value=1.0, value=0.2)
    tridimensionnel = st.checkbox('Structure tridimensionnelle', value=True)
    induit = st.checkbox('Champs induit', value=False)
    a = st.number_input('Importance de l\'encombrement dans le calcul du score : ', min_value=0.0, value=0.5)
    b = st.number_input('Importance du poids dans le calcul du score : ', min_value=0.0, value=0.5)
    biais = st.number_input('Biais de sélection des structures : ', min_value=1, value=4)

if st.button('Démarrer apprentissage'):
    score, structure = apprentissage(nb_points, longueur_max, longueur_min, nb_structures,
                  nb_structures_a_garder, nb_iterations, temperature_debut,
                  temperature_fin, tridimensionnel, induit, a, b, biais,
                  montrer_perf = True)
    print("Score : ", score)

    enc, poi, force = structure.montrer_performance()

    print("Encombrement = ", enc, " m, poids = ", poi, " N, force = ", force, "N.")

    structure.visualiser_structure()

if st.button('Démarrer optimisation'):
    score, structure_optimisee = optimisation(structure)
    print("Score : ", score)

    enc, poi, force = structure_optimisee.montrer_performance()

    print("Encombrement = ", enc, " m, poids = ", poi, " N, force = ", force, "N.")

    structure_optimisee.visualiser_structure()