from __future__ import annotations
import math
from math import sqrt
from numbers import Number
from typing import List
import numpy as np

EPS = 1E-9;

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, x, y=0, z=0):
        '''Defines x and y variables'''
        self.X = x
        self.Y = y
        self.Z = z

    def __add__(self, other):
        return Point(self.X+other.X, self.Y+other.Y, self.Z+other.Z)

    def __sub__(self, other):
        return Point(self.X-other.X, self.Y-other.Y, self.Z-other.Z)

    def __str__(self):
        return f"Point({self.X}, {self.Y}, {self.Z})"

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.sqrt(dx**2 + dy**2)


    def calc_tangents (self, r1, r2) -> Line:
        r = r2-r1
        z = self.X*self.X + self.Y*self.Y
        d = z - r*r
        if d < -EPS:
            return 0
        d = sqrt(abs(d))
        l = Line( a = ((self.X * r + self.Y * d) / z), \
                b = ((self.Y * r - self.X * d) / z), \
                c = r1)
        return l

    @staticmethod
    def testPoint(x=0,y=0):
        '''Returns a point and distance'''
        p1 = Point(3, 4)
        print (p1)
        p2 = Point(3,0)
        print (p2)
        print("p1-p2: ", p1 - p2)
        print("p1+p2: ", p1 + p2)

        return p1.distance(p2) #math.hypot(dx, dy)

class Circle(Point):
    '''Creates a circle on a coordinate plane with values x and y.'''

    def __init__(self, x, y=0, z=0, r=1):
        '''Defines x, y, and radius variables'''
        super().__init__(x, y, z)
        self.radius = r
    
    '''
        tangent_circle: finds points on circle where a tangent line through (Px,Py) touches the circle
        https://math.stackexchange.com/questions/543496/how-to-find-the-equation-of-a-line-tangent-to-a-circle-that-passes-through-a-g
    '''
    def tangent_circle(self, Px: Number, Py: Number, **kwargs):
                    #center_x: Number=0, center_y: Number=0, radius: Number=1):
        center_x = self.X
        center_y = self.Y
        radius = self.radius
        if 'x' in kwargs.keys():
            center_x = kwargs['x']
        if 'y' in kwargs.keys():
            center_y = kwargs['y']
        if 'radius' in kwargs.keys():
            radius = kwargs['radius']

        dx, dy = Px-center_x, Py-center_y
        dxr, dyr = -dy, dx
        d = sqrt(dx**2+dy**2)
        if d >= radius :
            rho = radius/d
            ad = rho**2
            bd = rho*sqrt(1-rho**2)
            T1x = center_x + ad*dx + bd*dxr
            T1y = center_y + ad*dy + bd*dyr
            T2x = center_x + ad*dx - bd*dxr
            T2y = center_y + ad*dy - bd*dyr
            if (d/radius-1) < 1E-8:
                print('P is on the circumference')
            return T1x, T1y, T2x, T2y

        else:
            print('''\
        Point P: (%g,%g) is inside the circle with centre C: (%g,%g) and radius r=%g.
        No tangent is possible...''' % (Px, Py, center_x, center_y, radius))
            return None
    
    '''
        number_tangents_circle: finds number of common tangents between two circles
    '''
    def number_tangents_circle(self, b: Circle):
        # sq root may reduce precision
        distSq = (self.X - b.X)**2 + (self.Y - b.Y)**2 
        radSumSq = (self.radius + b.radius)**2
        if (distSq == radSumSq):  # circles touching
            return 3              # tangent lines
        elif (distSq > radSumSq): # circles seperated
            return 4 # tangent lines
        else:        # circles overlap
            return 2 # tangent lines
    '''
        tangents: finds all tangent lines between two circles.
        # https://cp-algorithms.com/geometry/tangents-to-two-circles.html
    '''
    def tangents(self, b: Circle):
        ans: List[Line] = []

        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                line = (b-self).calc_tangents(self.radius*i, b.radius*j)
                if type(line) is Line:
                    ans.append(line)
        for i, tan in enumerate(ans):
            ans[i].c -= tan.a * self.X + tan.b * self.Y
            ans[i].c - b.radius
        return ans


    '''
        points_on_tangent: calculates all intersection points of all tangent lines on two circles
    '''
    def points_on_tangent(self, b: Circle):
        answers = self.tangents(b)
        # f"{self.a}*x + {self.b}*y + {self.c} = 0"
        points = []
        for line in answers:
            x1, x2 = 0, 1
            y1 = -(line.a*x1 + line.c)/line.b
            y2 = -(line.a*x2 + line.c)/line.b
            # dydx = - line.a / line.b
            x3, y3 = self.X, self.Y
            k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2)
            x4 = x3 - k * (y2-y1)
            y4 = y3 + k * (x2-x1)
            points.append((x4,y4))

            # second circle
            x3, y3 = b.X, b.Y
            k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2)
            x4 = x3 - k * (y2-y1)
            y4 = y3 + k * (x2-x1)
            points.append((x4,y4))
            # dydx = (x1-a)/(y1-b)
            # x1^2 + y1^2 = r^2
            # dydx * y1- b*dydx = x1 -a
            # y1 = (x1 - a)/dydx + b
        return points
    
class Sphere(Circle):
    '''Creates a circle on a coordinate plane with values x and y.'''

    def __init__(self, x, y=0, z=0, r=1):
        '''Defines x, y, and radius variables'''
        super().__init__(x, y, r)
        self.Z = z

    def __iter__(self):
        return iter((self.X, self.Y, self.Z, self.radius))

    def data_for_sphere(self):
        center_x, center_y, center_z, radius = self

        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi/2:10j]
        x = radius*np.cos(u)*np.sin(v) + center_x
        y = radius*np.sin(u)*np.sin(v) + center_y
        z = radius*np.cos(v) + center_z
        return x, y, z
    
    # If ALL points are inside sphere, return True
    def inside_sphere(self, ps: list[Point]) -> bool:
        cx, cy, cz, r = self.X, self.Y, self.Z, self.radius

        for p in ps:
            x, y, z = p.X, p.Y, p.Z
            if (x - cx)**2 + (y - cy)**2 + (z - cz)**2 > r**2:
                return False # outside sphere
        return True

class Line(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"{self.a}*x + {self.b}*y + {self.c} = 0"
    
    def __repr__(self) -> str:
        return f"{self.a}*x + {self.b}*y + {self.c} = 0"

class Cylinder(Sphere):
    def __init__(self, x, y, z, r, h):
        '''Defines x, y, and radius variables'''
        super().__init__(x, y, z, r)
        self.height = h

    def __iter__(self):
        return iter((self.X, self.Y, self.Z, self.radius, self.height))

    def data_for_cylinder_along_z(self, **kwargs):
        center_x, center_y, center_z, radius, height_z = self
        z = np.linspace(center_z, height_z, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid=np.meshgrid(theta, z)
        x_grid = radius*np.cos(theta_grid) + center_x
        y_grid = radius*np.sin(theta_grid) + center_y
        return x_grid,y_grid,z_grid

if __name__ == "__main__":

    print (f"distance = {Point.testPoint()}" )

    center_x, center_y = 0, 0
    radius = 5
    Px, Py = 10, 1
    # circle = Circle(center_x, center_y, radius)
    # point 1, point 2
    # T1x, T1y, T2x, T2y = tangent_circle(Px, Py, center_x=center_x, center_y=center_y, radius=radius)
    T1x, T1y, T2x, T2y = Circle(center_x, center_y, radius).tangent_circle(Px, Py)
    # T1x, T1y, T2x, T2y = tangent_circle(Px, Py, circle)

    print(f'The tangent of the circle at ({center_x}, {center_y}) of radius {radius}')
    print(f'that passes through ({Px, Py}) has')
    print('the tangent points:')
    print('\tT1: (%g,%g),  T2: (%g,%g).'%(T1x, T1y, T2x, T2y))

    print('The equations of the lines P-T1 and P-T2:')
    print('\t%+g·y%+g·x%+g = 0'%(T1x-Px, Py-T1y, T1y*Px-T1x*Py))
    print('\t%+g·y%+g·x%+g = 0'%(T2x-Px, Py-T2y, T2y*Px-T2x*Py))

    # Number of tangent lines

    c1 = Circle(-10, 8, 30)
    c2 = Circle(14, -24, 10)
    t = c1.number_tangents_circle(c2);

    if (t == 3):
        print("There are 3 common tangents between the circles.")
    elif (t == 4):
        print("There are 4 common tangents between the circles.")
    else:
        print("There are 2 common tangents between the circles.")
 
    # Actually get tangents
    answers = [str(tan) for tan in Circle(10, 1, 5).tangents(Circle(0,0,3))]
    print("Num tangents: \n", "\n".join( answers ) )

    print("Points? ", Circle(10, 1, 5).points_on_tangent(Circle(0,0,3)))

    s = Sphere(0, 0, 0, 1)
    print("Inside sphere:", s.inside_sphere([Point(0.5,0.5,0.5)]) )
    print("Outside sphere [False]:", s.inside_sphere([Point(0.9, 1.5, 1)]) )

