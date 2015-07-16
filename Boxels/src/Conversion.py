from Boxels import *
from Dexels import *
from Geometry import *
from numpy import *
import time

def boxelsToDexels(boxelSet):
    (lenx,leny,lenz)=boxelSet.boxelArray.shape
    dexelGrid=DexelGrid()
    dexelGrid.dexelSize=boxelSet.boxelSize
    dexelGrid.dexelArray=ndarray((lenx,leny),dtype=list)
    for xi in range(lenx):
        for yi in range(leny):
            depthList=[]
            currentInterval=[]
            currentDepth=0
            dexelGrid.dexelArray[xi][yi]=[]
            
            while (currentDepth<lenz):
                if (boxelSet.boxelArray[xi][yi][currentDepth]):
                    stillFull=True
                    running = currentDepth+1
                    while (running<lenz)&(stillFull):
                        if (boxelSet.boxelArray[xi][yi][running]):
                            running+=1
                        else: 
                            stillFull=False
                    dexelGrid.dexelArray[xi][yi].append([currentDepth,running])
                    currentDepth=running
                else:
                    currentDepth+=1
    # one also needs to fill the other characteristics, but I'm not sure if it's necessary
    return dexelGrid
    
def dexelsToBoxels(dexelGrid):
    (lenx,leny)=dexelGrid.dexelArray.shape
    boxelSet=BoxelSet()
    boxelSet.boxelSize=dexelGrid.dexelSize
    boxelSet.boxelArray=array(lenx,leny,deepest(dexelGrid.dexelArray)+1)
    for xi in range(lenx):
        for yi in range(leny):
            currentInterval=0
            while (currentInterval<len(dexelGrid.dexelArray[xi][yi])):
                for zi in range(dexelGrid.dexelArray[xi][yi][currentInterval][0],dexelGrid.dexelArray[xi][yi][currentInterval][1]):
                    boxelSet.boxelArray[xi][yi][zi].isFull=True
    # one also needs to fill the other characteristics, but I'm not sure if it's necessary
    return boxelSet

def stlToBoxels(triangleList):
    start=time.time()
    boxelSet=BoxelSet()
    boxelSet.boxelSize=minimumSize(triangleList) # can be smaller, depends on precision
    (xmax,xmin,ymax,ymin,zmax,zmin)=boundaries(triangleList)
    boxelSet.xmax=xmax
    boxelSet.xmin=xmin
    boxelSet.ymax=ymax
    boxelSet.ymin=ymin
    boxelSet.zmax=zmax
    boxelSet.zmin=zmin
    lenx = ceil((xmax-xmin)/boxelSet.boxelSize)
    leny = ceil((ymax-ymin)/boxelSet.boxelSize)
    lenz = ceil((zmax-zmin)/boxelSet.boxelSize)
    boxelSet.boxelArray=zeros((lenx,leny,lenz),dtype=bool)
    limitsize=boxelSet.boxelSize/2 #prestoring the half size
    
    for index in range(len(triangleList)):
        #precreating needed objects
        triangle=triangleList[index]
        A=triangle.p1
        B=triangle.p2
        C=triangle.p3
        triangle.findNormal()
        n=triangle.normalVector
        vAB=defineVector(A,B)
        vAC=defineVector(A,C)
        vBC=defineVector(B,C)
        #defining the "boundary box"
        (maxx,minx,maxy,miny,maxz,minz)=triangle.boundaries()
        minix = int((minx-xmin)//(2*limitsize))
        maxix=int((maxx-xmin)//(2*limitsize))
        miniy = int((miny-ymin)//(2*limitsize))
        maxiy=int((maxy-ymin)//(2*limitsize))
        miniz = int((minz-zmin)//(2*limitsize))
        maxiz=int((maxz-zmin)//(2*limitsize))
        # and the loop
        ix=minix
        while (ix<=maxix):
            iy=miniy
            while (iy<=maxiy):
                iz=miniz
                while (iz<=maxiz):
                    if not (boxelSet.boxelArray[ix][iy][iz]): #is the boxel is full there is no need to check again if it intersects with a triangle
                        xcenter= xmin+(ix+0.5)*(2*limitsize)
                        ycenter= ymin+(iy+0.5)*(2*limitsize)
                        zcenter= zmin+(iz+0.5)*(2*limitsize)
                        center=Point(xcenter,ycenter,zcenter)
                        boxelSet.boxelArray[ix][iy][iz]=(center.distanceSquaredToTriangle(n,A,B,C,vAB,vAC,vBC,limitsize)<=(limitsize)*(limitsize))
                    iz+=1
                iy+=1
            ix+=1          
    print ("It took", time.time()-start, "seconds.") #just to see how much time it takes
    return boxelSet
            
    