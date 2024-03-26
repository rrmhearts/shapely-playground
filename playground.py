from shapely.geometry import Point, Polygon, LineString, mapping
import matplotlib.pyplot as plt
import json
import shapely
from shapely import wkt, polygonize
from typing import Union

def polygonToPoints(polygon: Polygon):
    poly_coordinates = mapping(poly)['coordinates'][0]
    # poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]
    poly_ = [(coords[0], coords[1]) for coords in poly_coordinates]
    # Mind that the above output will contain one point two times, the first and last points
    return poly_[:-1]

def pointToCoordinate(point: Point):
    return tuple(point.coords)[0]
    try:
        return (point.x, point.y, point.z)
    except shapely.errors.DimensionError:
        return (point.x, point.y)

def polygonToEdges(polygon: Polygon):
    b = polygon.boundary.coords
    linestrings = [LineString(b[k:k+2]) for k in range(len(b) - 1)]
    return [list(ls.coords) for ls in linestrings]

def coordsToArea(coords: Union[tuple, list]):
    polygon = Polygon(coords)
    return polygon.area

def edgesToPolygon(edges: Union[tuple, list]):
    polyy2 = polygonize([LineString(e) for e in edges])
    # return first polygon in collection
    return shapely.get_geometry(polyy2, 0) 

if __name__ == '__main__':
    poly = Polygon([[14.471329,46.037286],[14.467378,46.036733],[14.468441,46.034822]])
    # poly_coordinates = mapping(poly)['coordinates'][0]
    # poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]
    poly_ = polygonToPoints(poly)
    print(json.dumps(poly_))
    print(f"List of points in Polygon: {poly_}")

    p1 = Point([1.2, 3.4, 5.6])
    print(f"Point to coord: {pointToCoordinate(p1)}")
    poly_from_points = Polygon(poly_)

    poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 0]])
    edges = polygonToEdges(poly)
    print(f"List of edges in Polygon: {edges}")

    poly_from_edges = edgesToPolygon(edges)
    plt.plot(  *poly_from_edges.exterior.xy  )# polyy2.get_geometry().exterior.xy)
    plt.show()

    coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)) 
    print(f"Area of coords: {coordsToArea(coords)}")

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

