CREATE USER fligoo WITH PASSWORD 'fligoo';
CREATE DATABASE testfligoo owner fligoo;
GRANT ALL PRIVILEGES ON DATABASE "testfligoo" to fligoo;
\connect testfligoo;
CREATE TABLE IF NOT EXISTS testdata (flight_date VARCHAR (50) NOT NULL, flight_status VARCHAR (50) NOT NULL);
