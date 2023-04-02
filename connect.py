import os
import json
import time
import requests
import urllib.parse
from IPython.display import Image, display
from models import *
from database import db_session
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# Azure Maps API
subscriptionKey = "mdvhwX6Era11JlFA5Mtx9Lar7xnzUxQc_6fuvtQ8p_w"

matrix = pd.read_excel('side_files/DataTypesAzureMap.xlsx')


def rank_polygon(sel_polygon):

    boundsData = {
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [sel_polygon.longtitude_1, sel_polygon.latitude_1],
                    [sel_polygon.longtitude_2, sel_polygon.latitude_2],
                    [sel_polygon.longtitude_3, sel_polygon.latitude_3],
                    [sel_polygon.longtitude_4, sel_polygon.latitude_4],
                    [sel_polygon.longtitude_1, sel_polygon.latitude_1]
                ]
            ]
        }
    }

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
        print(searchPolyResponse)
        numRes = searchPolyResponse["summary"]["numResults"]
        print("Total Number of " + poiName + " nearby: ", numRes)
        if numRes > 0:
            counting = counting.append({'Category': poiName, 'Count': numRes}, ignore_index=True)
            cat = Categories.filter(Categories.name == poiName).first()
            sel_polygon.categories.append(cat)
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
    ranking = pd.merge(counting, matrix, on='Category')

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

    sel_polygon.scoring_industrial = Industrial_Ranking
    sel_polygon.scoring_f_b = FoodandBeverage_Ranking
    sel_polygon.scoring_amenities = Public_Amenities_Ranking


sel_polygan = Polygon.query.filter(Polygon.id == 325).first()
rank_polygon(sel_polygan)


db_session.commit()
