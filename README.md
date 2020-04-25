# psycopg2-memory-leak
Memory leak in psycopg2

Every call to set_client_encoding is leaking tiny amount of memory. Though its small amount but if you call this function multiple times you would accumulate memory leak.

Run leak.py to test the memory.

In my case I am setting encoding to 'UTF8' which is leaking 5 bytes per call.

```
/tmp/leak.py:18: size=3105 KiB (+3105 KiB), count=636000 (+636000), average=5 B
/tmp/leak.py:18: size=3125 KiB (+3125 KiB), count=640000 (+640000), average=5 B
/tmp/leak.py:18: size=3135 KiB (+3135 KiB), count=642000 (+642000), average=5 B
/tmp/leak.py:18: size=3145 KiB (+3145 KiB), count=644000 (+644000), average=5 B
/tmp/leak.py:18: size=3154 KiB (+3154 KiB), count=646000 (+646000), average=5 B
```

Note the leak is seen despite I am closing the connection. 
