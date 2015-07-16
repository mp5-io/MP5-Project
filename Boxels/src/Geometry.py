from numpy import *
from scipy import *
import time
import copy


## Geometric 3D objects    

class Point:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        self.label=None
        
    def translate(self,vector):
        self.x+=vector.x
        self.y+=vector.y
        self.z+=vector.z
        
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"
    
    #The following functions are made for boxelization
    
    def distanceSquaredFromCoplanarTriangle(self,A,B,C,vAB,vAC,vBC):
         #the three points and the 3 vectors are precreated to decrease computation time
        vPA=defineVector(self,A)
        vPB=defineVector(self,B)
        vPC=defineVector(self,C)
        toA=scalarproduct(vPA,vPA)
        toB=scalarproduct(vPB,vPB)
        toC=scalarproduct(vPC,vPC)
        toAB=float('inf')
        toAC=float('inf')
        toBC=float('inf')
        
        def isCloserToSegment(pt1,pt2,v): #takes to pts, and the vector defined by these points (to decrease computation time) and tells if main pt is closer from the segment than the bounding points
            v1=defineVector(pt1,self)
            v2=defineVector(self,pt2)
            return (scalarproduct(v1,v)>0)&(scalarproduct(v2,v)>0)
        if isCloserToSegment(A,B,vAB):
            
            toAB=toA-(scalarproduct(vAB,vPA)*scalarproduct(vAB,vPA))
        if isCloserToSegment(A,C,vAC):
            
            toAC=toA-(scalarproduct(vAC,vPA)*scalarproduct(vAC,vPA))
        if isCloserToSegment(B,C,vBC):
            
            toBC=toB-(scalarproduct(vBC,vPB)*scalarproduct(vBC,vPB))
        return min(toA,toB,toC,toAB,toAC,toBC)

    def isInCoplanarTriangle(self, A,B,C):
        #the 3 points are precreated to decrease computation time
        return area(A,B,C)==(area(self,B,C)+area(self,A,B)+area(self,A,C))
        
    def distanceSquaredToTriangle(self, n,A,B,C,vAB,vAC,vBC,limitsize):
        #the normal, the three points and the 3 vectors are precreated to decrease computation time
        
        algebraicDistance=scalarproduct(defineVector(self,A),n)
        if (abs(algebraicDistance)>limitsize):
            return float('inf')
        v=copy.copy(n)
        v.multiply(algebraicDistance)
        projectedPoint=self
        projectedPoint.translate(v)
        if projectedPoint.isInCoplanarTriangle(A,B,C):
            return (algebraicDistance*algebraicDistance)
        else:
            return (algebraicDistance*algebraicDistance)+projectedPoint.distanceSquaredFromCoplanarTriangle(A,B,C,vAB,vAC,vBC)
    

class Vector:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    def norm(self):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    def normalize(self):
        self.x=self.x/self.norm()
        self.y=self.y/self.norm()
        self.z=self.z/self.norm()
    
    def multiply(self,number):
        self.x=number*self.x
        self.y=number*self.y
        self.z=number*self.z



class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.normalVector=None
        self.label=None
        
    def findNormal(self):
        v1 = defineVector(self.p1,self.p2)
        v2 = defineVector(self.p3,self.p1)
        v=crossproduct(v1,v2)
        v.normalize()
        self.normalVector=v
    
    def size(self):
        size=max(Segment(self.p1,self.p2).length(),Segment(self.p1,self.p3).length(),Segment(self.p3,self.p2).length())
        return size
        
    def boundaries(self):
        xmax=max(self.p1.x,self.p2.x,self.p3.x)
        xmin=min(self.p1.x,self.p2.x,self.p3.x)
        ymax=max(self.p1.y,self.p2.y,self.p3.y)
        ymin=min(self.p1.y,self.p2.y,self.p3.y)
        zmax=max(self.p1.z,self.p2.z,self.p3.z)
        zmin=min(self.p1.z,self.p2.z,self.p3.z)
        return (xmax,xmin,ymax,ymin,zmax,zmin)
    
    def __str__(self):
        return "["+str(self.p1) + " " + str(self.p2) + " " + str(self.p3) + "]" +str(self.label)+"\n"
        
class Segment:
    def __init__(self, p1, p2):
        self.p1=p1
        self.p2=p2
        self.label=None
    # the segment is defined as p1*t + p2*(1-t)
        
    def length(self):
        return sqrt((self.p1.x-self.p2.x)*(self.p1.x-self.p2.x)+(self.p1.y-self.p2.y)*(self.p1.y-self.p2.y)+(self.p1.z-self.p2.z)*(self.p1.z-self.p2.z))
        
    def __str__(self):
        return "["+str(self.V1) + " " + str(self.V2) + "]  " + str(self.label)
        
## Functions on 3D objects

def defineVector(A,B):
    return Vector(B.x-A.x,B.y-A.y,B.z-A.z)

def area(p1,p2,p3):#the area of the triangle made of 3 points. 
    v1=defineVector(p1,p2)
    v2=defineVector(p1,p3)
    v=crossproduct(v1,v2)
    return (v.norm()/2)

def crossproduct(v1,v2):
    x=v1.y*v2.z-v1.z*v2.y
    y=v1.z*v2.x-v1.x*v2.z
    z=v1.x*v2.y-v1.y*v2.x
    return Vector(x,y,z)

def scalarproduct(v1,v2):
    return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z
    
def minimumSize(triangleList):
    size=triangleList[0].size()
    for index in range(len(triangleList)):
        size=min(size,triangleList[index].size())
    return size
    
def maximumSize(triangleList):
    size=triangleList[0].size()
    for index in range(len(triangleList)):
        size=max(size,triangleList[index].size())
    return size
        
def boundaries(triangleList):
    (xmax,xmin,ymax,ymin,zmax,zmin)=triangleList[0].boundaries()
    for index in range(len(triangleList)):
        (maxx,minx,maxy,miny,maxz,minz)=triangleList[index].boundaries()
        xmin=min(xmin,minx)
        ymin=min(ymin,miny)
        zmin=min(zmin,minz)
        xmax=max(xmax,maxx)
        ymax=max(ymax,maxy)
        zmax=max(zmax,maxz)
    return (xmax,xmin,ymax,ymin,zmax,zmin)

## 2D objects and functions, mainly for path generation

class Point2D:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.label=None
    
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")  " + self.label
        


class Segment2D:
    def __init__(self, p1, p2):
        self.p1=p1
        self.p2=p2
        self.label=None
        
    def intersectsSegment(self, s):
        o1=orientation2D(self.p1,self.p2,s.p1)
        o2=orientation2D(self.p1,self.p2,s.p2)
        o3=orientation2D(s.p1,s.p2,self.p1)
        o4=orientation2D(s.p1,s.p2,self.p2)
        return (o1*o2<=0)&(o3*o4<=0)
    
    def __str__(self):
        return "["+str(self.V1) + " " + str(self.V2) + "]  " + str(self.label)
        
def orientation2D(A,B,C):#check the orientation of the three points A,B,C in 2D. The equivalent in 2D of orientationVector
    result = (B.y-A.y)*(C.x-B.x)-(B.x-A.x)*(C.y-B.y) 
    if(result==0):
        return 0 #"colinear" 
    elif(result>0):
        return 1 #"clockwise"
    else:
        return -1 #"counterclockwise"
        
## Misc    

def samePoint2D(A,B): # this is to cope with float approx errors. epsilon can be modified
    epsilon = 0.001
    return ((abs(A.x,B.x)<epsilon) and (abs(A.y,B.y)<epsilon) )

def samePoint(A,B):# this is to cope with float approx errors. epsilon can be modified
    epsilon = 0.00001 
    return (abs(A.x,B.x)<epsilon) and (abs(A.y,B.y)<epsilon) and (abs(A.z,B.z)<epsilon)

def printList(liste): #has to be put somewhere else
    print("\nReading list :")
    print("[",end ="")
    for e in liste:
        print(" " + str(e),end ="" )
    print("]")
    print("End list\n")
        