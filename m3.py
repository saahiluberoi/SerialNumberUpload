import json
import requests

# M3 connection
url = 'https://duxtest-bel1.cloud.infor.com:63922/m3api-rest/execute/'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


# Get Item Description from M3
def get_ITDS_from_M3(params):
    api = 'MMS200MI/'
    transaction = 'GetItmBasic/'
    response = requests.get(url + api + transaction, params=params, headers=headers,
                            auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
    _ITDS_list = json.loads(response.text)
    for key in _ITDS_list['MIRecord']:
        for key_2 in key['NameValue']:
            if key_2['Name'] == 'ITDS':
                ITDS = key_2['Value']
    return ITDS


# Form data to send to M3
def data_to_m3(response, _year, _itno, _serial):
    data_list = {
        "CUOW": 9900,
        "CONO": 100,
        "DIVI": 'H01',
        "ITDS": response,
        "LNCD": 'EN',
        "ITNO": _itno,
        "SERI": _serial,
        "INNO": _serial,
        "CUPL": 9900,
        "INGR": 'TEMPLATE',
        "CFE6": _year,
        "MLYR": _year,
        "DEDA": _year,
    }

    return data_list


# Send to M3
def send_data(data_list):
    _api = 'SOS100MI/'
    _transaction = 'AddIndItem/'
    try:
        # print('Sending data to M3')
        print(data_list)
        response = requests.get(url + _api + _transaction, params=data_list, headers=headers,
                                 auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
        return response.text[response.text.find('<Message>') + 8:response.text.find('</Message>')]

    except Exception as e:
        print(e)
        message = response.text[response.text.find('<Message>') + 9:response.text.find('</Message>')]
        return message
