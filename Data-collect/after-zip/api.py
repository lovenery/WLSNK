import requests
requests.packages.urllib3.disable_warnings()

username='student'
password='lora_experiment'

def getToken() :
    payload = {"username": username, "password": password}
    url = 'https://140.115.52.100:8080/api/internal/login'
    headers = { "Accept" : "application/json"}
    r = requests.post(url, json = payload, verify = False)
    return r.json()['jwt']

def getFrame(eui, jwt) :
    payload = {'limit' : '2', 'offset' : '0'}
    header = {'Grpc-Metadata-Authorization' : jwt }
    url = 'https://140.115.52.100:8080/api/devices/{}/frames'.format(eui)
    r = requests.get(url, params = payload, headers = header, verify = False)
    return r.json()['result']

