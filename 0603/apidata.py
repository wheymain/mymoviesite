#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import time
import sqlite3
import web

conn = sqlite3.connect('moviesite.db')    #若没有此数据库，则自动创建
cursor = conn.cursor()

cursor.execute('drop table movie')  #删除原先的数据表
cursor.execute('drop table casts')

cursor.execute('create table if not exists movie (id, title, original_title, url, rating, images, directors, casts, year, genres, countries, summary)')
cursor.execute('create table if not exists casts (id, name, name_en, gender, born_place, url, avatars)')

db = web.database(dbn='sqlite', db='moviesite.db')

def add_movie(data):
	data = data.decode('utf-8')
	movie=json.loads(data)
	db.insert('movie', 
		id=int(movie['id']),
		title=movie['title'],
		original_title=movie['original_title'],
		url=movie['alt'],
		rating=movie['rating']['average'],
		images=movie['images']['large'],
		directors=','.join([d['name'] for d in movie['directors']]),
		casts=','.join([c['name'] for c in movie['casts']]),
		year=movie['year'],
		genres=','.join(movie['genres']),
		countries=','.join(movie['countries']),
		summary=movie['summary'],
		)

def add_cast(data):
	data = data.decode('utf-8')
	casts=json.loads(data)
	db.insert('casts', 
		id=int(casts['id']),
		name=casts['name'],
		name_en=casts['name_en'],
		gender=casts['gender'],
		born_place=casts['born_place'],
		url=casts['alt'],
		avatars=casts['avatars']['large'],
		#works=','.join([e['title'] for e in casts['works']]),
		)


movie_id=[]
casts_id=[]

#print(index)
response = urllib.request.urlopen('http://api.douban.com/v2/movie/top250')
data = response.read()
data = data.decode('utf-8')
data_json = json.loads(data)
top250 = data_json['subjects']
for movie in top250:
	movie_id.append(movie['id'])
	for n in range(len(movie['casts'])):
		casts_id.append(movie['casts'][n]['id'])
	print(movie['id'],movie['title'], casts_id)


count=0
for n in movie_id:
	print(count, n)
	response = urllib.request.urlopen('http://api.douban.com/v2/movie/subject/%s' % n)
	data=response.read()
	add_movie(data)
	count+=1
	time.sleep(2)

count=0
for num in casts_id:
	response = urllib.request.urlopen('http://api.douban.com/v2/movie/celebrity/%s' % num)
	castdata = response.read()
	add_cast(castdata)
	count+=1
	time.sleep(2)
