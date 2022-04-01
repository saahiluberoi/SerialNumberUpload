from os import environ
import numpy as np
from flask_pymongo import MongoClient
from app import app

# General Config
SECRET_KEY = environ.get('legacy-apps123')
FLASK_ENV = environ.get('development')

app.config['UPLOAD_EXTENSIONS'] = ['.xls', '.xlsx', 'csv']
app.config['UPLOAD_FOLDER'] = 'uploads'

my_client = MongoClient("mongodb://root:example@192.168.117.130:27017/")
mydb = my_client["admin"]
my_col = mydb["upload_sn_data"]
series_data = mydb["series_data"]


# Helper Functions
def convert(val1):
    if val1 == np.NaN:
        return 0
    else:
        return val1
