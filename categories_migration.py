import pandas as pd
from models import *
from database import *

# Replace 'path/to/your/file.xlsx' with the actual path to your Excel file
df = pd.read_excel('side_files/DataTypesAzureMap.xlsx')

# Loop through the rows of the DataFrame
for index, row in df.iterrows():
    # Access the columns of the row as a list
    columns = row.iloc[:].tolist()

    category = Categories(columns[3])
    category.scoring_industrial = columns[0]
    category.scoring_f_b = columns[1]
    category.scoring_amenities = columns[2]
    category.matching_code = columns[4]

    db_session.add(category),0


db_session.commit()
