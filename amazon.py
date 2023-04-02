from flask import Flask, jsonify
from sqlalchemy import desc
from models import *

app = Flask(__name__)


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




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")