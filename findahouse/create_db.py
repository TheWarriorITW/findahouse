# -*- coding: utf-8 -*-

from shapefile import Reader
from pyproj import Proj, transform

lambert_93 = Proj("+init=EPSG:2154")
wgs_84 = Proj("+init=EPSG:4326")



def conversion_lambert93_wgs84_dep(limite_lambert):
    limite_wgs84 = []
    for coord in limite_lambert:
        lon, lat = transform(lambert_93, wgs_84, coord[0], coord[1])
        limite_wgs84.append([lon, lat])
    return limite_wgs84

def creer_departement_json(info, limite):
    departement_json = {}
    departement_json["type"] = "Feature"
    departement_json["properties"] = {"Numero_departement": info[1],\
        "nom_departement": info[2], "code_prefecture": info[3],\
        "code_region": info[9]}
    departement_json["geometry"] = {"type": "MultiPolygon", "coordinates":  [limite]}
    return departement_json

def extraction_shp_departement(chemin):
    '''Structure info_departement
     0  :   Numéro departement
     1  :   Nom departement en majuscule
     2  :   Code geographique de la prefecture
     3  :   Code region
     4  :   limite en coordonne wgs84'''
    sf = Reader(chemin)
    shapeRecs = sf.shapeRecords()
    points = shapeRecs[5].shape.points
    record = shapeRecs[5].record
    info_departement = []
    for dep in shapeRecs:
        info = dep.record
        limite = conversion_lambert93_wgs84_dep(dep.shape.points)
        departement_json = creer_departement_json(info, limite)
        info_departement.append([info[1], info[2], info[3], info[9],\
            departement_json])
    return info_departement
    
if __name__ == '__main__':
    information_departement = extraction_shp_departement('./data/DEPARTEMENT/DEPARTEMENT')
    for i in information_departement:
        dep_str = '# : {}, Nom : {}, Préfecture : {}, Région : {}'.format(i[0],
        i[1], i[2], i[3])
        print dep_str
