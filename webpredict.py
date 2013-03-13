#!/usr/bin/env python
import webapp2
import LocalPredict
import os

from google.appengine.ext.webapp import template

template.DEBUG = True

def jspathforargs(**args):
	"""[
		   [header, [[key, pretty, note, value], [key, pretty, note, value], ...]]
		   ...
	   ]"""
	return [(header, [(key, value[0], value[1], args.get(key, '')) for key, value in inputs]) for header, inputs in LocalPredict.webinputs]

def getargdict():
	pass

class MainHandler(webapp2.RequestHandler):
	def post(self):
		self.get()
	def get(self):
		keys = self.request.arguments()
		values = (self.request.get(k, '') for k in keys)
		query_args = dict(zip(keys, values))
		
		render={}
		
		render['inputs'] = jspathforargs(**query_args)
		
		if self.request.get('go', '') == '':
			path = os.path.join(os.path.dirname(__file__), 'home.html')
		else:
			path = os.path.join(os.path.dirname(__file__), 'map.html')
			try:
				uptrack, downtrack = LocalPredict.webPredict(query_args)
				formattrack = lambda points: "[%s]" % ",".join("[%s,%s]" % (lat, lon) for lat, lon, alt in points)
				render['uptrack'] = formattrack(uptrack)
				render['downtrack'] = formattrack(downtrack)
				render['error'] = False
			except LocalPredict.PredictionException as err:
				path = os.path.join(os.path.dirname(__file__), 'error.html')
				render['error'] = {'message':err.args[0], 'type':'prediction error'}
			except Exception as err:
				path = os.path.join(os.path.dirname(__file__), 'error.html')
				render['error'] = {'message':err.args, 'type':'other'}

		self.response.out.write(template.render(path, render))
		
class AddHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write('hi')
		
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/add', AddHandler),
], debug=True)
