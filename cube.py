import sys, math, pygame, random, time, os
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT
from operator import itemgetter

import getpass
if getpass.getuser() != 'root': sys.exit("Must be run as root.")

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)

class Simulation:
    def __init__(self, win_width = 240, win_height = 320):        
        os.putenv('SDL_FBDEV',   '/dev/fb1')
        pygame.init()
        pygame.mouse.set_visible(False)
        
        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Rendering")
        self.clock = pygame.time.Clock()
        
        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]
        
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
        self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        
    def rotate(self, direction):
        tVertices = []
        for vertex in self.vertices:
            rotation = vertex.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            projection = rotation.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
            tVertices.append(projection)

        avgZ = []
        i = 0
        for f in self.faces:
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z) / 4.0
            avgZ.append([i,z])
            i = i + 1

        for zVal in sorted(avgZ,key=itemgetter(1),reverse=True):
            fIndex = zVal[0]
            f = self.faces[fIndex]
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                         (tVertices[f[1]].x, tVertices[f[1]].y), (tVertices[f[2]].x, tVertices[f[2]].y),
                         (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y),
                         (tVertices[f[3]].x, tVertices[f[3]].y), (tVertices[f[0]].x, tVertices[f[0]].y)]
            pygame.draw.polygon(self.screen,self.colors[fIndex],pointList)
 
        if (direction == "UP"):
            self.angleX += 2
        elif (direction == "DOWN"):
            self.angleX -= 2
        elif (direction == "LEFT"):
            self.angleY += 2
        elif (direction == "RIGHT"):
            self.angleY -= 2
        
        pygame.display.flip()
     
    def colorFade(self, origColor, fadeInColor):
        if (origColor[0] != fadeInColor[0]):
            if (origColor[0] < fadeInColor[0]):
                origColor[0]+= 1
            else:
                origColor[0]-= 1
        
        if (origColor[1] != fadeInColor[1]):
            if (origColor[1] < fadeInColor[1]):
                origColor[1]+= 1
            else:
                origColor[1]-= 1
                
        if (origColor[2] != fadeInColor[2]):
            if (origColor[2] < fadeInColor[2]):
                origColor[2]+= 1
            else:
                origColor[2]-= 1
            
        self.screen.fill(origColor)
 
    def run(self):
        origColor = [0,0,0]
        self.screen.fill(origColor)
        self.rotate("UP")
        pygame.display.flip()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.clock.tick(50)

            self.rotate("UP")
            self.rotate("LEFT")
            self.colorFade(origColor, origColor)

if __name__ == "__main__":
    Simulation().run()