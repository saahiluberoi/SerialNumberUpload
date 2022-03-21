import json
from datetime import datetime
import pandas as pd
import requests
from flask import Flask, request, render_template
from flask_crontab import Crontab

import user

app = Flask(__name__, template_folder='template')
crontab = Crontab(app)


# Render to Homepage
@app.route('/')
def homepage():
    return render_template('home.html', name='home')


# Render to Upload Page
@app.route('/process_file/', methods=['GET', 'POST'])
def process_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        if file:
            # Read the file
            df = pd.read_excel(file)

            # Convert to JSON
            _json_data = df.to_json(orient='records')
            _val = json.loads(_json_data)

            # check radio button value
            if request.form['radio'] == 'Storage Heaters':
                store_series_data(df, file)
            else:
                m3_operation(_val, file)
    return 'File Uploaded'
    # m3_operation(_val, file)


def store_series_data(df, file):
    try:
        start_list = []
        for value in df:
            n = df.apply(lambda row: row['QTY'] + 1, axis=1)
            a = value
            xn = a + (n - 1)
            while a <= xn:
                if a != xn:
                    start_list.append(a)
                a = a + 1

        list_string = [str(item) for item in start_list]
        date_time = datetime.today()
        for val in list_string:
            data_list = {
                "FileName": file.filename,
                "SerialNumbers": val,
                "Status": "Accepted",
                "TimeStamp": date_time
            }
        print("Passed")
        # send_data(data_list)
    except Exception as e:
        print(e)
        return ValueError('File Invalid')


def m3_operation(_val, file):
    # Get item description from M3
    _api = 'MMS200MI/'
    _transaction = 'GetItmBasic/'
    try:
        # Empty Table before inserting
        user.my_col.delete_many({})
        for value in _val:
            # Get Manufacturing Dates
            _year = '20' + str(value['MANUFACTURING DATE'])[0:2]
            _full_date = '20' + str(value['MANUFACTURING DATE'])
            _serial = str(value['SERIAL NO.'])[5:]
            params = {'ITNO': value['DUX CODE'], 'CONO': '100', 'LNCD': 'EN'}
            response = requests.get(user.url + _api + _transaction, params=params, headers=user.headers, auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
            _ITDS_list = json.loads(response.text)
            for key in _ITDS_list['MIRecord']:
                for key_2 in key['NameValue']:
                    if key_2['Name'] == 'ITDS':
                        _ITDS = key_2['Value']
                        # Set Values for MongoDB
                        data_list = {
                            "FILE_NAME": file.filename,
                            "CUOW": 9900,
                            "CONO": 100,
                            "DIVI": 'H01',
                            "ITDS": _ITDS,
                            "LNCD": 'EN',
                            "ITNO": value['DUX CODE'],
                            "SERI": _serial,
                            "INNO": _serial,
                            "CUPL": 9900,
                            "INGR": 'TEMPLATE',
                            "CFE6": _full_date,
                            "MLYR": _year,
                            "DEDA": value['MANUFACTURING DATE']
                        }
                # Insert to MongoDb
                user.my_col.insert_one(data_list)
        print(response.reason)

    # Catch all exceptions
    except Exception as e:
        print(e)
        return ValueError('File Invalid')


# Send to M3
# @crontab.job(minute='*/5')
def send_data(data_list):
    _api = 'SOS100MI/'
    _transaction = 'AddIndItem/'

    try:
        response = requests.get(user.url + _api + _transaction, params=data_list, headers=user.headers, auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
        return response.text[response.text.find('<Message>') + 8:response.text.find('</Message>')]

    except Exception as e:
        print(e)
        message = response.text[response.text.find('<Message>') + 9:response.text.find('</Message>')]
        return message


# @crontab.job(minute='*/5')
if __name__ == '__main__':
    app.run(debug=True)
