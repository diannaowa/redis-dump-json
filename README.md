# redis-dump-json
Export redis data to a file, save it as JSON format,with python<br />
For help
```python
[root@localhost~]# python redis-dump.py --help
usage: redis-dump.py [-h] [--host HOST] [--port PORT] [--passwd PASSWD]
                     [--db DB] [--path PATH]

optional arguments:
  -h, --help       show this help message and exit
  --host HOST      redis server host,default[localhost]
  --port PORT      redis server port,defalut[6379]
  --passwd PASSWD  redis server passwd,default[None]
  --db DB          witch database will be export,defalut[0]
  --path PATH      the file path,ex:/tmp/dump.json
```
Dump redis data
```python
[root@localhost~]# python redis-dump.py --path /tmp/dump.json
```
