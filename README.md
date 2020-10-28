## Proejct: Data Modeling with Postgres

### Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. My role is to create a database schema and ETL pipeline for this analysis.

### Procedures
The purpose of this project is to create a database schema and ETL pipeline.

### Database Schema
Here is the database ![schema diagram]("schema_diagram.png")

### File description
The project consists of five files.

- sql_queries.py : Script regarding all the queries (e.g. creating tables, inserting data) 
- create_tables.py : Connecting the database and creating tables using 'sql_queries.py'
- etl.py : Main script extracting the JSON data from 'data' folder and transforming the data into tables created in 'create_tables.py' (fact table: 'songplays'/ dim talbe: 'users', 'times', 'songs', 'artists')  
- etl.ipynb : Guideline helping to create 'etl.py' provided by Udacity
- test.ipynb : Script to check if tables are created in a intended way

 ### Install
This project requires Python3 and PostgreSQL.
