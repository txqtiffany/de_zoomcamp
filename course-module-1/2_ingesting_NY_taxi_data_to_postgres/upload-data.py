import pandas as pd
from sqlalchemy import create_engine
from time import time
import psycopg2

# alternative way of assessing the entire dataset
# url = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"
# df = pd.read_csv(url)

# Read in the sample dataset for creating the SQL table schema
df = pd.read_csv('yellow_head.csv')

# Get schema and generate DDL statements for creating SQL tables of this df
print(pd.io.sql.get_schema(df, name="yellow_taxi_data"))

# Create connection to postgres via SQLAlchemy
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Create the table via the connection using the DDL statements
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

# Using the iterator tool to break the file into smaller chunks
df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

while True:
    t_start = time()

    df = next(df_iter)

    # Fix data types by parsing 2 columns into datetime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    t_end = time()

    print("inserting one chunk... took %.3f seconds" % (t_end - t_start))
