#scikit sklearn-genetic-opt?

from structure import Structure


a = Structure(10, 1, 1, True)
a.generation_structure()
print(a.points)
a.modifier_parametres(0.05, True, True)
a.generation_structure()
print(a.points)