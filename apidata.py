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

cursor.execute('create table if not exists movie (id, title, original_title, url, rating, images, directors, casts, year, genres, countries, summary)')
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


movie_id=[]

#print(index)
response = urllib.request.urlopen('http://api.douban.com/v2/movie/top250')
data = response.read()
data = data.decode('utf-8')
data_json = json.loads(data)
top250 = data_json['subjects']
for movie in top250:
	movie_id.append(movie['id'])
	print(movie['id'],movie['title'])
#time.sleep(3)


count=0
for n in movie_id:
	print(count, n)
	response = urllib.request.urlopen('http://api.douban.com/v2/movie/subject/%s' % n)
	data=response.read()
	add_movie(data)
	count+=1
	time.sleep(3)
