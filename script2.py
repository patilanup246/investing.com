"""

    Created on Thu May 02 16:28:14 2019

    @author: keyur-r

    Description: Edit the raw csv and save edited csv into ./data/edits/

    Run :
    python script2.py

"""

import pandas as pd
import os
import glob
import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
READ_PATH = os.path.join(ROOT_PATH, 'data')
WRITE_PATH = os.path.join(ROOT_PATH, 'data/edits')
CSV_FILES = glob.glob(READ_PATH+"/*.csv")
COL = ['Date','Open','High','Low']



def format_date(date_text):
    try:
        date_obj = datetime.datetime.strptime(date_text, '%b %d, %Y')
        formatted_date = '{:02d}'.format(date_obj.year) + '{:02d}'.format(date_obj.month) + '{:02d}'.format(date_obj.day)
        return formatted_date
    except ValueError:
        raise ValueError("Incorrect data format, should be May 10, 2018 {}".format(date_text))

def format_price(price):
    if isinstance(price, str):
        price = price.replace('"', '')
        price = price.replace(',', '')
    return price

if __name__ == '__main__':
    if not os.path.exists(READ_PATH):
        print ("Source csv files are not available.")
        exit()

    if not os.path.exists(WRITE_PATH):
        os.makedirs(WRITE_PATH)

    for file in CSV_FILES:
        df = pd.read_csv(file)
        df['Date'] = df['Date'].apply(format_date)
        df['Open'] = df['Open'].apply(format_price)
        df['High'] = df['High'].apply(format_price)
        df['Low'] = df['Low'].apply(format_price)
        new_df = df[COL]
        new_df = new_df.sort_values('Date')
        new_csv_file = os.path.join(WRITE_PATH, file.split('/')[-1])
        new_df.to_csv(new_csv_file, index=False)