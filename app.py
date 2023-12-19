import time
import uuid
import random
import datetime
import json
import threading
import psycopg2 as pg

from sqlalchemy import create_engine, text
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


ddl = ""
with open("setup.sql", "r") as file:
    ddl = file.read()

credentials = "user=postgres password=postgres host=localhost dbname=example"

def setup():
    conn = pg.connect(credentials)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

    with conn.cursor() as tx:
        tx.execute(ddl)
        tx.execute('truncate outbox;')

    conn.close()

def step1(delay):
    try:
        conn = pg.connect(credentials)
        cursor = conn.cursor()
        cursor.execute("insert into outbox (event_id, event_type, event_data, inserted_at) values('aaa', 'aaa', '{\"blah\": \"aaa\"}', CURRENT_TIMESTAMP);")
        time.sleep(delay)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def step2(delay):
    try:
        conn = pg.connect(credentials)
        cursor = conn.cursor()
        cursor.execute("insert into outbox (event_id, event_type, event_data, inserted_at) values('bbb', 'bbb', '{\"blah\": \"bbb\"}', CURRENT_TIMESTAMP);")
        time.sleep(delay)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def read(delay):
    time.sleep(delay)

    with pg.connect(credentials) as conn:
        with conn.cursor() as tx:
            print("   id   |   tx_id   |   data ")
            print("--------+-----------+--------")
            tx.execute("select sequence, xmin, event_data from outbox order by sequence;");
            for (id, xmin, data) in tx.fetchall():
                print(f" {id}     |     {xmin}   |   {data['blah']}")
            print("\n")

setup()

threads = [
    threading.Thread(target = step2, args = [0.2]),
    threading.Thread(target = read,  args = [0.3]),
    threading.Thread(target = step1, args = [0.4]),
    threading.Thread(target = read,  args = [0.5])
]

for t in threads:
    t.start();

for t in threads:
    t.join();
