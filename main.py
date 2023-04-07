import requests
from datetime import datetime
import time
import sys
import socket

args = list(sys.argv)[1:]

source = args[0]
noradID = int(args[1])
lat = float(args[2])
long = float(args[3])

print("Posting data: \n Source: "+source+"\n NORAD ID: "+str(noradID)+"\n Latitude: "+str(lat)+"\n Longitude: "+str(long)+"\n")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("FAILED TO CREATE SOCKET")

try:
    print("CONNECTING TO "+str("127.0.0.1")+":"+str("8100"))
    s.connect(('127.0.0.1', 8100))
    print("CONNECTED!")
except Exception as e:
    print("CANNOT CONNECT TO SOUNDMODEM. ABORTING...",e)
    #abort
    exit()

def send_sids(bcn):
    DB_TELEMETRY_ENDPOINT_URL= "https://db.satnogs.org/api/telemetry/"
    # SiDS parameters
    params = {
        'noradID': noradID,
        'source': str(source), 
        'timestamp': datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S.000Z'), 
        'locator': 'longLat', 
        'longitude': long, 
        'latitude': lat, 
        'frame': str(bcn), 
    }
    #print(DB_TELEMETRY_ENDPOINT_URL, params)
    postSuccess = False
    while(not postSuccess):
        try:
            response = requests.post(DB_TELEMETRY_ENDPOINT_URL, data=params, timeout=10)
            print(response)
            response.raise_for_status()
            postSuccess = True
            print("Posted frame to Satnogs!")
        except Exception as e:
            
            print('Could not post data to satnogs, retrying.', e)
            time.sleep(0.5)
    return


while True:
    reply = str(s.recv(4096).hex())
    reply = reply[4:len(reply)-2].replace("\n","").replace(" ","") #just in case
    if reply != "":
        #print(reply)
        send_sids(reply)
