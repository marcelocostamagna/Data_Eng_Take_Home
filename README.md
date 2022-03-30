Data Engineering Take Home
==============================

Real-time Flight Status
The AviationStack API was built to provide a simple way of accessing global aviation data for real-time and historical flights as well as allow customers to tap into an extensive data set of airline routes and other up-to-date aviation-related information. Requests to the REST API are made using a straightforward HTTP GET URL structure and responses are provided in lightweight JSON format. The objective of this project is to construct an ETL for a client in order to query information from the API, clean it, and store the results into a consumable database.

**Take-Home Goals**

Navigate to https://aviationstack.com/ and create a key for the API and read the documentation to understand how it works. For this exercise, consider only flight_status = active and limit = 100. We are not interested in acquiring the entire information, just focus on:
- Flight date
- Flight status
- Departure
     - Airport
     - Timezone
- Arrival
     - Airport
     - Timezone
     - Terminal
- Airline
     - Name
- Flight
     - Number

Build a docker with the services you think are necessary. The database and the table have to be created when running docker.
Database: testfligoo
Table: testdata
Create a process in Airflow that allows obtaining the information from the API.
Replace the "/" of the arrivalTerminal and departureTimezone fields for " - ". E.g: "Asia/Shanghai" to "Asia - Shanghai"
Insert the information in the database.
Create a Jupyter notebook to consume the information stored in the database.
Show the information in a Pandas dataframe
Requirements

Python 3.x & Pandas 1.x
Paying attention to the details and narrative is far way more important than extensive development.
Once you complete the assessment, share the Git repository link.
Have a final meeting with the team to discuss the work done in this notebook and answer the questions that could arise.
Finally, but most important: Have fun!
Nice to have aspects

Environment isolation.
Code versioning with Git (you are free to publish it on your own Github/Bitbucket account!).
Show proficiency in Python: By showing good practices in the structure and documentation, usage of several programming paradigms (e.g. imperative, OOP, functional), etc.

## How to run the solution


 1. Run compose:

 ```shell
    docker-compose up --build
 ```

 2. Navigate to airflow and run the DAG **flights_data_read**: 

 ```shell
    http://localhost:8080/
 ```

 3. Navigate to jupyter to check results:  

 ```shell
    http://localhost:8888/
 ```

 4. Run the below notebook to retrieve data from postgres:

 ```shell
    /home/docker_worker/work/read_data_from_postgres.ipynb
 ```

 5. Stop all the containers

 ```shell
    docker compose down 
 ```
 
 6. Clean up the environment
 
 ```shell
    docker-compose down --volumes --remove-orphans
 ```

 Base docker-compose yaml file was taken from [airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).


## How to test a specific task in a DAG

 1. Find the container id where Airflow worker is running and connect to it:
 
 ```shell
 docker ps
 docker exec -it <worker_container_id> bash 
 ```
2. Run the below command specifying DAG id, task id and a date before today

```shell
airflow tasks test <dag_id> <task_id>  2021-01-01
 ```
