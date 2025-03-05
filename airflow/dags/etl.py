import logging
import datetime
import airflow
from airflow.operators.python import PythonOperator

from modules.orders import get_orders
from modules.employee import get_employee
from modules.category import get_category

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Initializing process...")

# Defines Airflow's DAG with job scheduler to once a day at 4:30 AM
dag = airflow.DAG(

    'etl',

    default_args={'start_date': datetime.datetime(2024, 1, 1)},

    schedule='30 7 * * *',

    catchup=False

)

# Creates run task operator for ETL process

get_category = PythonOperator(

    task_id='get_category',

    python_callable=get_category,

    dag=dag

)

get_employee = PythonOperator(

    task_id='get_employee',

    python_callable=get_employee,

    dag=dag

)

get_orders = PythonOperator(

    task_id='get_orders',

    python_callable=get_orders,

    dag=dag

)

# Runs the job

get_category >> get_employee >> get_orders

logger.info("Process completed")
