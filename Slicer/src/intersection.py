from geometry import *

#We want to know whether two segments intersect in just one point that is not in one of its extremities
#Then we want to calculate this point if it exists
#We work in the plan


#check the orientation of the three points A,B,C
def orientation(A,B,C):
    result = (B.y-A.y)*(C.x-B.x)-(B.x-A.x)*(C.y-B.y)
    if(result==0):
      return 0 #"colinear"
    elif(result>0):
        return 1 #"clockwise"
    else:
        return 2 #"counterclockwise"



# check whether two segments intersect in just one point that is not in their extremities
def checkIntersection(A,B,C,D):

    o1=orientation(A,B,C)
    o2=orientation(A,B,D)
    o3=orientation(C,D,A)
    o4=orientation(C,D,B)

    #General case (no colinearity)
    if((o1!=o2) and (o3!=o4)):
        return True
    else:
        return False


#calculate the determinant
def det(a,b,c,d):
    return ((a*d)-(c*b))


# give an equation of the line AB in the forme ax+by=e
def equation(A,B):

    #if the line is parallel to the ordinate
    if (A.x==B.x):
        return (1,0,A.x)
    else:
        a=((B.y-A.y)/(B.x-A.x))
        b=A.y-a*A.x
        return (a,-1,-b)

# assuming that (AB) and (CD) are not parallel, returns their intersection
def intersectionPoint(A,B,C,D):

    (a,b,e)=equation(A,B)
    (c,d,f)=equation(C,D)


    determinant=det(a,b,c,d)
    if (determinant==0):
        print("parallel lines")
    else:
        x=(det(e,b,f,d)/determinant)
        y=(det(a,e,c,f)/determinant)
        return PointPlan(x,y,"")


# A=PointPlan(0,0,"A")
# B=PointPlan(0,1,"B")
# C=PointPlan(1,1,"C")
# D=PointPlan(1,0,"D")
# print(checkIntersection(A,C,B,D))
# (a,b,e)=(equation(A,C))
# (c,d,f)=(equation(B,D))
# print((det(e,b,f,d)/det(a,b,c,d)))
# print(intersectionPoint(A,C,B,D))

