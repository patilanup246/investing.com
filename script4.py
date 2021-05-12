"""

    Created on Thu May 02 17:02:27 2019

    @author: keyur-r

    Description: Adding name of .day files to charts.lst 

    Run :
    python script4.py

"""


import pandas as pd
import os
import glob
import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
READ_PATH = os.path.join(ROOT_PATH, 'data/edits')
DAY_FILES = glob.glob(READ_PATH+"/*.day")
LST_FILE = os.path.join(READ_PATH, 'charts.lst')

if __name__ == '__main__':
    if not os.path.exists(READ_PATH):
        print ("Source csv files are not available.")
        exit()

    with open(LST_FILE, 'a') as lst_file:
        for file in DAY_FILES:
            nameofdayfile = file.split('/')[-1]
            symbolofstock = nameofdayfile.split('.')[0]
            data = "7," + nameofdayfile + ",na,0,1,0," + symbolofstock + "," + symbolofstock + "\n"
            lst_file.write(data)