from Boxels import *
import Dexels
from Geometry import *
from Conversion import *
from STLparser import *
from TestFunctions import *
l = loader()
l.load_stl("elephant.stl") #put the name of the file you want to boxelize here (it should be in the same folder)
file=stlToBoxels(l.model)
file=boxelsToDexels(file)
layers=Dexels.slice(file,4)