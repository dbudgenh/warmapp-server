import json
import time
import hashlib
import hmac
import base64
import uuid
import requests  # Import the requests library
from database import MongoDB

API_URL = "https://warmapp-server.onrender.com"

def get_api_header(token = 'b0d308b991cfd23731963bb2bbac42a330ec01adfdbe4229fc40e25432fa289b369679849b3dad1c05e64166e1943fb2',secret = 'ae14fd6cd1d6f7630857c8cea2faec27'):
    # Declare empty header dictionary
    apiHeader = {}
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = f'{token}{t}{nonce}'
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    # Build api header JSON
    apiHeader['Authorization'] = token
    apiHeader['Content-Type'] = 'application/json'
    apiHeader['charset'] = 'utf8'
    apiHeader['t'] = str(t)
    apiHeader['sign'] = str(sign, 'utf-8')
    apiHeader['nonce'] = str(nonce)
    return apiHeader

def setup():
    apiHeader = get_api_header()
    url = 'https://api.switch-bot.com/v1.1/webhook/setupWebhook'
    data = {
        "action":"setupWebhook",
        "url":API_URL,
        "deviceList":"ALL"
    }
    response = requests.post(url=url,headers=apiHeader,data=json.dumps(data))

    # Check the response status
    if response.status_code == 200:
        print("POST request successful!")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)

def query():
    apiHeader = get_api_header()
    url = 'https://api.switch-bot.com/v1.1/webhook/queryWebhook'
    data = {
        "action":"queryUrl",
    }
    response = requests.post(url=url,headers=apiHeader,data=json.dumps(data))

    # Check the response status
    if response.status_code == 200:
        print("POST request successful!")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)

def update():
    apiHeader = get_api_header()
    url = 'https://api.switch-bot.com/v1.1/webhook/updateWebhook'
    data = {
        "action":"updateWebhook",
        "config":{
            "url":API_URL,
            "enable":True
        }
    }
    response = requests.post(url=url,headers=apiHeader,data=json.dumps(data))

    # Check the response status
    if response.status_code == 200:
        print("POST request successful!")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)

def get_device_status(id: str):
    url = f'https://api.switch-bot.com/v1.1/devices/{device_id}/status'
    api_header = get_api_header()
    response = requests.get(url, headers=api_header)
    if response.status_code == 200:
        # Successful request
        data = response.json()
        status_code = data['statusCode']
        message = data['message']
        if int(status_code) == 100:
            battery = data['body']['battery']
            temperature = data['body']['temperature']
            humidity = data['body']['humidity']
            print(data)
            #print(f'Name:{device_name}\nId:{device_id}\nType:{device_type}\nBattery:{battery}\nTemperature:{temperature}\nHumdidity:{humidity}')
            print('---------------------------')
        else:
            print('Error:',message)
    else:
        print('Error:', response.status_code, response.text)

def main():
    apiHeader = get_api_header()
    url = 'https://api.switch-bot.com/v1.1/devices'
    response = requests.get(url, headers=apiHeader)
    result = {}
    # Check the response
    if response.status_code == 200:
        # Successful request
        data = response.json()
        status_code = data['statusCode']
        message = data['message']
        print(data)
        if int(status_code) == 100:
            devices = data['body']['deviceList']
            for device in devices:
                device_id = device['deviceId']
                device_name = device['deviceName']
                device_type = device['deviceType']
                hub_device_id = device['hubDeviceId']

                if "hub" in device_type.lower():
                    print("Skipping data from hub")
                    continue
                result[device_id] = device_name
            return result
        else:
            print('Error:',message)
    else:
        print('Error:', response.status_code, response.text)


if __name__ == '__main__':
    update()