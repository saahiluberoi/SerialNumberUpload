from os import environ
import numpy as np
from flask_pymongo import MongoClient


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

