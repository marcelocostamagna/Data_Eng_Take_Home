CREATE USER fligoo WITH PASSWORD 'fligoo';
CREATE DATABASE testfligoo owner fligoo;
GRANT ALL PRIVILEGES ON DATABASE "testfligoo" to fligoo;
\connect testfligoo;
CREATE TABLE IF NOT EXISTS testdata (flight_date VARCHAR (200), flight_status VARCHAR (200), departure_airport VARCHAR (200), departure_timezone VARCHAR (200), arrival_airport VARCHAR (200), arrival_timezone VARCHAR (200), arrival_terminal VARCHAR (200), airline_name VARCHAR (200), flight_number VARCHAR (200) );
