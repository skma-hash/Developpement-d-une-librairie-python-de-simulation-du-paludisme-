# A package is a collection of python modules into a directory with a __init__.py
from Packages.Module1 import triple, perimetre 
from Packages.Module2 import mean 

print("Moyenne = ", mean([2, 1, 3]))
print("Perimetre = ", perimetre(4, 2))
print("Triple = ", triple(4))
