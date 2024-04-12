from shapely.geometry import Point, Polygon, LineString, mapping
import matplotlib.pyplot as plt
import json
import shapely
import itertools
import networkx as nx
import numpy as np

from shapely import wkt, polygonize
from typing import Union
from math import sqrt

def polygon_to_tuple_points(polygon: Polygon):
    poly_coordinates = mapping(polygon)['coordinates'][0]
    # poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]
    poly_ = [(coords[0], coords[1]) for coords in poly_coordinates]
    # Mind that the above output will contain one point two times, the first and last points
    return poly_[:-1]

def point_to_tuple(point: Point):
    return tuple(point.coords)[0]

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
    pZero = Polygon([ p for i, p in enumerate(pentagon.exterior.coords[:-1]) if i%8==0 ])
    pOne = Polygon([ p for i, p in enumerate(pentagon.exterior.coords[:-1]) if i%8==1 ])

    oneLarger = pOne.area > pZero.area
    if oneLarger and large or not oneLarger and not large:
        return pOne
    return pZero


def complete_graph_from_list(L, create_using=None):
    G = nx.empty_graph(L,create_using)
    if len(L)>1:
        if G.is_directed():
            edges = itertools.permutations(L,2)
        else:
            edges = itertools.combinations(L,2)
        G.add_edges_from(edges)
    return G

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

