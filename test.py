import numpy as np
import pyodbc
import requests

import app
import config as db


def convert(val1):
    if val1 == np.NaN:
        return 0
    else:
        return val1


params = {'CONO': 100,
          'FACF': 'H01',
          'FACT': 'H01',
          'STSF': 20,
          'STST': 80}

headers = 'application/json'


def test_mo_download():
    response = requests.get('https://duxprod-bel1.cloud.infor.com:63922/m3api-rest/execute/' + 'PMS100MI/' + 'Select/',
                            params=params, headers=headers, auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
    if response:
        print(response.status_code)
        print(response.text)
        print(response.json())
        return response.json()
    # mo_data = response.json()
    # os.makedirs('excel sheets', exist_ok=True)
    # mo_data.to_csv('excel_sheets/mo_data.csv')
    # print(mo_data)
    pass


# Test to connect to DB
def test_db_connection():
    try:
        connection = app.connection()
        # connection = pyodbc.connect(db.connection_string)
        cursor = connection.cursor()
        m3_server = cursor.execute(
            "SELECT PARAMETERVALUE FROM " + db.DATABASE + ".[DBO].[CONFIGPARAMETERS] WHERE PARAMETERNAME = 'M3WEBSERVICEURL'").fetchone()
        print(m3_server)
        for row in m3_server:
            print(row)
        return True
    except Exception as e:
        print(e)
        return False
