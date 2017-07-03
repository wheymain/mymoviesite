#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web

render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='moviesite.db')

urls = (
    '/', 'index',
    '/movie/(\d+)', 'movie',
    '/cast/(.*)', 'cast',
    '/director/(.*)', 'director',
)

class index:
    def GET(self):
    	movies = db.select('movie')
    	return render.index(movies)

    def POST(self):
    	data = web.input()
    	condition = r'title like "%'+data.title+'%"'
    	movies = db.select('movie', where=condition)
    	return render.index(movies)

class movie:
	def GET(self, movie_id):
		movie_id = int(movie_id)
		movie = db.select('movie', where='id=$movie_id',vars=locals())[0]
		return render.movie(movie)

class cast:
	def GET(self,cast_id):
		cast_id = int(cast_id)
		cast = db.select('casts', where='id=$cast_id',vars=locals())[0]
		return render.cast(cast)

if __name__=='__main__':
	app = web.application(urls,globals())
	app.run()
