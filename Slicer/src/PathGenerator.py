# Path generator
from geometry import *


# swap the origin and the end of a segment line
def inverseLine(line):
    return Line(line.V2,line.V1,line.label)


def nextLineExist(point,segmentList):
    for line in segmentList:
        if(samePoint(point,line.V1) or samePoint(point,line.V2)):
            return True
    return False

def nextLine(point,segmentList):
    for line in segmentList:
        if(samePoint(point,(line.V1))):
            segmentList.remove(line)
            return segmentList,line
        elif(samePoint(point,line.V2)):
            segmentList.remove(line)
            return segmentList,inverseLine(line) # We exchange the two extremities of the segment



def generatePath(segmentList): #segmentList is the list of segments in one slicing plan
    newPath = [] #There can be several path in one segment list
    #print("new layer")
    while(len(segmentList)>0):# We find a path
        #print("new path")
        line=segmentList[0]
        #print(str(line))
        del segmentList[0]
        newPath.append(line)
        while(nextLineExist(line.V2,segmentList)):
            segmentLine,line = nextLine(line.V2,segmentList)
            #print(str(line))
            newPath.append(line)
    return newPath

def generatePathForEveryPlan(segmentListList):
    newListList =[]
    for segmentList in segmentListList:
        newListList.append(generatePath(segmentList))
    return newListList



