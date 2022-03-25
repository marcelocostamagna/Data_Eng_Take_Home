CREATE USER fligoo WITH PASSWORD 'fligoo';
CREATE DATABASE testfligoo owner fligoo;
GRANT ALL PRIVILEGES ON DATABASE "testfligoo" to fligoo;
\connect testfligoo;
CREATE TABLE IF NOT EXISTS testdata (flight_date VARCHAR (50), flight_status VARCHAR (50), departure_airport VARCHAR (50), departure_timezone VARCHAR (50), arrival_airport VARCHAR (50), arrival_timezone VARCHAR (50), arrival_terminal VARCHAR (50), airline_name VARCHAR (50), flight_number VARCHAR (50) );
