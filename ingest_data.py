import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import time
import argparse
import os

def main(params):
    # parameters
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    csv_name = params.csv_name
    
    # Creating the database connection
    print("Connecting to database...")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Creating the iterator to read the file in chunks
    print(f"Reading CSV file: {csv_name}")
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    print("Starting to load data...")
    
    # First chunk to create the table
    df = next(df_iter)
    
    # converating the date columns to datetime
    df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp)
    df.order_approved_at = pd.to_datetime(df.order_approved_at)
    df.order_delivered_carrier_date = pd.to_datetime(df.order_delivered_carrier_date)
    df.order_delivered_customer_date = pd.to_datetime(df.order_delivered_customer_date)
    df.order_estimated_delivery_date = pd.to_datetime(df.order_estimated_delivery_date)
    
    # Creating the table and schema, replacing it if it exists
    df.to_sql(name=table_name, con=engine, if_exists='replace')
    print(f"Created table '{table_name}' and inserted the first chunk...")

    # Looping through the rest of the chunks
    for chunk in df_iter:
        t_start = time.time()
        
        # converating the date columns to datetime
        chunk.order_purchase_timestamp = pd.to_datetime(chunk.order_purchase_timestamp)
        chunk.order_approved_at = pd.to_datetime(chunk.order_approved_at)
        chunk.order_delivered_carrier_date = pd.to_datetime(chunk.order_delivered_carrier_date)
        chunk.order_delivered_customer_date = pd.to_datetime(chunk.order_delivered_customer_date)
        chunk.order_estimated_delivery_date = pd.to_datetime(chunk.order_estimated_delivery_date)
        
        # Appending the chunk to the database
        chunk.to_sql(name=table_name, con=engine, if_exists='append')
        
        t_end = time.time()
        
        print(f'Inserted another chunk, took {t_end - t_start:.3f} seconds')

    print("Finished loading all data!")

if __name__ == '__main__':
    # setting up all the command-line arguments
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table to write to')
    parser.add_argument('--csv_name', help='name of the csv file')

    args = parser.parse_args()
    
    main(args)