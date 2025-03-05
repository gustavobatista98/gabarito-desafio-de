import json
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import exc

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Uses google storage link to retrieve order category data

category_url = 'https://storage.googleapis.com/challenge_junior/categoria.parquet'

production_cred_file = open("/opt/airflow/dags/modules/production_credentials.json")

credentials = json.load(production_cred_file)

database = credentials["database"]
user = credentials["user"]
host = credentials["host"]
password = credentials["password"]
port = credentials["port"]

def get_category():

    try:
        logger.info("Retrieving categories...")

        engine_url = URL.create(
            "postgresql",
            username=user,
            password=password,
            host=host,
            database=database
        )
        
        engine = create_engine(engine_url)

        categories = pd.read_parquet(category_url)

        logger.info("Saving categories to database...")
        
        categories.to_sql("category", engine, if_exists="replace", index=False)

    except:
        logger.info("Erro no processamento das categorias")
