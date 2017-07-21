import os
import csv
import psycopg2
import pandas as pd

def txt_to_csv(filename, csv_filename):
    txt_file = csv.reader(open(filename, "rb"),delimiter= '\t')
    out_csv = csv.writer(open(csv_filename, 'wb'))
    out_csv.writerows(txt_file)
    return

def get_txt_filenames(directory):
    filenames = os.listdir(directory)
    filenames = [filename for filename in filenames if is_txt(filename)]
    return filenames

def is_txt(filename):
    return filename.split('.')[-1] == "txt"
def change_filename_extension(filename):
    filename = filename.split('.')
    return filename[0] + ".csv"

def get_csv_filenames(filenames):
    return [change_filename_extension(filename) for filename in filenames if is_txt(filename)]

def remove_txt_files(filenames):
    os.system("cd ../data")
    for filename in filenames:
        command = "rm " + filename
        os.system(command)
    return


def get_data():
    conn = psycopg2.connect(database="nba_database", user="db_user", password="nba_database", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.excute("select * from shot_logs")
    data = cur.fetchall()

    data = pd.DataFrame(data,columns = ["pts_type","shot_dist","closest_def_dist","shot_res","closes_def","player"])
    return data
