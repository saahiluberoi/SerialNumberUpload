import json
import requests
import config as cfg

""" 
This route will make the API calls to M3
"""


class API_call():

    # Receive Item Description from M3
    itds_api = 'MMS200MI/'
    itds_transaction = 'GetItmBasic/'

    # Send Data to M3
    send_api = 'SOS100MI/'
    send_transaction = 'AddIndItem/'

    """
    Function to set data in the correct format for M3
    """

    def data_to_m3(ITDS, val):
        _full_date = '20' + str(val['MANUFACTURING DATE'])
        _year = '20' + str(val['MANUFACTURING DATE'])[0:2]
        # s = str(val['SERIAL NUMBER']).replace(str, '')
        # print(s)
        _serial = str(val['SERIAL NO.'])[::-1][10::-1]
        print(_serial)
        _itno = val['DUX CODE']
        data_list = {
            "CUOW": 9900,
            "CONO": 100,
            "DIVI": 'H01',
            "ITDS": ITDS,
            "LNCD": 'EN',
            "ITNO": _itno,
            "SERI": _serial,
            "INNO": _serial,
            "CUPL": 9900,
            "INGR": 'TEMPLATE',
            "CFE6": _full_date,
            "MLYR": _year,
            "DEDA": _full_date,
        }
        return data_list


"""
Get Item Description Information from M3
"""


def get_ITDS_from_M3(params):
    response = requests.get(cfg.url + API_call.itds_api + API_call.itds_transaction, params=params, headers=cfg.headers,
                            auth=cfg.auth)
    _ITDS_list = json.loads(response.text)
    for key in _ITDS_list['MIRecord']:
        for key_2 in key['NameValue']:
            if key_2['Name'] == 'ITDS':
                ITDS = key_2['Value']
                break
        return ITDS


"""
This route will send data to M3
"""


def send_data(data_list):
    try:
        response = requests.get(cfg.url + API_call.send_api + API_call.send_transaction, params=data_list,
                                headers=cfg.headers,
                                auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
        return response.text[response.text.find('<Message>') + 8:response.text.find('</Message>')]

    except Exception as e:
        print(e)
        message = response.text[response.text.find('<Message>') + 9:response.text.find('</Message>')]
        return message
