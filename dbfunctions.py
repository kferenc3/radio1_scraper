import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import exc
from datetime import datetime
from datetime import timedelta
import os
import pytz

def db_connect():
    usr=os.environ.get('DB_USER')
    pwd=os.environ.get('DB_PWD')
    engine=sqlalchemy.create_engine('postgresql://'+usr+':'+pwd+'@localhost:5432/postgres', future=True)
    metadata=sqlalchemy.MetaData()
    return engine, metadata

def ins_upd_record(tbl,rec: dict,eng,met, mode='i', keycol=None):
    table = sqlalchemy.Table(tbl,met,autoload_with=eng,schema='public')
    if mode == 'u':
        stmt = sqlalchemy.update(table).where(table.c[keycol]==rec[keycol]).values(rec)
    else:
        stmt = sqlalchemy.insert(table).values(rec)
    with eng.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
    if mode == 'u':
        return '1 update in ' + tbl
    else:
        return '1 insert into '+ tbl


def check_record(tbl,row: dict, col,rec,eng,metadat):
    table = sqlalchemy.Table(tbl,metadat,autoload_with=eng, schema='public')
    lst=[]
    local = pytz.timezone('Europe/Budapest')
    with Session(eng) as session:
        for i in session.query(table).where(table.c[col]==rec):
            lst.append(i)
    
    for i in lst:
        t_diff = abs((i[0].astimezone(pytz.utc)+timedelta(hours=1))-datetime.strptime(row['tstamp'],'%Y-%m-%d %H:%M:%S %z'))
        if timedelta(hours=0,minutes=0,seconds=0) == t_diff:
            raise exc.IntegrityError('insert','row','here')
        elif timedelta(minutes=5)> t_diff:
            return'drop'
        else:
            pass                                    
    return'keep'

#engine, metadata = db_connect()
#check_record('playlist', 'title', 'Paradise', engine, metadata)

#d = {'tstamp': '2023-11-03 11:45:34 +0000', 'length': 193521, 'artist': ['Sophie and the Giants ', ' Purple Disco Machine'], 'title': 'Paradise', 'updated_dt': '2023-11-03 14:28:17 +0000'}

#print(check_record('playlist', d, 'title',d['title'], engine, metadata))
