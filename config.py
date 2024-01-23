"""Configuration file, wildfires k-means clustering.

This should be all the constants that must be changed to
substitute a different data set and base map for the
provided Oregon wildfires data set and Oregon base map.
See also the README file in the data directory for
notes on obtaining suitable datasets and basemaps, and program
add_utm.py for augmenting a data set with UTM coordinates.
"""

FIRE_DATA_PATH = "data/fire_locations_utm.csv"
BASEMAP_PATH = "data/Oregon.png"
BASEMAP_SIZE = (1024, 783)
# Origin    (-124.9, 41.8) =  342151, 4629315 10T
# NE corner (-116.3, 46.5) = 1014041, 5171453 10T
BASEMAP_ORIGIN_EASTING = 342151
BASEMAP_ORIGIN_NORTHING = 4629315
BASEMAP_EXTENT_EASTING = 1014041
BASEMAP_EXTENT_NORTHING = 5171453
BASEMAP_WIDTH_UTM = BASEMAP_EXTENT_EASTING - BASEMAP_ORIGIN_EASTING
BASEMAP_HEIGHT_UTM =  BASEMAP_EXTENT_NORTHING - BASEMAP_ORIGIN_NORTHING

# How many clusters should we try to make?
N_CLUSTERS = 10

# How long will we allow the algorithm to run?
# (It will usually end much sooner)
MAX_ITERATIONS = 30