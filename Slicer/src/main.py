

from geometry import *
from STLparser import *
from slicing import *
from infill import *
from GCodeWriter import *
from PathGenerator import *

l = loader()
l.load_stl("figure.stl")
genereGCode("figure2",l.trList)



