import json
import requests
import pandas as pd
import warnings
from models import *

warnings.filterwarnings("ignore", category=FutureWarning)

# Azure Maps API
subscriptionKey = "mdvhwX6Era11JlFA5Mtx9Lar7xnzUxQc_6fuvtQ8p_w"



url2 = "https://raw.githubusercontent.com/caliline2/Hack_Kosice/main/DataTypesAzureMap.csv"

matrix = pd.read_csv(url2)

# User input address
addresstoAnalyze = input(
    "Enter an address to analyze: ")  # Analyzing the Catchment Area for the Starbucks Store (400, Pine Street, Seattle) in Westlake Center, Seattle.
locationDetails = requests.get(
    "https://atlas.microsoft.com/search/address/json?subscription-key={}&api-version=1.0&query={}".format(
        subscriptionKey, addresstoAnalyze)).json()
latlong = locationDetails["results"][0]["position"]
currentLocation = [0, 0]
currentLocation[0] = latlong["lat"]
currentLocation[1] = latlong["lon"]

# return lat long of the point (to be printed in front end)

print("Lat Long for", addresstoAnalyze, "is", latlong)
walkingTime = 300  # this is 600secs. you can experiment with different values
cTraffic = "true"  # you can test how far you can go in current traffic
tMode = "pedestrian"  # you can change this to car, bus, pedestrian, bicycle and more. see http://bit.ly/2nGErtX for details

# Calculate polygon x minutes distance
routeRangeResponse = requests.get(
    "https://atlas.microsoft.com/route/range/json?subscription-key={}&api-version=1.0&query={}&timeBudgetInSec={}&traffic={}&travelmode={}".format(
        subscriptionKey, str(currentLocation[0]) + "," + str(currentLocation[1]), walkingTime, cTraffic, tMode)).json()
routeRangeResponseF = json.dumps(routeRangeResponse, indent=4)
print(routeRangeResponseF)

polyBounds = routeRangeResponse["reachableRange"]["boundary"]

for i in range(len(polyBounds)):
    coordList = list(polyBounds[i].values())
    coordList[0], coordList[1] = coordList[1], coordList[0]
    polyBounds[i] = coordList

polyBounds.pop()
polyBounds.append(polyBounds[0])

boundsData = {
    "geometry": {
        "type": "Polygon",
        "coordinates":
            [
                polyBounds
            ]
    }
}

boundsDataF = json.dumps(boundsData, indent=4)
print(boundsDataF)

poiNames = [cat.name for cat in Categories.query.all()]

# Calculating count = counting
# Observations = to display on the map

n = 0
counting = pd.DataFrame(columns=['Category', 'Count'])
observations = pd.DataFrame(columns=['Category', 'Name', 'Latitude', 'Longitude'])

for n in range(106):
    if n >= len(poiNames):
        break
    poiName = poiNames[n]
    searchPolyResponse = requests.post(
        url="https://atlas.microsoft.com/search/geometry/json?subscription-key={}&api-version=1.0&query={}&idxSet=POI&limit=50".format(
            subscriptionKey, poiName), json=boundsData).json()
    numRes = searchPolyResponse["summary"]["numResults"]
    print("Total Number of " + poiName + " nearby: ", numRes)
    counting = counting.append({'Category': poiName, 'Count': numRes}, ignore_index=True)
    print("Here is a list of the Search Results: ")
    for loc in range(len(searchPolyResponse["results"])):
        print(loc + 1, ". ", searchPolyResponse["results"][loc]["poi"]["name"])
    for loc in range(len(searchPolyResponse["results"])):
        print(loc + 1, ". ", searchPolyResponse["results"][loc]["poi"]["name"])
        latitude = searchPolyResponse["results"][loc]["position"]["lat"]
        longitude = searchPolyResponse["results"][loc]["position"]["lon"]
        print("Latitude: ", latitude)
        print("Longitude: ", longitude)
        observations = counting.append(
            {'Category': poiName, 'Name': (loc + 1, ". ", searchPolyResponse["results"][loc]["poi"]["name"]),
             'Latitude': latitude, 'Longitude': longitude}, ignore_index=True)

print(counting)
# observations = observations.dropna(subset=['Name'], inplace=True)
# print(observations)

# Merging matrix with counting per polygon
ranking = pd.merge(counting, matrix)

ranking['Industrial_Rank'] = ranking['Scoring_industrial'] * ranking['Count']
ranking['F&B'] = ranking['Scoring_F&B'] * ranking['Count']
ranking['Scoring_amenities'] = ranking['Scoring_amenities'] * ranking['Count']

# Normalizing to 0-100
Industrial_Ranking = ranking['Industrial_Rank'].sum()
Industrial_Ranking = min(Industrial_Ranking / 500, 1) * 100  # normalize score to 0-100 range
Industrial_Ranking = min(Industrial_Ranking, 100)  # cap the score at 100

FoodandBeverage_Ranking = ranking['F&B'].sum()
FoodandBeverage_Ranking = min(FoodandBeverage_Ranking / 500, 1) * 100  # normalize score to 0-100 range
FoodandBeverage_Ranking = min(FoodandBeverage_Ranking, 100)  # cap the score at 100

Public_Amenities_Ranking = ranking['Scoring_amenities'].sum()
Public_Amenities_Ranking = min(Public_Amenities_Ranking / 500, 1) * 100  # normalize score to 0-100 range
Public_Amenities_Ranking = min(Public_Amenities_Ranking, 100)  # cap the score at 100

print("Industrial Ranking is ", Industrial_Ranking)
print("F&B Ranking is ", FoodandBeverage_Ranking)
print("Public Amenities Ranking is ", Public_Amenities_Ranking)