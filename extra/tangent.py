from math import sqrt
from numbers import Number
from geometry import Line, Circle, Point, EPS
from typing import List

'''
    tangent_circle: finds points on circle where a tangent line through (Px,Py) touches the circle
    https://math.stackexchange.com/questions/543496/how-to-find-the-equation-of-a-line-tangent-to-a-circle-that-passes-through-a-g
'''
def tangent_circle(Px: Number, Py: Number, *args, **kwargs):
                   #center_x: Number=0, center_y: Number=0, radius: Number=1):
    if len(args) > 0 and isinstance(args[0], Circle):
        center_x = args[0].X
        center_y = args[0].Y
        radius = args[0].radius
    elif len(args) > 0:
        center_x = args[0]
        center_y = args[1]
        radius = args[2]
    else:
        center_x = kwargs['center_x']
        center_y = kwargs['center_y']
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
def number_tangents_circle(a: Circle, b: Circle):
    # sq root may reduce precision
    distSq = (a.X - b.X)**2 + (a.Y - b.Y)**2 
    radSumSq = (a.radius + b.radius)**2
    if (distSq == radSumSq):  # circles touching
        return 3              # tangent lines
    elif (distSq > radSumSq): # circles seperated
        return 4 # tangent lines
    else:        # circles overlap
        return 2 # tangent lines

def calc_tangents (c: Point, r1, r2):
    r = r2-r1
    z = c.X*c.X + c.Y*c.Y
    d = z - r*r
    if d < -EPS:
        return 0
    d = sqrt(abs(d))
    l = Line( a = ((c.X * r + c.Y * d) / z), \
              b = ((c.Y * r - c.X * d) / z), \
              c = r1)
    return l

'''
    tangents: finds all tangent lines between two circles.
    # https://cp-algorithms.com/geometry/tangents-to-two-circles.html
'''
def tangents(a: Circle, b: Circle) -> List:
    ans: List[Line] = []

    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            line = calc_tangents(b-a, a.radius*i, b.radius*j)
            if type(line) is Line:
                ans.append(line)
    for i, tan in enumerate(ans):
        ans[i].c -= tan.a * a.X + tan.b * a.Y
        ans[i].c - b.radius
    return ans

'''
    points_on_tangent: calculates all intersection points of all tangent lines on two circles
'''
def points_on_tangent(a: Circle, b: Circle) -> list:
    answers = tangents(a, b)
    # f"{self.a}*x + {self.b}*y + {self.c} = 0"
    points, lines = [], []
    for line in answers:
        x1, x2 = 0, 1
        y1 = -(line.a*x1 + line.c)/line.b
        y2 = -(line.a*x2 + line.c)/line.b
        # dydx = - line.a / line.b
        x3, y3 = a.X, a.Y
        k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2)
        ax4 = x3 - k * (y2-y1)
        ay4 = y3 + k * (x2-x1)
        points.append((ax4,ay4))

        # second circle
        x3, y3 = b.X, b.Y
        k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2)
        bx4 = x3 - k * (y2-y1)
        by4 = y3 + k * (x2-x1)
        points.append((bx4,by4))

        # dydx = (x1-a)/(y1-b)
        # x1^2 + y1^2 = r^2
        # dydx * y1- b*dydx = x1 -a
        # y1 = (x1 - a)/dydx + b
    return points
    
if __name__ == "__main__":
    center_x, center_y = 0, 0
    radius = 5
    Px, Py = 10, 1
    # circle = Circle(center_x, center_y, radius)
    # point 1, point 2
    # T1x, T1y, T2x, T2y = tangent_circle(Px, Py, center_x=center_x, center_y=center_y, radius=radius)
    T1x, T1y, T2x, T2y = tangent_circle(Px, Py, center_x, center_y, radius)
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
    t = number_tangents_circle(c1, c2);

    if (t == 3):
        print("There are 3 common tangents between the circles.")
    elif (t == 4):
        print("There are 4 common tangents between the circles.")
    else:
        print("There are 2 common tangents between the circles.")
 
    # Actually get tangents
    answers = [str(tan) for tan in tangents(Circle(10, 1, 5), Circle(0,0,3))]
    print("Num tangents: \n", "\n".join( answers ) )

    print("Points? ", points_on_tangent(Circle(10, 1, 5), Circle(0,0,3)))


## The following is another instance of projecting a point (x3,y3)
#   # onto a line defined by (x1,y1) and (x2,y2). (x4,y4) is on the line
#   # and the projection of point 3.
##   first convert line to normalized unit vector
# double dx = x2 - x1;
# double dy = y2 - y1;
# double mag = sqrt(dx*dx + dy*dy);
# dx /= mag;
# dy /= mag;

##  translate the point and get the dot product
# double lambda = (dx * (x3 - x1)) + (dy * (y3 - y1));
# x4 = (dx * lambda) + x1;
# y4 = (dy * lambda) + y1;