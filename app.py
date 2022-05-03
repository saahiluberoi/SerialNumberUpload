import json

import pandas as pd
import requests
from flask import Flask, request, render_template
from flask_crontab import Crontab

import user
import m3

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
            try:
                # Read File
                df = pd.read_excel(file)
                # Convert to JSON
                data = df.to_json(orient='records')
                # Convert to list
                _val = json.loads(data)
                # check radio button value
                if request.form['radio'] == 'Storage Heaters':
                    store_series_data(df)
                else:
                    m3_operation(_val)
                # Call M3 API
                return m3_operation(_val)
            except Exception as e:
                print(e)
                return ValueError('File Invalid')
    return render_template('result.html', name='upload')


def m3_operation(_val):
    try:
        # Empty Table before inserting
        # user.my_col.delete_many({})
        all_data = []
        data_list = []
        for val in _val:
            # Get Manufacturing Dates
            _year = '20' + str(val['MANUFACTURING DATE'])[0:2]
            _full_date = '20' + str(val['MANUFACTURING DATE'])

            # Get Serial Numbers
            _serial = str(val['SERIAL NO.'])[5:]
            _itno = val['DUX CODE']

            # M3 API Call
            params = {'ITNO': val['DUX CODE'], 'CONO': '100', 'LNCD': 'EN'}
            response = m3.get_ITDS_from_M3(params)
            data_list = m3.data_to_m3(response, _year, _itno, _serial)
            # Set values for MongoDB
            # data_list = {
            #     "CUOW": 9900,
            #     "CONO": 100,
            #     "DIVI": 'H01',
            #     "ITDS": response,
            #     "LNCD": 'EN',
            #     "ITNO": _itno,
            #     "SERI": _serial,
            #     "INNO": _serial,
            #     "CUPL": 9900,
            #     "INGR": 'TEMPLATE',
            #     "CFE6": _full_date,
            #     "MLYR": _year,
            #     "DEDA": val['MANUFACTURING DATE']
            # }
            # Insert to MongoDb
            # user.my_col.insert_one(data_list)
            all_data.append(data_list)
            return m3.send_data(data_list)

    # Catch all exceptions
    except Exception as e:
        print(e)
        return ValueError('File Invalid')


# Series Functionality
def store_series_data(df):
    try:
        # Empty Table before inserting
        user.series_data.delete_many({})
        # Clean Data
        data = pd.read_excel(df, sheet_name="sheet2", skiprows=[0], converters={" ": user.convert(df)}, dtype={" ": str}, usecols=["Model No.", "QTY", "Starting SN", "Production Date"])
        # Empty DataFrame
        new_df = pd.DataFrame(columns=["Model No.", "QTY", "Serial Number", "Production Date"])
        n = 0
        # Start Series and load into the empty dataframe
        for index, row in data.iterrows():
            for qty in range(row["QTY"]):
                new_serial = row["Starting SN"] + qty
                df = pd.DataFrame({"Model No.": row["Model No."], "Serial Number": new_serial, "Production Date": row["Production Date"]}, index=[0])
                new_df.loc[n] = df.loc[0]
                n += 1
        # Convert to JSON
        json_data = new_df.to_json(orient="records")
        values = json.loads(json_data)

        for val in values:
            _year = val["Production Date"]
            _itno = val['Model No.']
            # M3 API Call
            params = {'ITNO': _itno, 'CONO': '100', 'LNCD': 'GB'}
            response = m3.get_ITDS_from_M3(params)
            # Set Values for MongoDB
        # return m3.pass_data_to_MongoDB(response, val, _year, _itno)
            data_list = {
                "CUOW": 9900,
                "CONO": 100,
                "DIVI": 'H01',
                "ITDS": response,
                "LNCD": 'EN',
                "ITNO": _itno,
                "SERI": val['Serial Number'],
                "INNO": val['Serial Number'],
                "CUPL": 9900,
                "INGR": 'TEMPLATE',
                "CFE6": val['Production Date'],
                "MLYR": _year,
                "DEDA": val['Production Date'],
            }
            # insert to mongoDB
            user.series_data.insert_one(data_list)
        pass
    except Exception as e:
        print(e)
        return ValueError('File Invalid')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    app.env = 'development'

