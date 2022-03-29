
from airflow import DAG
#from airflow.models.variable import Variable
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import json
import pandas as pd
import requests
from datetime import datetime
import os
from sqlalchemy import create_engine

ACCESS_KEY = '93c9fdad5d7027815a553c9ada1d778b'

def read_save_json():
    """Read json data from flights API and save it to local folder."""
    response=requests.get('http://api.aviationstack.com/v1/flights?access_key=' + ACCESS_KEY + '&flight_status=active&limit=100')
    data_dict = response.json()
    
    folder_name = "./jsons/"
    os.makedirs(folder_name, exist_ok=True)
    file_path =  folder_name + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".json"

    with open( file_path, 'w') as file:
        json.dump(data_dict, file)

    return file_path

def create_flights_data(file_path):
    """Read json data  and retreive useful columns."""
    with open(file_path) as file:
        data_dict = json.load(file)
    
    df_raw = pd.DataFrame.from_dict(data_dict['data'])
    
    data = df_raw[['flight_date', 'flight_status']]
    data[['departure_airport', 'departure_timezone']] = pd.json_normalize(df_raw['departure'])[['airport', 'timezone']]
    data[['arrival_airport', 'arrival_timezone', 'arrival_terminal']] = pd.json_normalize(df_raw['arrival'])[['airport', 'timezone', 'terminal']]
    data['airline_name'] = pd.json_normalize(df_raw['airline'])['name']
    data['flight_number'] = pd.json_normalize(df_raw['flight'])['number']
    
    data = replace_string(data)
    file_path = save_processed_file(data)

    return(file_path)
    

def replace_string(data):
    """Replace slash for hifen"""

    data['departure_timezone'] = data['departure_timezone'].str.replace('/','-')
    data['arrival_terminal'] = data['arrival_terminal'].str.replace('/','-')
    
    return(data)

def save_processed_file(data):
    """Save processed file as csv."""
    folder_name = "./processed/"
    os.makedirs(folder_name, exist_ok=True)
    file_path =  folder_name + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".csv"
    data.to_csv(file_path, encoding='utf-8', index=False)
    
    return(file_path) 

def store_in_db(file_path):
    """Insert dataframe in Postgres DB."""
    transformed_data = pd.read_csv(file_path)
    transformed_data.columns = [c.lower() for c in
                                    transformed_data.columns]  # postgres doesn't like capitals or spaces

    transformed_data.dropna(axis=0, how='any', inplace=True)
    engine = create_engine(
        'postgresql://airflow:airflow@postgres/testfligoo')

    transformed_data.to_sql("testdata",
                                engine,
                                if_exists='append',
                                chunksize=500,
                                index=False
                                )

default_args = {
    'owner': 'fligoo',
    'start_date': days_ago(7),
    'retry_delay': timedelta(minutes=1),
    'provide_context': True
}

with DAG(dag_id='aaa_flights_data_read',
         description='read json, transform and insert on DB',
         default_args=default_args, 
         catchup=False,
         render_template_as_native_obj=True,
         schedule_interval='30 14 * * 2') as dag:

    get_and_save_json_data = PythonOperator(
        task_id='read_save_json',
        python_callable=read_save_json,
        dag=dag
    )

    process_and_save_data = PythonOperator(
        task_id='create_flights_data',
        python_callable=create_flights_data,
        op_kwargs={"file_path": "{{ti.xcom_pull('read_save_json')}}"},
        dag=dag
    )
    
    save_into_db = PythonOperator(
        task_id='store_in_db',
        python_callable=store_in_db,
        op_kwargs={"file_path": "{{ti.xcom_pull('create_flights_data')}}"},
        dag=dag
    )

(
    get_and_save_json_data >> process_and_save_data
    >> save_into_db

)
