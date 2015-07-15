# These functions slice an object defined by a list of facets (triangles)
# It is based on the article A Method for Slicing CAD Models in Binary STL Format
# written by O. Topcu, Y. Tasc?oglu and H. O. Unver


from geometry import *
from zIntersection import *





# This function slices the object :
# for each slicing plan, it returns a list of segments that are the intersection of the object with the plan
# all those lists of lines are stored in a list of list
def getLines(Zmin,Zmax,Zstep,triangleList):
    z=Zmin
    lineListZ = [[]]#list of lists
    i = 0
    while(z<Zmax):
        # print("------------")
        #print("z = "+str(z))
        #print("------------")

        for tr in triangleList:
            zMinTr=getZmin(tr)
            zMaxTr=getZmax(tr)

            if(zMinTr<=z and zMaxTr>z):
                # print("\nnew triangle : " +str(tr.label))
                V1=tr.V1
                V2=tr.V2
                V3=tr.V3
                # As described on the pdf file, we need to permute the vertices to check every cases
                nbPassages = 0
                while(nbPassages<3):
                    z1=V1.z
                    z2=V2.z
                    z3=V3.z
                    if(z1==z and z2==z and z3==z):# case I
                        lineListZ[i].append(Line(V1,V2,-2))
                        lineListZ[i].append(Line(V2,V3,-2))
                        lineListZ[i].append(Line(V3,V1,-2))

                        #print(str(Line(V1,V2,-2)))
                        #print(str(Line(V2,V3,-2)))
                        #print(str(Line(V3,V1,-2)))
                        nbPassages=5
                    elif(z1==z and z2==z and z3!=z): # case II
                        lineListZ[i].append(Line(V1,V2,z3))
                        #print(str(Line(V1,V2,z3)))
                        nbPassages=5
                    elif( z1==z and((z2<z and z3>z) or (z2>z and z3<z))): # case III
                        lineListZ[i].append(Line(V1,ZIntersection(V2,V3,z),-1))
                        #print(str(Line(V1,ZIntersection(V2,V3,z),-1)))
                        nbPassages=5
                    elif( (z1<z and (z3>z and z2>z)) or (z1>z and (z3<z and z2<z)) ): # case IV
                        lineListZ[i].append(Line(ZIntersection(V1,V2,z),ZIntersection(V1,V3,z),-1))
                        #print(str(Line(ZIntersection(V1,V2,z),ZIntersection(V1,V3,z),-1)))
                        nbPassages=5
                    elif(z1==z and ( (z2>z and z3>z) or (z2<z and z3<z) )): # case V
                        nbPassages=4
                    V1,V2,V3=V2,V3,V1
                    nbPassages = nbPassages + 1
            elif(zMaxTr<z):

                triangleList.remove(tr)
                #print("removed " + str(tr))

        z=z+Zstep
        i += 1
        lineListZ.append([])
        #endwhile

    while(len(lineListZ)>0 and lineListZ[0]==[]):
        del lineListZ[0]
    print("End of first slicing")
    return lineListZ

#check if two lines are the same (they have the same extremities)
def sameLine(L1,L2):
    return ( (L1.V1.x==L2.V1.x and L1.V1.y==L2.V1.y and L1.V2.x==L2.V2.x and L1.V2.y==L2.V2.y) or (L1.V1.x==L2.V2.x and L1.V1.y==L2.V2.y and L1.V2.x==L2.V1.x and L1.V2.y==L2.V1.y) )


# As mentionned in the pdf file and the article, we need to get rid of overlapping lines
# This functions list of list of segments and returns the same list with no overlapping segments
# the list must have been created by the previous function to handle labels
def treatOverlappingLines(lineListZ,zStep):
    z=0
    newListList = []
    newList = []
    for list in lineListZ:
        newList = []
        i=0
        j=1
        def nextCouple(i,j,l):
            if(i==(l-1) and j==(i-1)):
                i=l
                j=l
            elif(j<(l-1)):
               if(j==(i-1)):
                   j += 2
               else:
                   j += 1
            else:
                i += 1
                j = 0
            return i,j
        while(i<len(list)):
            while(j<len(list)):
                #print("i"+str(i)+" j"+str(j)+" l"+str(len(list)))
                l1 = list[i]
                l2 = list[j]
                if((l1 != 0) and (l2 != 0) and sameLine(l1,l2)):
                    #print(str(l1))
                    #print(str(l1))

                    z=l1.V1.z
                    if (l1.label==-2 and l2.label==-2): #case A
                        print("case A")
                        list[i]=0
                        list[j]=0
                    elif((l1.label==-2 and l2.label!=-2) or (l1.label==-2 and l2.label!=-2) ): #case B
                        print("case B")
                        list[j]=0
                    elif( (l1.label<z and l2.label>z) or (l1.label>z and l2.label<z) ): #case C
                        print("case C")
                        list[j]=0
                    elif( (l1.label<z and l2.label<z) or (l1.label>z and l2.label>z) ): #case D
                        print("case D")
                        list[i]=0
                        list[j]=0
                i,j=nextCouple(i,j,len(list))
        # print(str(z))
        z += zStep
        for l in list:
            if(l!=0):
                newList.append(l)
        newListList.append(newList)
    print("Dealt with overlapping lines")
    return newListList


