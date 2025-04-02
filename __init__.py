#scikit sklearn-genetic-opt?
from apprentissage import apprentissage
from optimisation import optimisation
from structure import Structure as St

"""À votre information : les barres de progrès fonctionnent moins bien dans un environnement de programmation
comme Pycharm par rapport à la console de windows."""

score, structure = apprentissage()
print("Score : ", score)

enc, poi, force = structure.montrer_performance()

print("Encombrement = ", enc, ", poids = ", poi, ", force = ", force)

structure.visualiser_structure()

structure_optimisee = optimisation(structure)

enc, poi, force = structure_optimisee.montrer_performance()

print("Encombrement = ", enc, ", poids = ", poi, ", force = ", force)

structure_optimisee.visualiser_structure()