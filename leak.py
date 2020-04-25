import os
import psycopg2
from psycopg2.extras import NamedTupleCursor, register_composite, Json
import time
import tracemalloc

MAX_RETRIES = 6

def connect(uri):
    retry = 0
    while True:
        try:
            conn = psycopg2.connect(
                dsn=uri,
                dbname='postgres',
                cursor_factory=NamedTupleCursor
            )
            conn.set_client_encoding('UTF8')
            break
        except Exception as e:
            print(e)
            retry += 1
            if retry > MAX_RETRIES:
                conn = None
                break
            else:
                backoff = 2 ** retry
                print('Retry attempt {}/{} (wait={}s)...'.format(retry, MAX_RETRIES, backoff))
                time.sleep(backoff)

    if conn:
        return conn
    else:
        raise RuntimeError('Database connect error. Failed to connect after {} retries.'.format(MAX_RETRIES))


def main():
    uri = os.environ.get('DATABASE_URL', None)
    tracemalloc.start()
    s = tracemalloc.take_snapshot()
    cnt = 1
    while True:
        conn = connect(uri)
        conn.close()
        if cnt % 2000 == 0:
            top_stats = tracemalloc.take_snapshot().compare_to(s, 'lineno')
            for stat in top_stats[:20]:
                print(str(stat))
        cnt = cnt + 1
        time.sleep(0.01)

if __name__ == '__main__':
    main()
