#scikit sklearn-genetic-opt?

from structure import Structure

a = Structure(10, 1000, 100, True)
print(a.points)
print(a.montrer_performance(False))
a.modifier_parametres(0.05, True, True)
print(a.points)
print(a.montrer_performance(False))