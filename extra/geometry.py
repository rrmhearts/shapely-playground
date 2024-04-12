import math

EPS = 1E-9;

# should be replaced, used for circle code only
class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.X = x
        self.Y = y

    def __add__(self, other):
        return Point(self.X+other.X, self.Y+other.Y)

    def __sub__(self, other):
        return Point(self.X-other.X, self.Y-other.Y)

    def __str__(self):
        return f"Point({self.X}, {self.Y})"

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.sqrt(dx**2 + dy**2)

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

    def __init__(self, x, y, r):
        '''Defines x, y, and radius variables'''
        self.X = x
        self.Y = y
        self.radius = r

class Line(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"{self.a}*x + {self.b}*y + {self.c} = 0"
    
    def __repr__(self) -> str:
        return f"{self.a}*x + {self.b}*y + {self.c} = 0"
    
if __name__ == "__main__":

    print (f"distance = {Point.testPoint()}" )