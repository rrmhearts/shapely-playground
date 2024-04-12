from matplotlib import pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon

poly1 = Polygon([(0,0), (2,0), (2,2), (0,2)])
poly2 = Polygon([(2,2), (4,2), (4,4), (2,4)])
poly3 = Polygon([(1,1), (3,1), (3,3), (1,3)])
poly4 = Polygon([(3,3), (5,3), (5,5), (3,5)])
poly5 = Polygon([(7,7), (8,8), (9,9), (7,9)])
polys = [poly1, poly2, poly3, poly4, poly5]     

gpd.GeoSeries(polys).boundary.plot()
plt.show()

from shapely.ops import unary_union

mergedPolys = unary_union(polys)
print(list(mergedPolys.geoms) )
gpd.GeoSeries([mergedPolys]).boundary.plot()
plt.show()