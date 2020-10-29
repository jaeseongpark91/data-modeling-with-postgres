## Proejct: Data Modeling with Postgres

### Sparkify
A music streaming startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. 

In this project I will create a Postgres database with tables designed to optimize queries on song play analysis and build ETL pipeline.

Ultimately, the final byproduct of this project are one fact table ('songplays') and four dimension tables ('songs', 'artists' 'users', 'times'). By utilizing four dimension tables, I can reduce duplicated information from the fact table. 

### Dataset
1. Song dataset
: The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.
> song_data/A/B/C/TRABCEI128F424C983.json
> song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

    {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
    
    
2. Log dataset
: The second dataset consists of log files in JSON format. These activity logs from a music streaming app based on specified configurations. The log files in the dataset are partitioned by year and month.
> log_data/2018/11/2018-11-12-events.json
> log_data/2018/11/2018-11-13-events.json

And here is an example of what the data in a log file looks like.
![log-data]("log-data.png")

### Database Schema
Here is the database ![schema diagram]("schema_diagram.png") and brief explanation of each tables.
- (fact) 'songplays' : records in log data associated with song plays i.e. records with page NextSong (*songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*)
- (dim) 'artists' : artist in the music database (*artist_id, name, location, latitude, longitude*)
- (dim) 'songs' : song in the music database (*song_id, title, artist_id, year, duration*)
- (dim) 'users' : users in the app (*user_id, first_name, last_name, gender, level*)
- (dim) 'times' : timestamps of records in songplays broken down into specific units (*songplay_id, hour, day, week, month, year, weekday*)

### Procedures
First of all by extracting 'song' data, I built two dimension tables ('songs' and 'artists') and from 'log' data I created another two dimension tables ('users', 'times'). Then by consolidating two datasets I built 'songplays' fact table. 

One tricky issue was that since the log file does not specify an ID for either the song or the artist. I solved this issue by geting the song ID and artist ID by querying the songs and artists tables to find matches based on song title, artist name, and song duration time.

### File description
The project consists of five files.

- sql_queries.py : Script regarding all the queries (e.g. creating tables, inserting data) 
- create_tables.py : Connecting the database and creating tables using 'sql_queries.py'
- etl.py : Main script extracting the JSON data from 'data' folder and transforming the data into tables created in 'create_tables.py' (fact table: 'songplays'/ dim talbe: 'users', 'times', 'songs', 'artists')  
- etl.ipynb : Guideline helping to create 'etl.py' provided by Udacity
- test.ipynb : Script to check if tables are created in a intended way

### How to run the code
1. Run 'create_tables.py' in the terminal
2. Run 'etl.py' in the terminal
3. Run 'test.ipynb' in the jupyter notebook to check the tables and inserted data. 

### Install
This project requires Python3 and PostgreSQL.
