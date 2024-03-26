
from shapely import Polygon
import shapely

import shapely.geometry as geom

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
    if not any(line.intersects(geom.Point(point)) for point in polygon_points):
      filtered_lines.append(line)

  return filtered_lines

# Example usage:
if __name__ == "__main__":
    c = 5.5#sam['lat']
    b = -10#sam['lng']
    r = 2#sam['widthFeet']/364000
    #Eq = y=c±√r^2−(x−b)^2
    p1 = (b, c+r) #coord pair for x=b
    p2 = (b+r, c) #coord pair for y=c
    p3 = (b-r, c) #coord pair for y=c
    p4 = (b, c-r) #coord pair for x=b
    poly = Polygon([p1, p2, p3, p4])
    print(p1, p2, p3, p4)
    # circle = shapely.minimum_bounding_circle(poly)
    # shapely.plotting.plot_polygon(circle)

    lines = [
        geom.LineString([(0, 0), (10, 10)]), 
        geom.LineString([(5, 5), (15, 15)]), 
        geom.LineString([(1,1), (11,11)]),
        geom.LineString([(11,11), (12,13)])
    ]
    polygons = [geom.Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])]

    filtered_lines = remove_lines_through_polygons(lines, polygons)

    print(filtered_lines)