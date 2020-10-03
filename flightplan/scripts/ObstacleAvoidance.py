########################DECLARATION
# so far I have everything tested and looking good on mission planner
# i dont really want to mess with altitude so i am setting an altitude of the new mission points the mission points altitude wil to fly at the whole mission 
#download the following librarys math,numpy,pyproj
# this script reads two txt files and outputs one txt file 
#zone = 18 is utm zone of competition

from math import sqrt, acos, atan2, sin, cos
import numpy as np

import pyproj
# !pip3 install pyproj

P = pyproj.Proj(proj='utm', zone=18,ellps='WGS84', preserve_units=True)
G = pyproj.Geod(ellps='WGS84')

def LatLon_To_XY(Lat,Lon):
    return P(Lat,Lon)    

def XY_To_LatLon(x,y):
    return P(x,y,inverse=True)    

def distance(Lat1, Lon1, Lat2, Lon2):
    return G.inv(Lon1, Lat1, Lon2, Lat2)


alt = 300  # declaration of altitude for mission



####################OBJECT CODE

def line_intersect(A1,A2,B1,B2):
    slope_A = (A2[1] - A1[1]) / (A2[0] - A1[0])
    slope_B = (B2[1] - B1[1]) / (B2[0] - B1[0])
    
    A_y = A1[1] - slope_A*A1[0]
    B_y = B1[1] - slope_B*B1[0]
            # y = mx + b
            # Set both lines equal to find the intersection point in the x direction
            # m1 * x + b1 = m2 * x + b2
            # m1 * x - m2 * x = b2 - b1
            # x * (m1 - m2) = b2 - b1
            # x = (b2 - b1) / (m1 - m2)
    x = (B_y - A_y) / (slope_A - slope_B)
            # Now solve for y -- use either line, because they are equal here
            # y = mx + b
    y = slope_A * x + A_y
    return x,y


def tangency(Ax,Ay,Bx,By,Cx,Cy,a):
    
    b = sqrt((Ax - Cx)**2 + (Ay - Cy)**2)  # hypot() also works here
    th = acos(a / b)  # angle theta
    d = atan2(Ay - Cy, Ax - Cx)  # direction angle of point P from C
    d1 = d + th  # direction angle of point T1 from C
    d2 = d - th  # direction angle of point T2 from C

    T1x = Cx + a * cos(d1)
    T1y =Cy + a * sin(d1)
    T2x = Cx + a * cos(d2)
    T2y = Cy + a * sin(d2)
    
    b = sqrt((Bx - Cx)**2 + (By - Cy)**2)  # hypot() also works here
    th = acos(a / b)  # angle theta
    d = atan2(By - Cy, Bx - Cx)  # direction angle of point P from C
    d1 = d + th  # direction angle of point T1 from C
    d2 = d - th  # direction angle of point T2 from C

    T3x = Cx + a * cos(d1)
    T3y =Cy + a * sin(d1)
    T4x = Cx + a * cos(d2)
    T4y = Cy + a * sin(d2)

        
    A1 = [Ax,Ay] # original point, positive slope line
    A2 = [T2x,T2y] # new tangent point
    B1 = [Bx,By] # final point, negative slope relative to tangency
    B2 = [T3x,T3y] # new tangent point

    x,y = line_intersect(A1,A2,B1,B2)
   
    return x,y
# using tangent point and og point we use slope intercept equation to find #intersection line between
# the slope of the original two points of the waypoint path

def object_avoidance(Ax,Ay,Bx,By,Cx,Cy,R):
    
    global x,y

# compute the euclidean distance between A and B
    LAB = np.sqrt( (Bx-Ax)**2+(By-Ay)**2 )

# compute the direction vector D from A to B
    Dx = (Bx-Ax)/LAB
    Dy = (By-Ay)/LAB

# the equation of the line AB is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= LAB.

# compute the distance between the points A and E, where
# E is the point of AB closest the circle center (Cx, Cy)
    t = Dx*(Cx-Ax) + Dy*(Cy-Ay)    

# compute the coordinates of the point E
    Ex = t*Dx+Ax
    Ey = t*Dy+Ay
# compute the euclidean distance between E and C
    LEC = np.sqrt((Ex-Cx)**2+(Ey-Cy)**2)

# test if the line intersects the circle
    if LEC < R :

    # compute distance from t to circle intersection point
        dt = np.sqrt( R**2 - LEC**2)

    # compute first intersection point
        Fx = (t-dt)*Dx + Ax
        Fy = (t-dt)*Dy + Ay

    # compute second intersection point
        Gx = (t+dt)*Dx + Ax
        Gy = (t+dt)*Dy + Ay
        print('drone intersects')
    # integrate tangent line new coordinate into here
        x,y = tangency(Ax,Ay,Bx,By,Cx,Cy,R)
        
    #convert back to longitude and latitude
    
# else test if the line is tangent to circle
    elif LEC == R :
        print('line is tangent')
        
    # tangent point to circle is E

    else :
        print('drone doesnt intersect')
    #line doesn't touch circle
    return x,y


#################################PARSING CODE
#C:\Users\Public\Downloads\InteropCode\interop\MissionPointsParsed.txt
#C:\Users\Public\Downloads\InteropCode\interop\StationaryParsed.txt
#C:\Users\Public\Downloads\InteropCode\interop\MissionPointsParsedObstacle.txt


path1 = 'C:\Users\Public\Downloads\InteropCode\interop\MissionPointsParsed.txt'
MissionPlanned = open(path1,'r')


Mission_Planned = MissionPlanned.read()


path2 = 'C:\Users\Public\Downloads\InteropCode\interop\StationaryParsed.txt'
MissionObstacle = open(path2,'r')

Mission_Obstacle=MissionObstacle.read()


Obstacle = list(Mission_Obstacle.split(','))
Planned = list(Mission_Planned.split(','))

TotalObstacle = len(Obstacle)
TotalPlanned = len(Planned)


i = 1
while i<=TotalObstacle:
    if i ==1:
        Only_Obstacles = Obstacle[i:i+3]
        print(Only_Obstacles)
        i= i+5
    Only_Obstacles = Only_Obstacles + Obstacle[i:i+3]
    i = i + 5
    
i = 1
while i<=TotalPlanned:
    if i ==1:
        Only_Planned = Planned[i:i+2]
        print(Planned)
        i= i+4
    Only_Planned = Only_Planned + Planned[i:i+2]
    i = i + 4
    
FObstacles = [float(i) for i in Only_Obstacles]
FPlanned = [float(i) for i in Only_Planned]
print(FObstacles)
print(FPlanned)
##################CONVERSION FROM LAT LON TO XY
FObstacleTotal = len(FObstacles)
FPlannedTotal = len(FPlanned)
FP = []
OB = []
index = 0
while index < FPlannedTotal-1:
    C = FPlanned[index]
    D = FPlanned[index+1]
    print('this is C',C)
    print('this is D', D)
    A,B = LatLon_To_XY(C,D)
    FP.append(A)
    FP.append(B)
    
    index = index + 2
index = 0   
while index < FObstacleTotal-2:
    R= FObstacles[index]
    S=FObstacles[index+1]
    Rad = FObstacles[index+2]
    F,V=LatLon_To_XY(R,S)
    OB.append(F)
    OB.append(V)
    OB.append(Rad)
    index = index + 3
print(FP)
print(OB)
################
##############OBJECT AVOIDANCE APPENDED TO NEW LIST

n = 0
i = 0


while n <= FPlannedTotal-3:
    if n<=FPlannedTotal-3:
        n= n+1
        while i<FObstacleTotal:
            x = 0
            y = 0
          
            
            x,y= object_avoidance(FP[n-1],FP[n],FP[n+1],FP[n+2],OB[i],OB[i+1],OB[i+2]/3.2808) 
            # 3.2808 to account for feet for radius
            if x != 0:
                s = 2
                print('this is x,y',x,y)
                
                G,H = XY_To_LatLon(x,y)
               
    
                #Store data please
                #convert float x,y to string and put at specific value
                
                FPlanned.insert(s,G)
                FPlanned.insert(s+1,H)
                
                s = s+4
            i = i+3

i = 0
index = 1
FP_len = len(FPlanned)
print('this is FP_len',FP_len)
while i < FP_len+3:
    FPlanned.insert(i,index)
    FPlanned.insert(i+3,alt)
    i = i+4
    index = index +1

############Write to text file!
FPlanned = str(FPlanned)[1:-1] 
my_file =
open('C:\Users\Public\Downloads\InteropCode\interop\MissionPointsParsedObstacle.txt', 'w')
my_file.write(FPlanned)

my_file.close()
print('Writing Complete')


