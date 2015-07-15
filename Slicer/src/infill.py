
# We generate the in-fill of a sliced object

from geometry import *
from intersection import *
from slicing import *


# insert a point correctly in a sorted list of points (sorted by their X value)
def xInsertion(list, element):
    i=0
    while(i<len(list) and list[i].x<element.x):
        i += 1
    list.insert(i,element)
    return list
# insert a point correctly in a sorted list of points (sorted by their X value)
def yInsertion(list, element):
    i=0
    while(i<len(list) and list[i].y<element.y):
        i += 1
    list.insert(i,element)
    return list

# get the intersections of x=k with all the segments of the figure and sort them
def xIntersect(k,segmentList,lowerY,upperY):
    pointList = []
    X1=PointPlan(k,lowerY,"")
    X2=PointPlan(k,upperY,"")
    for segment in segmentList:
        if(checkIntersection(X1,X2,segment.V1,segment.V2)):
            poinList = (yInsertion(pointList,intersectionPoint(X1,X2,segment.V1,segment.V2)))
    return pointList

# get the intersections of x=k with all the segments of the figure and sort them
def yIntersect(k,segmentList,lowerX,upperX):
    pointList = []
    Y1=PointPlan(lowerX,k,"")
    Y2=PointPlan(upperX,k,"")
    for segment in segmentList:
        if(checkIntersection(Y1,Y2,segment.V1,segment.V2)):
            pointList = (xInsertion(pointList,intersectionPoint(Y1,Y2,segment.V1,segment.V2)))
    return pointList

# To obtain the infill segment we run the intersection points with every segments on a X-Y grid
def generateInfill(stepGrid,Xmin,Ymin,Xmax,Ymax,object):
    infillSegments = [] # will contain a list  of list of segments that constitute the infill (every list is for one slicing plan)
    listX = []
    listY = []
    i=0
    for slicedPlan in object:
        #print(i)
        infillSegments.append([])
        x = Xmin
        y = Ymin
        while( (x<Xmax and ((i%2)==0)) or (y<Ymax and (i%2)==1)):
            if(x<Xmax and ((i%2)==0)):
                listX=xIntersect(x,slicedPlan,Ymin,Ymax)
                # now we extract the segments from the point list
                while(len(listX)>1):
                    A=listX[0]
                    B=listX[1]
                    if((A.x!=B.x) or (A.y!=B.y)):
                        l=Line(A,B," x="+str(x));
                        infillSegments[i].append(l)
                    listX.remove(A)
                    listX.remove(B)
                x = x + stepGrid
            if(y<Ymax and ((i%2)==1)):
                listY=yIntersect(y,slicedPlan,Xmin,Xmax)
                # now we extract the segments from the point list
                while(len(listY)>1):
                    A=listY[0]
                    B=listY[1]
                    if((A.x!=B.x) or (A.y!=B.y)):
                        l=Line(A,B," y="+str(y))
                        infillSegments[i].append(l)
                    listY.remove(A)
                    listY.remove(B)
                y = y + stepGrid
        i += 1
    return infillSegments

