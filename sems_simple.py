import requests
import json
import paho.mqtt.client as mqtt


#tariff electricity
tariff = 0.19

#mqtt connection details
mqtt_ip = '192.168.xx.xx'
mqtt_port = 1883

#Goodwe / SEMS account and powerStationId 
account = '??????'
pwd = '?????'
powerStationId ='xxxxxxx-xxxx-xxx-xxx-xxxxxxx'

client = mqtt.Client()
client.connect(mqtt_ip,mqtt_port,60)

loginPayload = { 'account': account, 'pwd': pwd }
token = '{"version":"v2.0.4","client":"ios","language":"en"}'
global_url = 'https://globalapi.sems.com.cn/api/'
headers = { 'User-Agent': 'JanJansen47', 'Token': token }  #update token
try:
       c = requests.post(global_url + 'v1/Common/CrossLogin', headers=headers, data=loginPayload, timeout=30)
       c.raise_for_status()
except requests.exceptions.RequestException as e:    
       print("Exception_1:  ")
       print(e)       
print(c) 
data = c.json()
token = json.dumps(data['data'])
payload = { 'powerStationId' : powerStationId }
headers = { 'User-Agent': 'JanJansen47', 'token': token }  #update token
try:    
       r = requests.post(global_url + 'v1/PowerStation/GetMonitorDetailByPowerstationId', headers=headers, data=payload, timeout=10)
       r.raise_for_status()
except requests.exceptions.RequestException as e:    
       print("Exception_2:  ")
       print(e)
dat = r.json()
if dat['msg'] =='success' :
    print("success")
    #print(" data:  ")   #overview all data
    d2 =dat['data']
    #print(d2)
    d3= d2['inverter']
    d4=d3[0]
    #print(d4)           #overview important data
    
    #mqtt communication based upon json.
    x = {
    "name": "zon",
    "Eday":   (d4['eday'])*tariff,
    "Pnow":   d4['output_power'],
    "Etotal": (round(d4['etotal']))*tariff
    }
    y= json.dumps(x)
    try:
        client.connect(mqtt_ip,mqtt_port,60) 
        r.raise_for_status()
    except requests.exceptions.RequestException as e:    
       print("Exception_3:  ")
       print(e)
    try:
        client.publish("zon",y ,qos=0)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:    
        print("Exception_4:  ")
        print(e)
        client.disconnect();
        r.raise_for_status()
    except requests.exceptions.RequestException as e:    
        print("Exception_5:  ")
        print(e)





