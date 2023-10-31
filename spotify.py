import requests
import os
from datetime import datetime
from  datetime import timedelta

def auth(client_id, client_secret):
    endpoint = 'https://accounts.spotify.com/api/token'
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type':'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    r = requests.post(endpoint,headers=header,data=payload)
    expires_at = datetime.utcnow() + timedelta(seconds=int(r.json()['expires_in']))
    return r.json()['access_token'], expires_at

def search(track, artist, bearer):
    endpoint = 'https://api.spotify.com/v1/search'
    header = {'Authorization': 'Bearer ' + bearer}
    payload = {'q': 'track:'+track+' artist:'+'artist', 'type': 'track'}
    r = requests.get(endpoint, headers=header, params=payload)
    return r.json()
    


if __name__=='__main__':
    c_id = os.environ.get('CLIENT_ID')
    c_secret = os.environ.get('CLIENT_SECRET')
    expires_at = datetime.utcnow()
    if datetime.utcnow() > expires_at:
        print("need authentication")
        access_token, expires_at = auth(c_id,c_secret)
    else:
        print('all good')
    
    print(search('Belly Dancer', 'Imanbek', access_token))

