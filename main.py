from database import db_session
from models import *

maxes = [48.753807, 21.326419]
mins = [48.665355, 21.216874]

number_of_rows = 25

latitutde_dif = maxes[0] - mins[0]
longtitude_dif = maxes[1] - mins[1]


width_shift = latitutde_dif/number_of_rows
height_shift = longtitude_dif/number_of_rows

print(width_shift, height_shift)

matrix = []

for i in range(number_of_rows):
    row = []
    for j in range(number_of_rows):
        latitutde = mins[0] + width_shift*j
        longtitude = mins[1] + height_shift*i
        row.append([latitutde, longtitude])

    matrix.append(row)

print(matrix[0][0])
print(matrix[1][1])


polygons = []

for i in range(number_of_rows):
    row = []
    for j in range(number_of_rows):
        polgo = Polygon()
        polgo.latitude_1 = mins[0] + width_shift*j
        polgo.longtitude_1 = mins[1] + height_shift*i

        polgo.latitude_2 = mins[0] + width_shift * j
        polgo.longtitude_2 = mins[1] + height_shift * (i + 1)

        polgo.latitude_3 = mins[0] + width_shift * (j + 1)
        polgo.longtitude_3 = mins[1] + height_shift * (i + 1)

        polgo.latitude_4 = mins[0] + width_shift * (j + 1)
        polgo.longtitude_4 = mins[1] + height_shift * i

        db_session.add(polgo)
        #row.append([latitutde_1, longtitude_1, latitutde_2, longtitude_2, latitutde_3, longtitude_3, latitutde_4, longtitude_4,])

    #polygons.append(row)

db_session.commit()
print()
