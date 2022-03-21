# Database Connection
from os import environ

from flask_crontab import Crontab
from flask_pymongo import MongoClient

from app import app

my_client = MongoClient("mongodb://root:example@192.168.117.129:27017/")
mydb = my_client["admin"]
my_col = mydb["upload_sn_data"]

# M3 connection
url = 'https://duxtest-bel1.cloud.infor.com:63922/m3api-rest/execute/'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# General Config
SECRET_KEY = environ.get('legacy-apps123')
FLASK_ENV = environ.get('development')

app.config['UPLOAD_EXTENSIONS'] = ['.xls', '.xlsx', 'csv']
app.config['UPLOAD_FOLDER'] = 'uploads'