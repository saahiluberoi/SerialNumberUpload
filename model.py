import json

import pyodbc
import config as cfg
import m3
import numpy as np
import pandas as pd


# Continuous Serial Number Data
def continuous_data(df):
    # Convert to JSON
    data = df.to_json(orient='records')
    # Convert to list
    _val = json.loads(data)
    # Create a list of serial numbers
    data_list = []
    for val in _val:
        # Set Parameters for M3 API Call
        params = {'ITNO': val['DUX CODE'], 'CONO': '100', 'LNCD': 'EN'}
        # Get Item Description
        ITDS = m3.get_ITDS_from_M3(params)
        # Set Data in M3 Format
        data_list = m3.API_call.data_to_m3(ITDS, val)
        # Send Data to M3
        m3.send_data(data_list)


# Helper Functions
def convert(val1):
    if val1 == np.NaN:
        return 0
    else:
        return val1


# Establish Connection to DB
def connection():
    conn = pyodbc.connect(cfg.connection_string)
    return conn


# Series Functionality
def store_series_data(df):
    try:
        all_data = []
        data_list = []
        # Empty Table before inserting
        # user.series_data.delete_many({})
        # Clean Data
        data = pd.read_excel(df, sheet_name="sheet2", skiprows=[0], converters={" ": convert()}, dtype={" ": str}, usecols=["Model No.", "QTY", "Starting SN", "Production Date"])
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
            _serial = val['Serial Number']
            # M3 API Call
            params = {'ITNO': _itno, 'CONO': '100', 'LNCD': 'GB'}
            response = m3.get_ITDS_from_M3(params)
            # Set Values for MongoDB
        # return m3.pass_data_to_MongoDB(response, val, _year, _itno)
            data_list = m3.data_to_m3(response, val) # _year, _itno, _serial

            # insert to mongoDB
            # user.series_data.insert_one(data_list)
            all_data.append(data_list)
            # m3.send_data(data_list)
    except Exception as e:
        print(e)
        return ValueError('File Invalid')
