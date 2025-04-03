#scikit sklearn-genetic-opt?
#faire UI avec streamlit
from apprentissage import apprentissage
from optimisation import optimisation
from structure import Structure as St

"""À votre information : les barres de progrès fonctionnent moins bien dans un environnement de programmation
comme Pycharm par rapport à la console de windows."""

score, structure = apprentissage()
print("Score : ", score)

enc, poi, force = structure.montrer_performance()

print("Encombrement = ", enc, " m, poids = ", poi, " N, force = ", force, "N.")

structure.visualiser_structure()

score, structure_optimisee = optimisation(structure)
print("Score : ", score)

enc, poi, force = structure_optimisee.montrer_performance()

print("Encombrement = ", enc, " m, poids = ", poi, " N, force = ", force, "N.")

structure_optimisee.visualiser_structure()