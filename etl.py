import os
import glob
import psycopg2
import pandas as pd
import json
from sql_queries import *


def process_song_file(cur, all_files):
    """
DESCRIPTION: This function consists of two parts. First, it reads the data in 'data/song_data' and create a dataframe consolidating the data in 'data/song_data' directory. Secondly, it inserts data into songs and artists dim table.
    
ARGUMENTS:
cur: the curosr object
filepath: song data file path.
    
RETURNS:
    None 
    """
    # open song file
    df_song = pd.DataFrame()
    for filepath in all_files:
        with open(filepath) as f:
            data = json.load(f)
        df = pd.DataFrame([data])
        df_song = pd.concat([df, df_song])

    # insert song record
    song_data = df_song.loc[:,['song_id', 'title', 'artist_id', 'year', 'duration']]
    for i, row in song_data.iterrows():
        cur.execute(song_table_insert, row)
    
    # insert artist record
    artist_data = df_song.loc[:,['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    for i, row in artist_data.iterrows():
        cur.execute(artist_table_insert, row)


def process_log_file(cur, all_files):
    """
DESCRIPTION: This function consists of two parts. First, it reads the data in 'data/log_data' and create a dataframe consolidating the data in 'data/log_data' directory. Secondly, it inserts data into times, users, and songplays table.
    
ARGUMENTS:
    cur: the curosr object
    filepath: log data file path.
    
RETURNS:
    None 
    """
    # open log file
    log_data = []
    for filepath in all_files:
        for line in open(filepath, 'r'):
            log_data.append(json.loads(line))
    df_log = pd.DataFrame(log_data)

    # convert timestamp column to datetime
    from datetime import datetime
    df_log['ts'] = df_log['ts'] / 1000
    df_log['dt'] = df_log['ts'].apply(datetime.fromtimestamp)
    
    # insert time data records
    def datetime_extract(dt):
        hr = dt.hour
        day = dt.day
        week_year = dt.strftime("%V")
        month = dt.month
        yr = dt.year
        weekday = dt.dayofweek
        list_data = [hr, day, week_year, month, yr, weekday]
        return list_data

    df_log['extracted'] = df_log['dt'].apply(datetime_extract)
    df_log = df_log[df_log['page']=='NextSong']
    
    time_data = df_log['extracted'].tolist()
    column_labels = ['hour', 'day', 'week_of_the_year', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df_log.loc[:,["userId", "firstName", "lastName", "gender", "level"]]
    user_df = user_df.dropna()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df_log.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        songplay_data_after = [i for i in songplay_data if str(i) != '']
        if songplay_data != songplay_data_after:
            continue
        else:
            cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
DESCRIPTION: This function creates a list of absolute directories of the data in the designated filepath and proceed the function(either 'process_song_file' or 'process_log_file'). 
    
ARGUMENTS:
    cur: the curosr object
    conn: the connection object
    filepath: data file path
    func: process function type (either 'process_song_file' or 'process_log_file')
    
RETURNS:
    None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    
    func(cur, all_files)


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
