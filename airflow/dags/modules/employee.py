import json
import logging
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import exc

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Uses API call to retrieve employees data
# If requests not succeeds, return HHTP error

production_cred_file = open("/opt/airflow/dags/modules/production_credentials.json")

credentials = json.load(production_cred_file)

database = credentials["database"]
user = credentials["user"]
host = credentials["host"]
password = credentials["password"]
port = credentials["port"]

get_link = "https://us-central1-bix-tecnologia-prd.cloudfunctions.net/api_challenge_junior?id="

def get_employee():

    logger.info("Retrieving employees...")

    employee = {}
    try:
        i = 1
        while True:
            response = requests.get(get_link + str(i))
            if response.text != "The argument is not correct":
                employee.update({i: requests.get(get_link + str(i)).text})
                i += 1
            else:
                break
            
        engine_url = URL.create(
            "postgresql",
            username=user,
            password=password,
            host=host,
            database=database
        )
        
        engine = create_engine(engine_url)
        
        employees  = pd.DataFrame(employee.items(), columns=['id','empregado'])
        
        logger.info("Saving employees to database...")

        employees.to_sql("empolyee", engine, if_exists="replace", index=False)

    except requests.exceptions.HTTPError as err:
            print(err)

