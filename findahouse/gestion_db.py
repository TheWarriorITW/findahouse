# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shapefile import Reader
from pyproj import Proj, transform

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tipi:r2d2@localhost/geo_data'
db = SQLAlchemy(app)
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
    departement_json["geometry"] = {"type": "Polygon", "coordinates":  [limite]}
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

class Departement(db.Model):
    numero_departement = db.Column(db.String(2), primary_key=True)
    nom_departement = db.Column(db.String(80), unique=True)
    code_prefecture = db.Column(db.String(5))
    code_region = db.Column(db.String(5))
    limite_departement = db.Column(db.JSON)

    def __init__(self, numero_departement, nom_departement, code_prefecture,\
                 code_region, limite_departement):
        self.numero_departement = numero_departement
        self.nom_departement = nom_departement
        self.code_prefecture = code_prefecture
        self.code_region = code_region
        self.limite_departement = limite_departement

    def __repr__(self):
        return '<Departement %r>' % self.nom_departement

if __name__ == '__main__':
    from create_db import extraction_shp_departement
    db.create_all()
    departements = extraction_shp_departement('./data/DEPARTEMENT/DEPARTEMENT')
    for dep_tmp in departements:
        ligne = Departement(dep_tmp[0], dep_tmp[1], dep_tmp[2], dep_tmp[3],\
            dep_tmp[4])
        db.session.add(ligne)
        print ligne
    db.session.commit()
    print 'Recuperation departement'


