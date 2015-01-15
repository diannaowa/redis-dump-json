#!/usr/bin/env python
#coding=utf-8

import json,redis
import argparse

class redisDump(object):
	def __init__(self,**kwargs):
		self.r = redis.Redis(
				host=kwargs['host'],
				port=kwargs['port'],
				password=kwargs['password'],
				db=kwargs['db'],
				encoding='utf-8')

	def __reader(self):
		for key in self.r.keys():
			key = key.decode('utf-8')
			type = self.r.type(key)
			if type == 'none':
				pass
			reader = readers.get(type)
			if reader is None:
				raise UnknowTypeError("Unknow type key:%s"%key)
			value = self.__readKey(reader,key)
			yield key,type,value
	def __readKey(self,reader,key):
		p = self.r.pipeline()
		p.watch(key)
		p.multi()
		reader.command(p,key)
		data = p.execute()
		return reader.pack(data[0])
	def dumps(self,f):
		encod = json.JSONEncoder(**{'separators':(',',':')})
		f.write('{')
		st = True
		for key,type,value in self.__reader():
			key = encod.encode(key)
			type = encod.encode(type)
			value = encod.encode(value)
			data = '%s:{"type":%s,"value":%s}' %(key,type,value)
			if st:
				st = False
			else:
				f.write(',')#if not the first item write ',' into file
			f.write(data)
		f.write('}')



class stringReader(object):

	@staticmethod
	def command(p,key):
		p.get(key)
	@staticmethod
	def pack(data):
		return data.decode('utf-8')

class setReader(object):
	@staticmethod
	def command(p,key):
		p.smembers(key)
	@staticmethod
	def pack(data):
		return [v.decode('utf-8') for v in data]

class listReader(object):
	@staticmethod
	def command(p,key):
		p.lrange(key,0,-1)
	@staticmethod
	def pack(data):
		return [v.decode('utf-8') for v in data]

class zsetReader(object):
	@staticmethod
	def command(p,key):
		p.zrange(key,0,-1,False,True)
	@staticmethod
	def pack(data):
		return [(v.decode('utf-8'),s) for v,s in data]

class hashReader(object):
	@staticmethod
	def command(p,key):
		p.hgetall(key)
	@staticmethod
	def pack(data):
		r = dict()
		for v in data:
			r[v.decode('utf-8')] = data[v].decode('utf-8')
		return r

readers = {'string':stringReader,
		'list':listReader,
		'set':setReader,
		'zset':zsetReader,
		'hash':hashReader}


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--host',action='store',dest='host',default='localhost',help='redis server host,default[localhost]')
	parser.add_argument('--port',action='store',dest='port',default=6379,help='redis server port,defalut[6379]')
	parser.add_argument('--passwd',action='store',dest='passwd',default=None,help='redis server passwd,default[None]')
	parser.add_argument('--db',action='store',dest='db',default=0,help='witch database will be export,defalut[0]')
	parser.add_argument('--path',action='store',dest='path',help='the file path,ex:/tmp/dump.json')
	args = parser.parse_args()
	arg = {'host':args.host,
			'port':args.port,
			'password':args.passwd,
			'db':args.db}
	with open(args.path,'w') as f:
		r = redisDump(**arg)
		r.dumps(f)
