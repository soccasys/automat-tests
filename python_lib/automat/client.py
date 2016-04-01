# Copyright (c) 2016, Socca Systems -- All Rights Reserved
import httplib
import json

class Automat:
	def __init__(self, host, port=80):
		self.host = host
		self.port = port
		self.automat = httplib.HTTPConnection(host, port)
	def Project(self, name):
		# FIXME Check that the name of the project is sane.
		p = Project(self, name)
		p.Get()
		return p

class Component:
	def __init__(self, name, url, revision):
		self.name = name
		self.url = url
		self.revision = revision

class BuildStep:
	def __init__(self, description, directory, command):
		self.description = description
		self.directory = directory
		self.command = command

class Project:
	def __init__(self, automat, name):
		self.automat = automat
		# FIXME Check that the name of the project is sane.
		self.name = name

	def Get(self):
		# Contact the automat server to get the description of the project.
		self.automat.connect()
		try:
			self.automat.request("GET", "/projects/%s" % (self.name,))
			response = self.automat.getresponse()
			data = json.loads(response.read())
		finally:
			self.automat.close()
		# FIXME Check that the name is consistent
		self.name = data['name']
		self.components = {}
		for cname in data['components']:
			self.components[cname] = Component(s['name'], s['url'], s['revision'])
		self.steps = []
		for s in data['steps']:
			self.steps.append(BuildStep(s['description'], s['directory'], s['command']))
		# FIXME Add support for the environment variables

	def Build(self):
		# Contact the server to trigger a build.
		self.automat.connect()
		try:
			self.automat.request("GET", "/projects/%s/build" % (self.name,))
			response = self.automat.getresponse()
			data = json.loads(response.read())
		finally:
			self.automat.close()
		print data
