"""Add UTM coordinates to file with lat,lon coordinates.
UTM coordinates easting and northing are in meters,
so X and Y coordinates in same units,
unlike degrees of latitude and longitude. On the other hand,
UTM coordinates must be rooted at a point identified by a zone,
and will be distorted from common map coordinates at long distances
from that origin.

Wildfire CSV file has been pruned to Oregon, which is in UTM zones T 10 and T 11;
we'll use T 10.
"""
import utm
import csv

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Configuration constants
SRC = "data/WFIGS_-_Wildland_Fire_Locations_Full_History.csv"
DEST = "data/fire_locations_utm.csv"
# Headers of latitude and longitude columns in SRC file
LAT_COL = "Y"
LON_COL = "X"
# Fixed UTM zone so that coordinates are uniform and
# consistent with UTM zone base of map origin.
# Oregon is T10 (western 2/3) and T11 (eastern).
UTM_ZONE_NUM = 10
UTM_ZONE_LET = "T"


with open(SRC, newline='', encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    # Have field names been initialized at this point? (Yes)
    fields = ["Easting", "Northing", "UTM Zone"] + reader.fieldnames
    log.debug(f"Field names {fields}")
    with open(DEST, "w") as outfile:
        writer = csv.DictWriter(outfile, fields)
        writer.writeheader()
        for row in reader:
            lat = float(row[LAT_COL])
            lon = float(row[LON_COL])
            easting, northing, _, _ = utm.from_latlon(lat, lon,
                                                      force_zone_number=UTM_ZONE_NUM,
                                                      force_zone_letter=UTM_ZONE_LET)
            row["Easting"] = int(easting)
            row["Northing"] = int(northing)
            row["UTM Zone"] = UTM_ZONE_LET + str(UTM_ZONE_NUM)
            writer.writerow(row)


