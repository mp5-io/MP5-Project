# New version of the slicing function
# These functions slice an object defined by a list of facets (triangles)
# It is based on the article A Method for Slicing CAD Models in Binary STL Format
# written by O. Topcu, Y. Tasc?oglu and H. O. Unver
# Each triangle is intersected with the slicing plans that are between it maximum and minimum altitude

from geometry import *
from zIntersection import *

class Sliced:
    lines=[]
    # Edges that are in the slicing plan need to be treated separetely
    # They are put in a separate list that is then treated and merged with the main on
    edges = []

    def __init__(self,zMin,zMax,zStep,triangleList):
        z=zMin
        # We create a list of empty list : one for every slicing plan
        self.lines=[]
        self.edges=[]
        zList=[]#list of the altitude of

        while(z<zMax):
            self.lines.append([])
            self.edges.append([])
            zList.append(z)
            z += zStep
        #print(len(self.lines))

        for triangle in triangleList:
            zMinTr=getZmin(triangle)
            zMaxTr=getZmax(triangle)

            # get the value of the first intersecting plan
            i=0
            while(i<len(zList) and zList[i] < zMinTr):
                i += 1
            z=zList[i]

            while(z<zMaxTr):
                #print(i)
                # print("\nnew triangle : " +str(triangle.label))
                V1=triangle.V1
                V2=triangle.V2
                V3=triangle.V3
                # As described on the pdf file, we need to permute the vertices to check every cases
                nbPassages = 0
                while(nbPassages<3):
                    z1=V1.z
                    z2=V2.z
                    z3=V3.z
                    if(z1==z and z2==z and z3==z):# case I
                        self.edges[i].append(Line(V1,V2,-2))
                        self.edges[i].append(Line(V2,V3,-2))
                        self.edges[i].append(Line(V3,V1,-2))

                        #print(str(Line(V1,V2,-2)))
                        #print(str(Line(V2,V3,-2)))
                        #print(str(Line(V3,V1,-2)))
                        nbPassages=5
                    elif(z1==z and z2==z and z3!=z): # case II
                        self.edges.append(Line(V1,V2,z3))
                        #print(str(Line(V1,V2,z3)))
                        nbPassages=5
                    elif( z1==z and((z2<z and z3>z) or (z2>z and z3<z))): # case III
                        self.lines[i].append(Line(V1,ZIntersection(V2,V3,z),-1))
                        #print(str(Line(V1,ZIntersection(V2,V3,z),-1)))
                        nbPassages=5
                    elif( (z1<z and (z3>z and z2>z)) or (z1>z and (z3<z and z2<z)) ): # case IV
                        self.lines[i].append(Line(ZIntersection(V1,V2,z),ZIntersection(V1,V3,z),-1))
                        #print(str(Line(ZIntersection(V1,V2,z),ZIntersection(V1,V3,z),-1)))
                        nbPassages=5
                    elif(z1==z and ( (z2>z and z3>z) or (z2<z and z3<z) )): # case V
                        nbPassages=4
                    V1,V2,V3=V2,V3,V1
                    nbPassages = nbPassages + 1
                z += zStep
                i += 1

        # merge the remaining edges with the segments
        j=0
        while(j<len(self.edges) and j<len(self.lines)):
            self.lines[j] = self.lines[j]+self.edges[j]
            j += 1

        while(len(self.lines)>0 and self.lines[0]==[]):
                del self.lines[0]
        print("End of first slicing")

    def addTo(self,l1):
        for l2 in self.edges:
            if(sameLine(l1,l2)):
                #print(str(l1))
                #print(str(l1))
                z=l1.V1.z
                if (l1.label==-2 and l2.label==-2): #case A
                    print("case A")
                    self.edges.remove(l2)
                elif((l1.label==-2 and l2.label!=-2) or (l1.label==-2 and l2.label!=-2) ): #case B
                    print("case B")
                elif( (l1.label<z and l2.label>z) or (l1.label>z and l2.label<z) ): #case C
                    print("case C")
                elif( (l1.label<z and l2.label<z) or (l1.label>z and l2.label>z) ): #case D
                    print("case D")
                    self.edges.remove(l2)
                else: # new segment
                    self.edge.append(l1)