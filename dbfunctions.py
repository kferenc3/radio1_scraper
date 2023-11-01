import sqlalchemy
import os


def insert_record(tbl,rec,eng,met):
    table = sqlalchemy.Table(tbl,met,autoload=True,autoload_with=eng,schema='dwh')
    col = tbl+'_name'
    stmt = sqlalchemy.insert(table).values({col:rec})
    with eng.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
    return print(rec+' has been inserted in table '+tbl)

def db_connect():
    usr=os.environ.get('DB_USER')
    pwd=os.environ.get('DB_PWD')
    engine=sqlalchemy.create_engine('postgresql://'+usr+':'+pwd+'@localhost:5432/postgres', future=True)
    metadata=sqlalchemy.MetaData(bind=engine)
    return engine, metadata