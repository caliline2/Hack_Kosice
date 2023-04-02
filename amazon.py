from flask import Flask, jsonify, request
from sqlalchemy import desc
from models import *
import json
import requests
import pandas as pd


app = Flask(__name__)



# Azure Maps API
subscriptionKey = "mdvhwX6Era11JlFA5Mtx9Lar7xnzUxQc_6fuvtQ8p_w"

url2 = "https://raw.githubusercontent.com/caliline2/Hack_Kosice/main/DataTypesAzureMap.csv"


@app.route("/test/")
def test_fun():
    return jsonify('''{"type":"FeatureCollection","features":[{ "type": "Feature", "geometry": { "type": "Polygon", "coordinates": [ [ [ 48.70781196, 21.260692 ], [ 48.70781196, 21.2650738 ], [ 48.71135004, 21.2650738 ], [ 48.71135004, 21.260692 ] ] ] } }, { "type": "Feature", "geometry": { "type": "Polygon", "coordinates": [ [ [ 48.72904044, 21.2563102 ], [ 48.72904044, 21.260692 ], [ 48.73257852, 21.260692 ], [ 48.73257852, 21.2563102 ] ] ] } } ] }''')


@app.route("/cat/<category>/")
def category_fun(category):
    polygons = Polygon.query.order_by(desc(Polygon.scoring_f_b)).limit(30).all()
    category = Categories.query.filter(Categories.name == category).first()

    actual_polygons = []
    for polygon in polygons:
        if category not in polygon.categories:
            actual_polygons.append(polygon)

    total_polygons = [pol for pol in actual_polygons]

    final_geojson_string = '''{ "type": "FeatureCollection", "features": [  '''
    for polygon in total_polygons[:10]:
        final_geojson_string += '''{ "type": "Feature", "properties":{}, "geometry": { "type": "Polygon", "coordinates": [ [ [ ''' + str(
            polygon.longtitude_1) + ''', ''' + str(polygon.latitude_1) + ''' ], [ ''' + str(polygon.longtitude_2) + ''', ''' + str(
            polygon.latitude_2) + ''' ], [ ''' + str(polygon.longtitude_3) + ''', ''' + str(polygon.latitude_3) + ''' ], [ ''' + str(
            polygon.longtitude_4) + ''', ''' + str(polygon.latitude_4) + ''' ], [ ''' + str(polygon.longtitude_1) + ''', ''' + str(
            polygon.latitude_1) + ''' ] ] ] } },'''

    final_geojson_string = final_geojson_string[:-1] + "] }"
    return final_geojson_string


@app.route("/get-ventures/")
def get_ventures_fun():

    return '''{ "type": "FeatureCollection", "features":[{ "type": "Feature", "properties":{"name":"Piváreň Troja"}, "geometry": { "type": "Point", "coordinates": [ 21.24192, 48.71498 ] } },{ "type": "Feature", "properties":{"name":"Šport Pub"}, "geometry": { "type": "Point", "coordinates": [ 21.2411, 48.71519 ] } },{ "type": "Feature", "properties":{"name":"Vigvam pub"}, "geometry": { "type": "Point", "coordinates": [ 21.23872, 48.71385 ] } },{ "type": "Feature", "properties":{"name":"Starobrno Pub"}, "geometry": { "type": "Point", "coordinates": [ 21.24304, 48.7128 ] } },{ "type": "Feature", "properties":{"name":"JULYDENT"}, "geometry": { "type": "Point", "coordinates": [ 21.23916, 48.7128 ] } },{ "type": "Feature", "properties":{"name":"KALLADENT"}, "geometry": { "type": "Point", "coordinates": [ 21.23916, 48.7128 ] } },{ "type": "Feature", "properties":{"name":"Zubná ambulancia"}, "geometry": { "type": "Point", "coordinates": [ 21.23885, 48.71324 ] } },{ "type": "Feature", "properties":{"name":"Turistická ubytovňa"}, "geometry": { "type": "Point", "coordinates": [ 21.23902, 48.71299 ] } },{ "type": "Feature", "properties":{"name":"Ubytovňa"}, "geometry": { "type": "Point", "coordinates": [ 21.24047, 48.7165 ] } },{ "type": "Feature", "properties":{"name":"Drink Market, S. R. O."}, "geometry": { "type": "Point", "coordinates": [ 21.23885, 48.71324 ] } },{ "type": "Feature", "properties":{"name":"Fragaria"}, "geometry": { "type": "Point", "coordinates": [ 21.23903, 48.71246 ] } },{ "type": "Feature", "properties":{"name":"K-Tel S. R. O."}, "geometry": { "type": "Point", "coordinates": [ 21.24373, 48.71162 ] } },{ "type": "Feature", "properties":{"name":"Dkf SRO"}, "geometry": { "type": "Point", "coordinates": [ 21.23916, 48.7128 ] } }] }'''


@app.route("/get-ventures-data/")
def get_ventures_data_fun():
    return {"IndustrialRanking": 0.2, "F&B Ranking" :  1.4000000000000001, "Public Amenities Ranking" :  1.0}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
