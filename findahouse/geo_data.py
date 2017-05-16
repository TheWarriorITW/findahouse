# -*- coding: utf-8 -*-
from shapefile import Reader
from pyproj import Proj, transform

lambert_93 = Proj("+init=EPSG:2154")
wgs_84 = Proj("+init=EPSG:4326")

# Exemple d'utilisation de la librairie pyproj
# lat, lon = 656936.8, 3042238.0
# x, y = transform(lambert, wgs84, lat, lon)

sf = Reader("./tipi/data/DEPARTEMENT/DEPARTEMENT")
shapes = sf.shapes()
shapeRecs = sf.shapeRecords()
points = shapeRecs[5].shape.points

print shapeRecs[5].record
# print points

limite_departement = []
for i in points:
    lon, lat = transform(lambert_93, wgs_84, i[0], i[1])
    limite_departement.append([lon, lat])
    

departement = {
    "type": "Feature",
    "properties": {"party": "Republican"},
    "style" : {
    "color": "#ff7800",
    "weight": 5,
    "opacity": 0.65
    },
    "geometry": {
        "type": "Polygon",
          "coordinates": [[
            [2, 45],
            [2.5,  45],
            [2.5,  45.5],
            [2, 45.5],
        ]]
    }
}



departement["geometry"]["coordinates"] = [limite_departement]
print departement

def test():
    return departement


