import itertools
import json
from math import sqrt
from typing import Union, overload

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import shapely
from shapely import polygonize, wkt
import shapely.affinity
from shapely.geometry import LineString, Point, Polygon, mapping
import shapely.plotting

from extra.geometry import Sphere


def polygon_to_tuple_points(polygon: Polygon, zcoords=() ):
    poly_coordinates = mapping(polygon)['coordinates'][0]
    try:
        poly_ = [(coords[0], coords[1], coords[2], *zcoords) for coords in poly_coordinates]
    except IndexError:
        # poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]
        poly_ = [(coords[0], coords[1], *zcoords) for coords in poly_coordinates]
    # Mind that the above output will contain one point two times, the first and last points
    return poly_[:-1]

def point_to_tuple(point: Point|tuple):
    if isinstance(point, Point):
        return tuple(point.coords)[0]
    return point

def points_to_intersections(points: list, rounder:int = 1, criterion=None):
    inters = []
    # G = nx.complete_graph(points)
    # G.remove_edges_from(nx.selfloop_edges(G))
    if criterion is None:
        criterion = lambda a, b: True

    for a, b, c, d in itertools.combinations(points, 4):
        if a != b and c != d:
            inter = LineString([a, b]).intersection(LineString([c, d]))
            if isinstance(inter, Point):
                rounded = Point(np.round(np.array(point_to_tuple(inter)), rounder).tolist())
                if rounded not in inters and criterion(rounded, inters):
                    inters.append(rounded)
    return inters
   
def polygon_to_edges(polygon: Polygon):
    b = polygon.boundary.coords
    linestrings = [LineString(b[k:k+2]) for k in range(len(b) - 1)]
    return [list(ls.coords) for ls in linestrings]

def edge_length(edge: Union[tuple, LineString]):
    if isinstance(edge, tuple):
        edge = LineString([edge[0], edge[1]])
    return edge.length

def coords_to_area(coords: Union[tuple, list]):
    polygon = Polygon(coords)
    return polygon.area

def edges_to_polygon(edges: Union[tuple, list]):
    polyy2 = polygonize([LineString(e) for e in edges])
    # return first polygon in collection
    return shapely.get_geometry(polyy2, 0) 

def polygon2D(obs: Polygon):
    return Polygon([el[0:2] for el in polygon_to_tuple_points(obs)])

def point2D(p: Point):
    return shapely.transform(p, lambda x: x) 


def distance_between(p1, p2):
    np1 = np.array(point_to_tuple(p1))
    np2 = np.array(point_to_tuple(p2))
    return np.sqrt(np.sum((np1-np2)**2))

def middle_points( ps: list[Point]):
    middles = set()
    for p, q in itertools.combinations(ps, 2):
        middles.add( Point( (p.x+q.x)/2, (p.y+q.y)/2, (p.z+q.z)/2 if p.has_z and q.has_z else 0 ))
    ps.extend( list(middles) )

def inside_ellipse( ps: list[Point], sam: Polygon):
    # sam.bounds contains the width and height of the sam if desired to model ellipse
    minx, miny, maxx, maxy = sam.bounds
    radx, rady = (maxx - minx)/2, (maxy - miny)/2
    center = shapely.centroid(sam)
    # height = shapely.hausdorff_distance(sam, center)
    height = max(radx, rady)
    cx, cy, cz = center.x, center.y, center.z if center.has_z else 0

    middle_points(ps) # extends ps
    for p in ps:
        x, y = p.x, p.y
        z = p.z if p.has_z else 0
        if (x - cx)**2/radx**2 \
            + (y - cy)**2/rady**2 + (z - cz)**2/height**2 < 1:
            return True
    return False

@overload
def inside_sphere(ps: list[Point], s: Sphere) -> bool: ...
@overload
def inside_sphere(ps: list[Point], center: Point, radius: float) -> bool: ...
def inside_sphere(*args) -> bool:
    if len(args) == 3:
        ps, center, radius = args
        cx, cy, cz, r = center.x, center.y, center.z if center.has_z else 0, radius
    else:
        ps, s = args
        cx, cy, cz, r = s.X, s.Y, 0, s.radius

    middle_points(ps)
    for p in ps:
        x, y = p.x, p.y
        z = p.z if p.has_z else 0
        if (x - cx)**2 + (y - cy)**2 + (z - cz)**2 < r**2:
            return True
    return False

def to_star(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    # get the centroid
    centroid = [(maxx+minx)/2, (maxy+miny)/2]
    # get the diagonal
    diagonal = sqrt((maxx-minx)**2+(maxy-miny)**2)
    square = Point(centroid).buffer(diagonal/sqrt(2.)/2., cap_style='square')
    return square.union(shapely.affinity.rotate(square, 45))

def to_octogon(polygon, large: bool=True):
    minx, miny, maxx, maxy = polygon.bounds
    # get the centroid
    centroid = [(maxx+minx)/2, (maxy+miny)/2, 2]
    # get the diagonal
    diagonal = sqrt((maxx-minx)**2+(maxy-miny)**2)
    octogon = Point(centroid).buffer(diagonal/sqrt(2.)/2., cap_style='square')
    octogon = octogon.union(shapely.affinity.rotate(octogon, 45))
    return Polygon([ p for i, p in enumerate(octogon.exterior.coords[:-1]) if i%2==int(large) ])

# Could save computation by removing large
def to_pentagon(polygon, large: bool=True):
    minx, miny, maxx, maxy = polygon.bounds
    # get the centroid
    centroid = [(maxx+minx)/2, (maxy+miny)/2]
    # get the diagonal
    diagonal = sqrt((maxx-minx)**2+(maxy-miny)**2)
    pentagon = Point(centroid).buffer(diagonal/sqrt(2.)/2., cap_style='square')
    for angle in range(36, 144, 36):
        pentagon = pentagon.union(shapely.affinity.rotate(pentagon, angle))
    # this is required for small errors in the above computation? shapely issue
    pentagon = pentagon.simplify(tolerance=0.01) 
    # for simple whole number polygons, i%8 == 1 is large, and 0 is smaller,
    # but with simplify, it is random, so
    if len(pentagon.exterior.coords[:-1]) > 8:
        pZero = Polygon([ p for i, p in enumerate(pentagon.exterior.coords[:-1]) if i%8==0 ])
        pOne = Polygon([ p for i, p in enumerate(pentagon.exterior.coords[:-1]) if i%8==1 ])
        oneLarger = pOne.area > pZero.area
        if oneLarger and large or not oneLarger and not large:
            return pOne
    else:
        # There are not enough points for the above math to work, just return exterior
        pZero = Polygon([p for p in pentagon.exterior.coords[:-1]])
    return pZero

def verify2DPolygonVisible(pin: Polygon, pout: Polygon|list) -> bool:
    pin = polygon2D(pin)
    if isinstance(pout, Polygon):
        poly = polygon2D(pout)
        return not poly.contains(pin)
    for poly in pout:
        poly = polygon2D(poly)
        if poly.contains(pin):
            return False
    return True

def complete_graph_from_list(L, create_using=None):
    G = nx.empty_graph(L,create_using)
    if len(L)>1:
        if G.is_directed():
            edges = itertools.permutations(L,2)
        else:
            edges = itertools.combinations(L,2)
        G.add_edges_from(edges)
    return G

def path_to_edges(path):
    edges = []
    for i, el in enumerate(path):
        edges.append((el, path[(i + 1) % len(path)]))
    return edges[:-1]

def remove_lines_through_polygons(lines, polygons):
  """
  Removes lines that intersect with any of the given polygons.

  Args:
    lines: A list of Shapely LineString objects.
    polygons: A list of Shapely Polygon objects.

  Returns:
    A list of Shapely LineString objects that do not intersect with any of the
    given polygons.
  """

  # Create a set of all the points that are contained within any of the polygons.
  polygon_points = set()
  for polygon in polygons:
    polygon_points.update(polygon.exterior.coords)
    for hole in polygon.interiors:
      polygon_points.update(hole.coords)

  # Filter the lines to only include those that do not intersect with any of the
  # polygon points.
  filtered_lines = []
  for line in lines:
    if not any(line.intersects(Point(point)) for point in polygon_points):
      filtered_lines.append(line)

  return filtered_lines

if __name__ == '__main__':
    poly = Polygon([[14.471329,46.037286],[14.467378,46.036733],[14.468441,46.034822]])
    # poly_coordinates = mapping(poly)['coordinates'][0]
    # poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]
    poly_ = polygon_to_tuple_points(poly)
    print(json.dumps(poly_))
    print(f"List of points in Polygon: {poly_}")

    p1 = Point([1.2, 3.4, 5.6])
    print(f"Point to coord: {point_to_tuple(p1)}")
    poly_from_points = Polygon(poly_)

    poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 0]])
    edges = polygon_to_edges(poly)
    print(f"List of edges in Polygon: {edges}")

    poly_from_edges = edges_to_polygon(edges)
    plt.plot(  *poly_from_edges.exterior.xy  )# polyy2.get_geometry().exterior.xy)
    plt.show()

    coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)) 
    print(f"Area of coords: {coords_to_area(coords)}")

    LineString(
        [(0, 0), (2, 2)]
    ).equals_exact(
        LineString([(0, 0), (1, 1), (2, 2)]),
        1e-6
    )

    p = Point(2, 2.5)
    p = Point(p.x, 5)
    plt.scatter(p.x, p.y)
    # plt.show()
    poly1 = wkt.loads("POLYGON((1 1,2 1,3 3,2 4,1 3,1 1))")
    poly2 = wkt.loads("POLYGON((1.5 2,3.5 2,3.5 3,1.5 3,1.5 2))")

    shared_region = poly1.intersection(poly2)
    poly1 = poly1.union(shared_region)
    poly2 = poly2.union(shared_region)

    print(f"p to poly1 distance: {poly1.exterior.distance(p)}")

    x,y = poly1.exterior.xy
    plt.plot(x,y)
    plt.plot(*poly2.exterior.xy)
    plt.plot(*shared_region.exterior.xy)
    plt.show()

    S = complete_graph_from_list(["a", "b", "c", "d"])
    print (S.edges() )
    S = complete_graph_from_list([(1,2), (3,4), (5,6)])
    print (S.edges() )


    lstPolys = [shapely.minimum_bounding_circle(Polygon([(1,2), (3,4), (-20, 2), (30, -1)]) ), ]
    square = list( map(to_pentagon, lstPolys) )

    # square[0] = Polygon([ p for i, p in enumerate(polygon_to_tuple_points(square[0])) if i%8==0 ])
    # shapely.plotting.plot_polygon(lstPolys[0])
    # shapely.plotting.plot_polygon(square[0])
    # plt.show()