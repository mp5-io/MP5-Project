from numpy import *
from scipy import *

class DexelGrid: # definition of a grid of dexels
    def __init__(self):
        self.dexelArray=None # all the dexels are stored in a 3d array that represents their organization
        self.dexelSize=None
        self.xmax=None #this is to keep track of the actual coordinates (in mm) that will be usefull during G-code generation ; xmax-xmin/dexelSize should be an integer
        self.xmin=None
        self.ymax=None
        self.ymin=None
        self.zmax=None
        self.zmin=None
# with a good parser we could directly get a dexelGrid
    
def support(dexelGrid, requirements):
    ()
    # to be written, not useful at the moment since we don't have input
    # support has to be created before slicing
    # maybe it should become internal to the class dexelGrid
    # requirements is the list of settings wanted by the user
    
def infill(dexelGrid,requirements):
    ()
    # to be written, not useful at the moment since we don't have input
    # infill has to be created before slicing
    # maybe it should become internal to the class dexelGrid
    # requirements is the list of settings wanted by the user
    

def innerDexels(dexelGrid): #takes a 3d object (its surface) and gives the inner parts (helpful to generate the infill) the surface itself is not counted as inner part. Could be useful later
    (lenx,leny)=dexelGrid.dexelArray.shape
    grid = array(lenx, leny)#creating the grid
    for xi in range(lenx):
        for yi in range(leny): #filling it
            currentLength=len(dexelGrid.dexelArray[xi][yi])
            grid[xi][yi]=[]#this is to ensure that the use of append will work, so that it knows that it is a grid of lists. Don't know if it is necessary in Python but can be in other languages
            k=0
            while (2*k+1<currentLength):
                grid[xi][yi].append([dexelGrid.dexelArray[xi][yi][2*k][1],dexelGrid.dexelArray[xi][yi][2*k+1][0]])
                k+=1
    return grid
            
            
    
def filerepair(dexelGrid):
    ()
    # to be written, not useful at the moment since we don't have input
    # infill has to be created before slicing
    # maybe it should become internal to the class dexelGrid
    
def isFull(depthList, depthMin, depthMax): #takes a list of intervals and tells if there is one full boxel between depth1 (included) and depth2 (not included)
    length = len(depthList)
    currentInterval=0
    while (currentInterval<length):
        if (depthList[currentInterval][0]>=depthMax): 
            return False
        elif (depthList[currentInterval][1]>depthMin):
            return True
        currentInterval=currentInterval+1
    return False
    
def findGrid(dexelGrid, depth, thickness):
        # depth and thickness are only integer, we are counting in 'dexel unit'
        #maybe it should be internal to the class dexelGrid
    (lenx,leny)=dexelGrid.dexelArray.shape
    grid = zeros((lenx, leny), dtype=bool)#creating the grid
    for xi in range(lenx):
        for yi in range(leny): #filling it
            grid[xi][yi] = isFull(dexelGrid.dexelArray[xi][yi],depth, depth+thickness)
    return grid


def findDeepest(dexelGrid):
    (lenx,leny)=dexelGrid.dexelArray.shape
    deepest=0
    for xi in range(lenx):
        for yi in range(leny):
            print(dexelGrid.dexelArray[xi][yi])
            if (dexelGrid.dexelArray[xi][yi]!=[]):
                deepest=max(deepest,dexelGrid.dexelArray[xi][yi][-1][1])
    return deepest
    
def slice(dexelGrid, thickness): #slicing, without the G-code generation
#maybe it should be internal to the class dexelGrid
    (lenx,leny)=dexelGrid.dexelArray.shape
    lenz=findDeepest(dexelGrid)
    depth=0
    layerlist=[]
    while (depth<lenz):
        layerlist.append(findGrid(dexelGrid, depth, thickness)) 
        depth=depth+thickness
    return layerlist 
        
    

            
    