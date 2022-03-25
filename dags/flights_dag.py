
from airflow import DAG
#from airflow.models.variable import Variable
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import json
import pandas as pd
import requests


def read_json():
    """Read json data from flights API."""
    response=requests.get('http://api.aviationstack.com/v1/flights?access_key=93c9fdad5d7027815a553c9ada1d778b&flight_status=active&limit=100')
    data_dict = response.json()
    
    return data_dict

def create_flights_data(data_dict):
    """Unnest json data from dictionary and retreive useful columns."""
    df_raw = pd.DataFrame.from_dict(data_dict['data'])
    
    data = df_raw[['flight_date', 'flight_status']]
    data[['departure_airport', 'departure_timezone']] = pd.json_normalize(df_raw['departure'])[['airport', 'timezone']]
    data[['arrival_airport', 'arrival_timezone', 'arrival_terminal']] = pd.json_normalize(df_raw['arrival'])[['airport', 'timezone', 'terminal']]
    data['airline_name'] = pd.json_normalize(df_raw['airline'])['name']
    data['flight_number'] = pd.json_normalize(df_raw['flight'])['number']
    data = data.to_dict()
    
    return(data)
    

def replace_string(data):
    """Replace slash for hifen"""
    df_data = pd.DataFrame.from_dict(data)

    df_data['departure_timezone'] = df_data['departure_timezone'].str.replace('/','-')
    df_data['arrival_terminal'] = df_data['arrival_terminal'].str.replace('/','-')
    

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

    get_json_data = PythonOperator(
        task_id='read_json',
        python_callable=read_json,
        dag=dag
    )
    create_dataframe = PythonOperator(
        task_id='create_flights_data',
        python_callable=create_flights_data,
        op_kwargs={"data_dict": "{{ti.xcom_pull('read_json')}}"},
        dag=dag
    )
    string_replacing = PythonOperator(
        task_id='replace_string',
        python_callable=replace_string,
        op_kwargs={"data": "{{ti.xcom_pull('create_flights_data')}}"},
        dag=dag
    )

(
    get_json_data >> create_dataframe
    >> string_replacing
)
