import json
import logging
import psycopg2
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import exc

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Module implemented to retrieve orders data from BIX database and return it as a pandas dataframe

# Defines BIX database variables using file to simulate ambient variables file

raw_cred_file = open('/opt/airflow/dags/modules/raw_credentials.json')
raw_credentials = json.load(raw_cred_file)

prod_cred_file = open('/opt/airflow/dags/modules/production_credentials.json')
prod_credentials = json.load(prod_cred_file)

raw_database = raw_credentials["database"]
raw_user = raw_credentials["user"]
raw_host = raw_credentials["host"]
raw_password = raw_credentials["password"]
raw_port = raw_credentials["port"]

prod_database = prod_credentials["database"]
prod_user = prod_credentials["user"]
prod_host = prod_credentials["host"]
prod_password = prod_credentials["password"]
prod_port = prod_credentials["port"]


def get_orders():
    logger.info("Retrieving orders...")
    #Try to connect with origin database, process tables and return it to a pandas dataframe

    try:
        with psycopg2.connect(database = raw_database, 
                                user = raw_user, 
                                host= raw_host,
                                password = raw_password,
                                port = raw_port) as conn:

            cursor = conn.cursor()

            cursor.execute("""SELECT * FROM public.venda""")

            tuples_list = cursor.fetchall()

            cursor.close()

            orders = pd.DataFrame(tuples_list, columns = ['id_venda', 'id_funcionario', 'id_categoria', 'data_venda', 'venda'])
    
    # Return error in case of origin database error

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    #Try to connect with production database to save the processed data
    logger.info("Saving orders to database...")
    try:
        engine_url = URL.create(
            "postgresql",
            username=prod_user,
            password=prod_password,
            host=prod_host,
            database=prod_database
        )

        engine = create_engine(engine_url)
        
        orders.to_sql("orders", engine, if_exists="replace", index=False)

    # Return error in case of database fails

    except (Exception, exc.SQLAlchemyError) as error:
        print(error)
