

first_polygon = [[48.71488812, 21.2519284], [48.71488812, 21.2563102], [48.7184262, 21.2563102], [48.7184262, 21.2519284]]
second_polygon = [[48.75026892, 21.260692], [48.75026892, 21.2650738], [48.753807, 21.2650738], [48.753807, 21.260692]]
third_polygon = [[48.665355, 21.2650738], [48.665355, 21.2694556], [48.66889308, 21.2694556], [48.66889308, 21.2650738]]
fourth_polygon = [[48.71135004, 21.2694556], [48.71135004, 21.2738374], [48.71488812, 21.2738374], [48.71488812, 21.2694556]]

total_logins = [first_polygon, second_polygon, third_polygon, fourth_polygon]

final_geojson_string = '''{ "type": "FeatureCollection", "features": [  '''

for polygon in total_logins:
    final_geojson_string += '''{ "type": "Feature", "properties":{}, "geometry": { "type": "Polygon", "coordinates": [ [ [ '''+ str(polygon[0][1]) + ''', ''' + str(polygon[0][0]) + ''' ], [ ''' + str(polygon[1][1]) + ''', ''' + str(polygon[1][0]) + ''' ], [ ''' + str(polygon[2][1]) + ''', ''' + str(polygon[2][0]) + ''' ], [ ''' + str(polygon[3][1]) + ''', ''' + str(polygon[3][0]) + ''' ], [ ''' + str(polygon[0][1]) + ''', ''' + str(polygon[0][0]) + ''' ] ] ] } },'''

final_geojson_string = final_geojson_string[:-1] + "] }"
print(final_geojson_string)
