from math import *
from geometry import *
from slicing import *
from slicingV2 import *
from infill import *
from PathGenerator import *


class genereGCode:
    E=0
    F = 1000
    X = 0
    Y = 0
    Z = 0.1
    zMin = 0
    zMax = 200
    flowE = 0.035
    layerThickness = 0.15
    infillStep = 8
    epsilon = 0.0001 #distance under which two number are considered equal


    def __init__(self,name,list):


        fichier = open(name+".gcode","w")
        fichier.write(self.startcode())

        triangleList2= self.translate(100,100,0,list)

        slicedObject = Sliced(self.zMin,self.zMax,self.layerThickness,triangleList2)
        result = slicedObject.lines

        result2 = treatOverlappingLines(result,self.layerThickness)
        result3 = generatePathForEveryPlan(result2)
        print("Outside path generated")
        inside = generateInfill(self.infillStep,0,0,200,200,result3)
        print("inside generated")

        shapeAndInfill = []
        i = 0
        while(i<len(result3)):
            if(i<len(inside)):
                shapeAndInfill.append( (result3[i] + inside[i]))
            else:
                shapeAndInfill.append( result3[i] )
            i += 1

        fichier.write(self.segment(Point(0,0,0.3,""),Point(100,0,0.3,"")))

        for l in shapeAndInfill:
            fichier.write("\n")
            fichier.write(";New layer : z="+str(self.Z)+"\n")
            for s in l:
                fichier.write(self.segment(s.V1,s.V2))
                fichier.write("\n")
            self.Z += self.layerThickness

        fichier.write(self.endcode())
        fichier.close()

    def calculE(self,A,B,):
        distance = sqrt( (pow((A.x-B.x),2)) + pow((A.y-B.y),2))
        self.E = (self.E + (self.flowE*distance))

    def segment(self,A,B):
        instruction = "G1" + " X"+str(A.x) + " Y"+str(A.y) + " Z"+str(self.Z) + " E"+str(self.E) + " F"+str(self.F+500)+"\n"
        self.calculE(A,B)
        instruction = instruction + "G1" + " X"+str(B.x) + " Y"+str(B.y) + " Z"+str(self.Z) + " E"+str(self.E) + " F"+str(self.F)+"\n"
        return instruction

    def startcode(self):
        startString = ""
        startCode = open("startcode.gcode","r")
        for line in startCode:
            startString = startString + line
        startCode.close()
        return startString

    def endcode(self):
        endString = ""
        endCode = open("endcode.gcode","r")
        for line in endCode:
            endString = endString + line
        endCode.close()
        return endString

    def translate(self,x,y,z,triangleList):
        translatedTriangles = []
        # print(str(triangleList[0]))
        def translate(tr):
            A = Point((tr.V1.x+x),(tr.V1.y+y),tr.V1.z+z,tr.V1.label)
            B = Point((tr.V2.x+x),(tr.V2.y+y),tr.V2.z+z,tr.V2.label)
            C = Point((tr.V3.x+x),(tr.V3.y+y),tr.V3.z+z,tr.V3.label)
            return Triangle(A,B,C,tr.label)
        for triangle in triangleList:
            translatedTriangles.append(translate(triangle))
        del triangleList
        # print(str(translatedTriangles[0]))
        return translatedTriangles


