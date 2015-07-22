import copy
from math import *

##Points and vectors

class Point3D:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        self.label=""

    def __init__(self,x,y,z,label):
        self.x=x
        self.y=y
        self.z=z
        self.label=label

    def __init__(self,point2D,z): # builds a 3D point from a 2D point and a Z value
        self.x=point2D.x
        self.y=point2D.y
        self.z=z
        self.label=point2D.label


class Point2D:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.label=""

    def __init_(self,x,y,label):
        self.x=x
        self.y=y
        self.label=label

        
    def liesInsideRectangle(self,rectangle): #method for grid generation.It modifies the point but it's not gonna be reused
        #first, translate the center of the rectangle to the origin
        self.x+=(-rectangle.center.x)
        self.y+=(-rectangle.center.y)
        # then rotate it so that the length is parallel to the x axis
        # beware, you have to rotate the other way than the orientation vector
        (self.x,self.y)=(rectangle.orientationVector.x*self.x+rectangle.orientationVector.y*self.y,-rectangle.orientationVector.y*self.x+rectangle.orientationVector.x*self.y)
        # then just check it's within the boundaries
        return (2*abs(self.x)<rectangle.length)&(2*abs(self.y)<rectangle.width)
        
    def liesInsideEllipse(self,ellipse): #method for grid generation.It modifies the point but it's not gonna be reused
        #first, translate the center of the ellipse to the origin
        self.x+=(-ellipse.center.x)
        self.y+=(-ellipse.center.y)
        # then rotate it so that the length is parallel to the x axis
        # beware, you have to rotate the other way than the orientation vector
        (self.x,self.y)=(ellipse.orientationVector.x*self.x+ellipse.orientationVector.y*self.y,-ellipse.orientationVector.y*self.x+ellipse.orientationVector.x*self.y)
        # then just check it's within the boundaries
        return (2*abs(self.x)/ellipse.length)*(2*abs(self.x)/ellipse.length)+(2*abs(self.y)/ellipse.width)*(2*abs(self.y)/ellipse.width)<1
    
def barycenter(alpha, pt1, beta, pt2): #pls make sure that alpha+beta=1 otherwise it's not a barycenter anymore
    return Point2D(alpha*pt1.x+beta*pt2.x,alpha*pt1.y+beta*pt2.y)
    
def areColinear(A,B,C):
    #takes 3 2D points and tells if they're colinear.
    return ((A.x-B.x)*(B.y-C.y)-(A.y-B.y)*(B.x-C.x)==0)
    
def formRightAngle(A,B,C):
    #takes 3 2D points and tells if ABC is a right angle.
    return ((A.x-B.x)*(B.x-C.x)+(A.y-B.y)*(B.y-C.y)==0)
    
class Vector:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        
class Vector2D:
    def __init__(self, x, y): #epresents a vector in the xy plane
        self.x=x
        self.y=y
        
    def normalVector(self):
        return Vector2D(self.y,-self.x)
        
    def multiply(self,number):
        self.x=number*self.x
        self.y=number*self.y
        
## 2D shapes
        
class Shape2D: #is part of an xy plane
    def __init__(self,center):
        self.center=center #the center is only used in the layers, when the shape is a base it doesn't matter
        self.orientationVector=Vector2D(1,0) #gives the orientation of the "length axis". By default, it is along the x axis
        self.length=0
        self.width=0
    
    def rotation(self, angle): #only for 2D vectors
            s=sin(angle)
            c=cos(angle)
            (self.orientationVector.x,self.orientationVector.y)=(c*self.orientationVector.x-s*self.orientationVector.y,s*self.orientationVector.x+c*self.orientationVector.y)
    
    def resizeLength(self,ratio):
        self.length=self.length*ratio

    def resizeWidth(self,ratio):
        self.width=self.width*ratio
        
    def rescale(self,ratio):
        self.resizeLength(ratio)
        self.resizeWidth(ratio)
        
    def boundingLength(self):# this is the lenght of the edge of a square  that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return max(self.length,self.width)
        
    def xmin(self):
        return self.center.x-(self.boundingLength()/2)
    
    def xmax(self):
        return self.center.x+(self.boundingLength()/2)
        
    def ymin(self):
        return self.center.y-(self.boundingLength()/2)
    
    def ymax(self):
        return self.center.y+(self.boundingLength()/2)
        
class Rectangle(Shape2D):
    def __init__(self,center,length,width):
        self.center=center #these are the coordinates of the center of the ellipsoid
        self.length=length
        self.width=width
        self.orientationVector=Vector2D(1,0)
        self.type="R" #as in "rectangle"
    def isSquare(self):
        return (self.xLength==self.yLength)

    def giveVertices(self):
        xTranslation = (self.length/2)*self.orientationVector.x - (self.width/2)*self.orientationVector.y
        yTranslation = (self.length/2)*self.orientationVector.y + (self.width/2)*self.orientationVector.x
        A=Point2D(self.center.x+xTranslation,self.center.y+yTranslation)
        B=Point2D(self.center.x+xTranslation,self.center.y-yTranslation)
        C=Point2D(self.center.x-xTranslation,self.center.y-yTranslation)
        D=Point2D(self.center.x-xTranslation,self.center.y+yTranslation)
        return [A,B,C,D]
    

class Ellipse(Shape2D):
    def __init__(self,center,length,width):
        self.center=center
        self.length=length
        self.width=width
        self.orientationVector=Vector2D(1,0)
        self.type="E" #as in "ellipse"
        
    def isCircle(self):
        return (self.xRadius==self.yRadius)

    def equationParameters(self):
        # returns the parameters of the parametric equation : (a,b,x_c,y_c,cos(alpha),sin(alpha))
        # x = x_c + a.cos(t).cos(alpha) - b.sin(t).sin(alpha)
        # y = y_c + a.cos(t).sin(alpha) + b.sin(t).cos(alpha)
        # t in [0,2.pi]
        # where (x_c,y_c) is the center of the ellipse and a the rotation angle
        return [self.length/2,self.width/2,self.center.x,self.center.y,self.orientationVector.x,self.orientationVector.y]



## 3D shapes

class Shape3D:
    def __init__(self,center):
        self.center=center
        
    def copy(self):
        return copy.copy(self)
        
    def resizeLength(self,ratio):
        () #to be defined for each particular kind of object. will be overwrited

    def resizeWidth(self,ratio):
        () #to be defined for each particular kind of object. will be overwrited
    
    def resizeHeight(self,ratio):
        ()  #to be defined for each particular kind of object. will be overwrited
        
    def rescale(self,ratio):
        self.resizeLength(ratio)
        self.resizeWidth(ratio)
        self.resizeHeight(ratio)
        
    def translation(self,vector):
        self.center.x=self.center.x+vector.x
        self.center.y=self.center.y+vector.y
        self.center.z=self.center.z+vector.z        
        #it would require to change the center of the 2d base also(actually no, only ultmately, when you want to slice)
    
    def boundingLength(self):# this is the length of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
    #to be overwrited
        return 0
     
    def zmax(self): 
    #to be overwrited
        return 0
        
    def zmin(self):
    #to be overwrited
        return 0
        
    def xmin(self):
        return self.center.x-(self.boundingLength()/2)
    
    def xmax(self):
        return self.center.x+(self.boundingLength()/2)
        
    def ymin(self):
        return self.center.y-(self.boundingLength()/2)
    
    def ymax(self):
        return self.center.y+(self.boundingLength()/2)
        
class Ellipsoid(Shape3D):
    def __init__(self,center,length,width,height):
        self.center=center
        self.length=length
        self.width=width
        self.height=height
        #self.isBall=(self.xRadius==self.yRadius)&(self.xRadius==self.zRadius)

    def parameters(self):
        # returns the parameters [a,b,c,x_c,y_x,cos(alpha),sin(alpha)]
        # of the parametric equation
        # x = a*cos(u)*cos(v)*cos(alpha)-b*cos(u)*sin(v)*sin(alpha)
        # y = b*cos(u)*sin(v)*cos(alpha)+a*cos(u)*cos(v)*sin(alpha)
        # z = c*sin(u)
        # where u and v are the parameters, (x_c,y_c) the center and alpha the rotation angle
        return [self.length/2,self.width/2,self.height,self.center.x,self.center.y,self.center.z,self.orientationVector.x,self.orientationVector.y]
    
    def resizeLength(self,ratio):
        self.length=self.length*ratio

    def resizeWidth(self,ratio):
        self.width=self.width*ratio
    
    def resizeHeight(self,ratio):
        self.height=self.height*ratio
        
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            outline=Ellipse(Point2D(self.center.x,self.center.y),self.length,self.width)
            ratio=sqrt(1-(2*abs(z-self.center.z)/abs(self.height)))
            outline.rescale(ratio)
            return [outline]
        else :
            return []
    
    def zmax(self):
        return max(self.center.z+(self.height/2),self.center.z-(self.height/2))
        
    def zmin(self):
        return min(self.center.z+(self.height/2),self.center.z-(self.height/2))


    
        

    
        
class StandingCylinder(Shape3D):
    def __init__(self,center,height,base):
        self.center=center # these are the coordinates of the center of the base
        self.height=height # can be negative, it is the algebraic distance to the base
        self.base=base #the base can be any 2D shape

    def equationParameters(self):
        # returns the parameters of the parametric equation : (a,b,x_c,y_c,cos(a),sin(a))
        # x = x_c + a.cos(u).cos(a) - b.sin(u).sin(a)
        # y = y_c + a.cos(u).sin(a) + b.sin(u).cos(a)
        # z = v
        # where u and v are the parameters
        # (x_c,y_c) is the center of the ellipse and a the rotation angle
        return [self.length/2,self.width/2,self.center.x,self.center.y,self.orientationVector.x,self.orientationVector.y]
    
    def resizeLength(self,ratio):
        self.base.resizeLength(ratio)

    def resizeWidth(self,ratio):
        self.base.resizeWidth(ratio)
    
    def resizeHeight(self,ratio):
        self.height=self.height*ratio
        
    def rotation(self,angle):
        self.base.rotation(angle)
        
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            self.base.center=Point2D(self.center.x,self.center.y)
            outline=copy.copy(self.base)
            return [outline]
        else :
            return []
            
    def zmax(self):
        return max(self.center.z+(self.height),self.center.z)
        
    def zmin(self):
        return min(self.center.z+(self.height),self.center.z)
        
    def boundingLength(self):# this is the lenght of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return max(self.base.length,self.base.width)
    
        
class Cone(Shape3D):
    def __init__(self,center,height,base):
        self.center=center # these are the coordinates of the center of the base
        self.height=height # can be negative, it is the algebraic distance to the base
        self.base=base #the base can be any 2D shape

    def equationParameters(self):
        # returns the parameters of the parametric equation (a,b,c,e,f,xC,yC,cos(alpha),sin(alpha))
        # x = x_c + (e*v-f)*( a*cos(u)*cos(alpha)-b*sin(u)*sin(d) )
        # y = y_c + (e*v-f)*( a*cos(u)*sin(d)+b*sin(u)*cos(d) )
        # z = v

        a=self.length/2
        b=self.width/2

        # e and f are computed so that e*v+f=1 when v=zBase and e*v+f=0 when v=(zBase+height)
        zBase = self.center.z # the heught of the base of the cylinder
        height = self.height
        e = -1/(self.height)
        f = (zBase+height)/height

        #cos(alpha) and sin(alpha) are the coordinates of the orientation vector
        cosalpha = self.orientationVector.x
        sinalpha = self.orientationVector.y


        return [a,b,e,f,self.center.x,self.center.y,cosalpha,sinalpha]




    def resizeLength(self,ratio):
        self.base.resizeLength(ratio)

    def resizeWidth(self,ratio):
        self.base.resizeWidth(ratio)
    
    def resizeHeight(self,ratio):
        self.height=self.height*ratio
        
    def rotation(self,angle):
        self.base.rotation(angle)
        
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            self.base.center=Point2D(self.center.x,self.center.y)
            outline=self.base #does it duplicate my object ? I want it to duplicate
            relativeHeight=z-self.center.z
            outline.rescale(1-(relativeHeight/self.height))
            return [outline]
        else :
            return []
            
    def zmax(self):
        return max(self.center.z+(self.height),self.center.z)
        
    def zmin(self):
        return min(self.center.z+(self.height),self.center.z)
    
    def boundingLength(self):# this is the lenght of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return max(self.base.length,self.base.width)
        
class Cuboid(StandingCylinder):
    def __init__(self,center,xLength,yLength,zLength):
        self.center=center # these are the coordinates of the center of the base
        self.height=zLength
        self.base=Rectangle(center,xLength,yLength)
        self.base.orientationVector=Vector2D(1,0)
    
    def isCube(self):
        return (self.xLength==self.yLength)&(self.xLength==self.zLength)
        
class Paraboloid(Shape3D):
    def __init__(self,center,height,base):
        self.center=center # these are the coordinates of the center of the base
        self.height=height # can be negative, it is the algebraic distance to the base
        self.base=base #the base can be any 2D shape
    
    def resizeLength(self,ratio):
        self.base.resizeLength(ratio)

    def resizeWidth(self,ratio):
        self.base.resizeWidth(ratio)
    
    def resizeHeight(self,ratio):
        self.height=self.height*ratio
        
    def rotation(self,angle):
        self.base.rotation(angle)
        
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            self.base.center=Point2D(self.center.x,self.center.y)
            outline=self.base #does it duplicate my object ? I want it to duplicate
            relativeHeight=z-self.center.z
            outline.rescale(sqrt(1-(relativeHeight/self.height)))
            return [outline]
        else :
            return []
            
    def zmax(self):
        return max(self.center.z+(self.height),self.center.z)
        
    def zmin(self):
        return min(self.center.z+(self.height),self.center.z)
        
    def boundingLength(self):# this is the lenght of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return max(self.base.length,self.base.width)

class ObliqueCylinder(Shape3D):
    def __init__(self,center,topCenter,base):
        self.center=center # these are the coordinates of the center of the base
        self.topCenter=topCenter # carries the coordinates of the center of the top shape (which is the same as the base shape)
        self.base=base #the base can be any 2D shape
    
    def resizeLength(self,ratio):
        self.base.resizeLength(ratio)

    def resizeWidth(self,ratio):
        self.base.resizeWidth(ratio)
    
    def resizeHeight(self,ratio):
        self.topCenter.z=copy.copy(self.center.z)+ratio*(self.topCenter.z-copy.copy(self.center.z))
        
    def rotation(self,angle):
        self.base.rotation(angle)
        
    def moveTop(self,vector):
        self.topCenter.x+=vector.x
        self.topCenter.y+=vector.y
        self.topCenter.z+=vector.z 
    
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            self.base.center=Point2D(self.center.x,self.center.y)
            outline=copy.copy(self.base)
            return [outline]
        else :
            return []
            
    def zmax(self):
        return max(self.center.z+(self.height),self.center.z)
        
    def zmin(self):
        return min(self.center.z+(self.height),self.center.z)
        
    def boundingLength(self):# this is the length of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return max(self.base.length,self.base.width)+max(abs(self.center.x-self.topCenter.x),abs(self.center.y-self.topCenter.y))
        
## Transversal 2D shapes 
        
class TransversalShape2D:  #in "cylindric coordinates with respect to a certain 3D point that would be the origin. Mostly made for toroids
    def __init__(self): # is is useless to define a center, it will never be used. A transversal shape is like a vector, it has no position in space
        self.height=0
        self.radialLength=0
    
    def resizeHeight(self,ratio):
        self.height=self.height*ratio
        
    def resizeRadialLength(self,ratio):
        self.transversalDimension=self.transversalDimension*ratio
        
        
    

class TransversalRectangle:
    def __init__(self, height, radialLength,center):
        self.center=center
        self.height=height
        self.radialLength=radialLength
        
class TransversalEllipse:
    def __init__(self, height, radialLength,center):
        self.center=center
        self.height=height
        self.radialLength=radialLength
        

## Transversal 3D shapes

        
class Toroid(Shape3D):
    def __init__(self,center,radius,base,transversalShape):
        self.center=center
        self.base=base
        self.transversalShape=transversalShape
        # transversalShape.radialLength must not exceed 2*min(length,width)
        
    def resizeLength(self,ratio):
        self.base.resizeLength(ratio)

    def resizeWidth(self,ratio):
        self.base.resizeWidth(ratio)
        
    def resizeHeight(self,ratio):
        self.transversalShape.resizeHeight(ratio)
        
    def resizeRadialLength(self,ratio):
        self.transversalShape.resizeRadialLength(ratio)
        
    def rotation(self,angle):
        self.base.rotation(angle)
        
    def rescale(self,ratio):
        self.resizeLength(ratio)
        self.resizeWidth(ratio)
        self.resizeHeight(ratio)
        self.resizeRadialLength(ratio)
        
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            if (self.transversalShape.type=="R"):
                divergence = abs(self.transversalShape.radialLength)/2
                innerOutline=copy.copy(self.base)
                innerOutline.center=Point2D(self.center.x,self.center.y)
                innerOutline.length+=(-divergence)
                innerOutline.width+=(-divergence)
                outerOutline=copy.copy(self.base)
                outerOutline.center=Point2D(self.center.x,self.center.y)
                outerOutline.length+=divergence
                outerOutline.width+=divergence
                
                return [innerOutline,outerOutline]
            elif (self.transversalShape.type=="E"):
            
                ratio=sqrt(1-(2*abs(z-self.center.z)/abs(self.transversalShape.z)))
                divergence = abs(self.transversalShape.radialLength*ratio)/2
                innerOutline=copy.copy(self.base)
                innerOutline.center=Point2D(self.center.x,self.center.y)
                innerOutline.length+=(-divergence)
                innerOutline.width+=(-divergence)
                outerOutline=copy.copy(self.base)
                outerOutline.center=Point2D(self.center.x,self.center.y)
                outerOutline.length+=divergence
                outerOutline.width+=divergence
                return [innerOutline,outerOutline]
            else:
                return []
        else :
            return []
            
    def zmax(self):
        return max(self.center.z+(self.transversalShape.height/2),self.center.z-(self.radius+self.transversalShape.height/2))
        
    def zmin(self):
        return min(self.center.z+(self.transversalShape.height/2),self.center.z-(self.radius+self.transversalShape.height/2))
        
    def boundingLength(self):# this is the length of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return max(self.base.length,self.base.width)+self.transversalShape.radialLength
        
class StandingToroid(Shape3D): #this is a little hard to slice, to be decided after
    def __init__(self,center,radius,transversalShape):
        self.center=center
        self.radius=radius
        self.transversalShape=transversalShape #in that case, the transversal "height" will be the thickness of the object
        self.orientationVector=Vector(1,0)
        
    def resizeRadius(self, ratio):
        self.radius=self.radius*ratio
        
    def resizeThickness(self,ratio):
        self.transversalShape.resizeHeight(ratio)
        
    def resizeRadialLength(self,ratio):
        self.transversalShape.resizeRadialLength(ratio)
        
    def rescale(self,ratio):
        self.resizeRadius(ratio)
        self.resizeThickness(ratio)
        self.resizeRadialLength(ratio)
        
    def rotation(self, angle): 
            s=sin(angle)
            c=cos(angle)
            (self.orientationVector.x,self.orientationVector.y)=(c*self.orientationVector.x-s*self.orientationVector.y,s*self.orientationVector.x+c*self.orientationVector.y)
    
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            if (self.transversalShape.type=="R"):
                if (z>=self.zmax()-self.transversalShape.radialLength)|(z<=self.zmin()+self.transversalShape.radialLength):
                    outline=Rectangle(Point2D(self.center.x,self.center.y),2*sqrt((self.radius+(self.transversalShape.radialLength/2))*(self.radius+(self.transversalShape.radialLength/2))-(z-self.center.z)*(z-self.center.z)),self.transversalShape.height)
                    outline.orientationVector=self.orientationVector
                    return [outline]
                else:
                    greatLength=sqrt((self.radius+(self.transversalShape.radialLength/2))*(self.radius+(self.transversalShape.radialLength/2))-(z-self.center.z)*(z-self.center.z))
                    smallLength=sqrt(self.radius*self.radius-(z-self.center.z)*(z-self.center.z))
                    first = Rectangle(Point2D(self.center.x,self.center.y),(greatLength-smallLength),self.transversalShape.height)
                    second=Rectangle(Point2D(self.center.x,self.center.y),(greatLength-smallLength),self.transversalShape.height)
                    first.orientationVector=self.orientationVector
                    second.orientationVector=self.orientationVector
                    v1=copy.copy(first.orientationVector)
                    v1.multiply((greatLength+smallLength)/2)
                    first.translation(v1)
                    v2=copy.copy(v1)
                    v2.multiply(-1)
                    second.translation(v2)
                    return [first,second]
            elif (self.transversalShape.type=="E"): #need to make sure it is correct, i.e. works almost like rectangles)
                if (z>=self.zmax()-self.transversalShape.radialLength)|(z<=self.zmin()+self.transversalShape.radialLength):
                    outline=Ellipse(Point2D(self.center.x,self.center.y),2*sqrt((self.radius+(self.transversalShape.radialLength/2))*(self.radius+(self.transversalShape.radialLength/2))-(z-self.center.z)*(z-self.center.z)),self.transversalShape.height)
                    outline.orientationVector=self.orientationVector
                    return [outline]
                else: #this is wong !!!!
                    greatLength=sqrt((self.radius+(self.transversalShape.radialLength/2))*(self.radius+(self.transversalShape.radialLength/2))-(z-self.center.z)*(z-self.center.z))
                    smallLength=sqrt(self.radius*self.radius-(z-self.center.z)*(z-self.center.z))
                    first = Ellipse(Point2D(self.center.x,self.center.y),(greatLength-smallLength),self.transversalShape.height)
                    second=Ellipse(Point2D(self.center.x,self.center.y),(greatLength-smallLength),self.transversalShape.height)
                    first.orientationVector=self.orientationVector
                    second.orientationVector=self.orientationVector
                    v1=copy.copy(first.orientationVector)
                    v1.multiply((greatLength+smallLength)/2)
                    first.translation(v1)
                    v2=copy.copy(v1)
                    v2.multiply(-1)
                    second.translation(v2)
                    return [first,second]
                
            else:
                return []
        else :
            return []
    def zmin(self):
        return self.center.z-(self.radius+(self.transversalShape.radialLength/2))
    def zmax(self):
        return self.center.z+(self.radius+(self.transversalShape.radialLength/2))
        
    def boundingLength(self):# this is the length of the edge of a square (an infinite square based cylinder if you prefer) that would bound the object. It is not optimal, but almost, and needs very few calculation, as you can see :
        return 2*self.radius+self.transversalShape.radialLength
        
class LeaningCylinder(Shape3D):
    def __init__(self,center,length,transversalShape,orientationVector):
        self.center=center #this is the center of the whole object
        self.length=length
        self.transversalShape=transversalShape #transversalshape must be an ellipse, otherwise it's a cuboid and it's better to use a StandingCylinder representation
        self.orientationVector=orientationVector
        
    def resizeLength(self,ratio):
        self.length=self.length*ratio
    
    def resizeHeight(self,ratio):
        self.transversalShape.resizeHeight(ratio)
        
    def resizeRadialLength(self,ratio):
        self.transversalShape.resizeRadialLength(ratio)
        
    def rescale(self,ratio):
        self.resizeLength(ratio)
        self.resizeHeight(ratio)
        self.resizeRadialLength(ratio)
    
    def rotation(self, angle): 
            s=sin(angle)
            c=cos(angle)
            (self.orientationVector.x,self.orientationVector.y)=(c*self.orientationVector.x-s*self.orientationVector.y,s*self.orientationVector.x+c*self.orientationVector.y)
            
    def intersectionWithLayer(self,z):
        if (z>=self.zmin())&(z<=self.zmax()):
            outline=Rectangle(Point2D(self.center.x,self.center.y),self.length,self.transversalShape.transversalLength)
            ratio=sqrt(1-(2*abs(z-self.center.z)/abs(self.transversalShape.z)))
            outline.orientationVector=self.orientationVector
            outline.rescale(ratio)
            return [outline]
        else :
            return []
    
    def zmax(self):
        return max(self.center.z+(self.transversalShape.z/2),self.center.z-(self.transversalShape.z/2))
        
    def zmin(self):
        return min(self.center.z+(self.transversalShape.z/2),self.center.z-(self.transversalShape.z/2))

    
## Special shapes (to be determined):

class Blob(Shape3D):
    ()
    #a paraboloid is similar to this
    
class RoundedShape(Shape3D):
    ()
    #a normal shape, with rounded angles and edges
    # this should have subclasses
    
## function on shapes

def contains(shape1,shape2):
    ()
    #tells if shape1 contains shape2
    # we need to find out if there is not too many calculations for this


def coucou(){
    print("coucou")
}