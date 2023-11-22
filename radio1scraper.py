import requests
from datetime import datetime
import dbfunctions
import pytz
from sqlalchemy import exc
import traceback

def radioscrape():
    url = 'https://radio1.hu/stream/stream.php'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    player = r.json()['player']
    artists = [x['artist'].split('/') for x in player] #in case there are multiple artists they are split into a sub-list
    titles = [x['title'] if x['title'] != '' else None for x in player]
    timestamps = [datetime.strptime(x['idopont'],'%Y-%m-%d %H:%M:%S') for x in player]
    local = pytz.timezone("Europe/Budapest")
    utc_tstamps = [local.localize(x).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S %z') for x in timestamps]
    length = [x['length'] if x['length'] != '' else None for x in player]
    rec = []
    exclude = ['WORLD IS MINE RADIO SHOW', '', 'DISCO\'S HIT', 'RADIO 1', 'RÁDIO 1 LIVE MIX', 'RÁDIÓ 1 LIVE MIX','RÁDIÓ 1 WEEKEND AFTER', 'RÁDIÓ 1 WEEKEND BEFORE']
    for i in range(len(utc_tstamps)):
        if artists[i][0] not in exclude:
            rec.append({
                'tstamp':utc_tstamps[i],
                'length':length[i],
                'artist':[x.strip() for x in artists[i]],
                'title':titles[i], 
                'updated_dt': local.localize(datetime.now()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S %z')})
        else:
            print("Not loading: ", artists[i],' - ', titles[i])

    return rec

def loader():
    records = radioscrape()
    engine, metadata = dbfunctions.db_connect()
    for r in records:
        try:
            
            if dbfunctions.check_record('playlist',r,'title',r['title'],engine,metadata) =='keep':
                print(dbfunctions.ins_upd_record('playlist',r,engine,metadata,'i'))
            else:
                print('Record was dropped due to being a potential duplicate:',r)
        except exc.IntegrityError:
            print(dbfunctions.ins_upd_record('playlist',r,engine,metadata,'u','tstamp'))

if __name__ == '__main__':
    try:
        print('Starting loader...')
        loader()
        print('Loader finished')
    except:
        print('error')
        traceback.print_exc()