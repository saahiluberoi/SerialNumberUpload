import json
import requests

# M3 connection
url = 'https://duxtest-bel1.cloud.infor.com:63922/m3api-rest/execute/'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
# Get item description from M3
api = 'MMS200MI/'
transaction = 'GetItmBasic/'


# Get Item Description from M3
def get_ITDS_from_M3(params):
    response = requests.get(url + api + transaction, params=params, headers=headers,
                            auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
    _ITDS_list = json.loads(response.text)
    for key in _ITDS_list['MIRecord']:
        for key_2 in key['NameValue']:
            if key_2['Name'] == 'ITDS':
                ITDS = key_2['Value']
    return ITDS


# Send to M3
def send_data(data_list):
    _api = 'SOS100MI/'
    _transaction = 'AddIndItem/'
    try:
        response = requests.post(url + _api + _transaction, params=data_list, headers=headers,
                                 auth=('INFORBC\#DUXFEA', 'L3t5F1x$TufF12345'))
        return response.text[response.text.find('<Message>') + 8:response.text.find('</Message>')]

    except Exception as e:
        print(e)
        message = response.text[response.text.find('<Message>') + 9:response.text.find('</Message>')]
        return message
