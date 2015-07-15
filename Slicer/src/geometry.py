
def abs(a,b):
    if(a>=b):
        return (a-b)
    else:
        return (b-a)

def samePoint(A,B):
    epsilon = 0.001
    return ((abs(A.x,B.x)<epsilon) and (abs(A.y,B.y)<epsilon) )

def samePointEspace(A,B):
    epsilon = 0.00001
    return (abs(A.x,B.x)<epsilon) and (abs(A.y,B.y)<epsilon) and (abs(A.z,B.z)<epsilon)

class Point:
    def __init__(self,x,y,z,label):
        self.x = x
        self.y = y
        self.z = z
        self.label = label

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"

class PointPlan:
    def __init__(self,x,y,label):
        self.x = x
        self.y = y
        self.label = label

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")  " + self.label

class Triangle:
    def __init__(self,A,B,C,label):
        self.V1 = A
        self.V2 = B
        self.V3 = C
        self.label = label

    def __str__(self):
        return "["+str(self.V1) + " " + str(self.V2) + " " + str(self.V3) + "]" +str(self.label)+"\n"

class Line:
    def __init__(self,A,B,label):
        self.V1 = A
        self.V2 = B
        self.label = label

    def __str__(self):
        return "["+str(self.V1) + " " + str(self.V2) + "]  " + str(self.label)



def printList(liste):
    print("\nReading list :")
    print("[",end ="")
    for e in liste:
        print(" " + str(e),end ="" )
    print("]")
    print("End list\n")

def getZmin(triangle):
    return min(triangle.V1.z,triangle.V2.z,triangle.V3.z)

def getZmax(triangle):
    return max(triangle.V1.z,triangle.V2.z,triangle.V3.z)

def sameLine(L1,L2):
    return ( (L1.V1.x==L2.V1.x and L1.V1.y==L2.V1.y and L1.V2.x==L2.V2.x and L1.V2.y==L2.V2.y) or (L1.V1.x==L2.V2.x and L1.V1.y==L2.V2.y and L1.V2.x==L2.V1.x and L1.V2.y==L2.V1.y) )