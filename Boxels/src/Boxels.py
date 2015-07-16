from numpy import *
from scipy import *
from Metadata import *
class Boxel: #this is how a boxel is represented
    def __init__(self, x, y, z, size, isFull, metadata):
        self.x=x
        self.y=y
        self.z=z
        self.size=size
        self.metadata=metadata
        self.isFull=isFull #a boolean

class BoxelSet: # definition of an ordered set of Boxels
    def __init__(self):
        self.boxelArray= None
        self.boxelSize=None
        self.xmax=None#this is to keep track of the actual coordinates (in mm) that will be usefull during G-code generation ; xmax-xmin/boxelSize should be an integer
        self.xmin=None
        self.ymax=None
        self.ymin=None
        self.zmax=None
        self.zmin=None
# with a good parser we could directly get a BoxelSet
    
def support(boxelSet, requirements):
    # to be written, not useful at the moment since we don't have input
    # support has to be created before slicing
    # maybe it should become internal to the class BoxelSet
    # requirements is the list of settings wanted by the user
    ()
    
def infill(boxelSet,requirements):
    # to be written, not useful at the moment since we don't have input
    # infill has to be created before slicing
    # maybe it should become internal to the class BoxelSet
    # requirements is the list of settings wanted by the user
    ()
    
def filerepair(boxelSet):
    # to be written, not useful at the moment since we don't have input
    # infill has to be created before slicing
    # maybe it should become internal to the class BoxelSet
    ()
    
def findLayer(boxelSet, height, thickness):
        # height and thickness are only integer, we are counting in 'boxel unit'
        #maybe it should be internal to the class BoxelSet
        return boxelSet.boxelArray[:,:,height:height+thickness]
        
def layertogrid(layer):
    (lenx,leny,lenz)=layer.shape
    grid = array(lenx, leny)#creating the grid
    for xi in range(lenx):
        for yi in range(leny): #filling it
            isFull = False
            for zi in range(lenz):
                if layer[xi][yi][zi].isFull: isFull=True
            grid[xi][yi]=isFull
    return grid
# one can easily add the metadata to the grid
#maybe it should be merged with findLayer


def slice(boxelSet, thickness): #slicing, without the G-code generation
#maybe it should be internal to the class BoxelSet
    (lenx,leny,lenz)=boxelSet.shape
    height=0
    layerlist=[]
    while (height<lenz):
        layer=findLayer(boxelSet, height, thickness)
        grid=layertogrid(layer)
        list.append(grid) # the last 3 lines could be sumed up in 1 operation, not wasting memory, it is just for readability 
        height=height+thickness
    return layerlist 
        
        
    

            
    