import os
import struct
from Geometry import *



class loader:
    model=[]
    def __init__(self):
        self.model = []

    #return the faces of the triangles
    def get_triangles(self):
        if self.model:
            for face in self.model:
                yield str(face)


    #load stl file detects if the file is a text file or binary file
    def load_stl(self,filename):
        #read start of file to determine if its a binay stl file or a ascii stl file
        fp=open(filename,'rb')
        h=fp.read(80)
        type=h[0:5]
        fp.close()

        if type=='solid':
            print("reading text file"+str(filename))
            self.load_text_stl(filename)
        else:
            print("reading binary stl file "+str(filename,))
            self.load_binary_stl(filename)

        #self.removeDoubles() #removed because it takes too much time, see below



    #read text stl match keywords to grab the points to build the model
    def load_text_stl(self,filename):
        fp=open(filename,'r')

        for line in fp.readlines():
            words=line.split()
            if len(words)>0:
                if words[0]=='solid':
                    self.name=words[1]

                if words[0]=='facet':
                    center=[0.0,0.0,0.0]
                    triangle=[]
                    normal=(eval(words[2]),eval(words[3]),eval(words[4]))

                if words[0]=='vertex':
                    triangle.append(Point(eval(words[1]),eval(words[2]),eval(words[3]),""))


                if words[0]=='endloop':
                    #make sure we got the correct number of values before storing
                    if len(triangle)==3:
                        A=Point(triangle[0][0],triangle[0][1],triangle[0][2])
                        B=Point(triangle[1][0],triangle[1][1],triangle[1][2])
                        C=Point(triangle[2][0],triangle[2][1],triangle[2][2])
                        self.model.append(Triangle(A,B,C))
        fp.close()

    #load binary stl file check wikipedia for the binary layout of the file
    #we use the struct library to read in and convert binary data into a format we can use
    def load_binary_stl(self,filename):
        fp=open(filename,'rb')
        h=fp.read(80)

        l=struct.unpack('I',fp.read(4))[0]
        count=0
        while True:
            try:
                p=fp.read(12)
                if len(p)==12:
                    n=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                p=fp.read(12)
                if len(p)==12:
                    p1=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]
                    p1=Point(p1[0],p1[1],p1[2])

                p=fp.read(12)
                if len(p)==12:
                    p2=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]
                    p2=Point(p2[0],p2[1],p2[2])

                p=fp.read(12)
                if len(p)==12:
                    p3=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]
                    p3=Point(p3[0],p3[1],p3[2])

                new_tri=(n,p1,p2,p3)

                if len(new_tri)==4:
                    tri=Triangle(p1,p2,p3)
                    self.model.append(tri)
                count+=1
                fp.read(2)

                if len(p)==0:
                    break
            except EOFError:
                break
        fp.close()

##  These functions are useful for deleting triangles but they take a lot of extra time, and for boxelization, double triangles are not a problem

#     def sameTriangle(self,tr,tr2):
#             if(samePointEspace(tr.V1,tr2.V1) and samePointEspace(tr.V2,tr2.V2) and samePointEspace(tr.V3,tr2.V3)):
#                 return True
#             elif(samePointEspace(tr.V1,tr2.V1) and samePointEspace(tr.V2,tr2.V3) and samePointEspace(tr.V3,tr2.V2)):
#                 return True
#             elif(samePointEspace(tr.V1,tr2.V2) and samePointEspace(tr.V2,tr2.V3) and samePointEspace(tr.V3,tr2.V1)):
#                 return True
#             elif(samePointEspace(tr.V1,tr2.V2) and samePointEspace(tr.V2,tr2.V1) and samePointEspace(tr.V3,tr2.V3)):
#                 return True
#             elif(samePointEspace(tr.V1,tr2.V3) and samePointEspace(tr.V2,tr2.V1) and samePointEspace(tr.V3,tr2.V2)):
#                 return True
#             elif(samePointEspace(tr.V1,tr2.V3) and samePointEspace(tr.V2,tr2.V2) and samePointEspace(tr.V3,tr2.V1)):
#                 return True
#             else:
#                 return False
# 
# 
#     def removeDoubles(self):
#         copy = self.model
#         self.model =[]
#         alreadyInList = False
#         for tr in copy:
#             for tr2 in self.model:
#                 alreadyInList = alreadyInList or self.sameTriangle(tr,tr2)
#             if(not(alreadyInList)):
#                 self.model.append(tr) 

