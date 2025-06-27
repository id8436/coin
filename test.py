import pandas as pd
import mysql.connector
from j1_0_0_get_origin_data import secret


cnx = mysql.connector.connect(**secret.db_info)
cursor = cnx.cursor()

df = pd.read_sql("SELECT * FROM coin LIMIT 10", con=cnx)
print(df)

cnx.close()