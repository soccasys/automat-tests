# Copyright (c) 2016, Socca Systems -- All Rights Reserved
import httplib
import json

class ProjectNotFound(Exception):
	def __init__(self, code, reason):
		self.code = code
		self.reason = reason
	def __str__(self):
		return repr(self.code) + " " + repr(self.reason)

class AutomatError(Exception):
	def __init__(self, code, reason):
		self.code = code
		self.reason = reason
	def __str__(self):
		return repr(self.code) + " " + repr(self.reason)

class Server:
	def __init__(self, host, port=80):
		self.host = host
		self.port = port
		self.automat = httplib.HTTPConnection(host, port)
	def GetProject(self, name):
		# FIXME Check that the name of the project is sane.
		p = Project(name, self.automat)
		p.Get()
		return p
	def PutProject(self, p):
		# FIXME Check that the name of the project is sane.
		p.automat = self.automat
		p.Put()
		return p
	def DeleteProject(self, name):
		# FIXME Check that the name of the project is sane.
		p = Project(name, self.automat)
		p.Delete()
		return p
	def BuildRecord(self, hash):
		p = BuildRecord(self.automat, hash)
		p.Get()
		return p

class Component:
	def __init__(self, name, url, revision):
		self.name = name
		self.url = url
		self.revision = revision

class BuildStep:
	def __init__(self, description, directory, command, env):
		self.description = description
		self.directory = directory
		self.command = command
		self.env = env

class Project:
	def __init__(self, name, automat=None):
		self.automat = automat
		# FIXME Check that the name of the project is sane.
		self.name = name
		self.components = {}
		self.steps = []
		self.env = {}

	def Get(self):
		# Contact the automat server to get the description of the project.
		self.automat.connect()
		try:
			self.automat.request("GET", "/projects/%s" % (self.name,))
			response = self.automat.getresponse()
			code, reason = response.status, response.reason
			if code != 200:
				raise ProjectNotFound(code, reason)
			data = json.loads(response.read())
		finally:
			self.automat.close()
		self.Update(data)

	def Put(self):
		# Contact the automat server to create/update the project.
		self.automat.connect()
		try:
			pdata = json.dumps(self.Dump(), sort_keys=True, indent=4, separators=(',', ': '))
			self.automat.request("PUT", "/projects/%s" % (self.name,), pdata)
			response = self.automat.getresponse()
			code, reason = response.status, response.reason
			if code != 200:
				raise AutomatError(code, reason)
			data = json.loads(response.read())
		finally:
			self.automat.close()

	def Delete(self):
		# Contact the automat server to delete the project.
		self.automat.connect()
		try:
			self.automat.request("DELETE", "/projects/%s" % (self.name,))
			response = self.automat.getresponse()
			code, reason = response.status, response.reason
			if code != 200:
				raise ProjectNotFound(code, reason)
			#data = json.loads(response.read())
		finally:
			self.automat.close()

	def Update(self, data):
		# FIXME Check that the name is consistent
		self.name = data['name']
		self.components = {}
		for cname in data['components']:
			self.components[cname] = Component(data['components'][cname]['name'], data['components'][cname]['url'], data['components'][cname]['revision'])
		self.steps = []
		for s in data['steps']:
			self.steps.append(BuildStep(s['description'], s['directory'], s['command'], s['env']))
		# FIXME Add support for the environment variables

	def Build(self):
		# Contact the server to trigger a build.
		self.automat.connect()
		try:
			self.automat.request("GET", "/projects/%s/build" % (self.name,))
			response = self.automat.getresponse()
			code, reason = response.status, response.reason
			if code == 404:
				raise ProjectNotFound(code, reason)
			if code != 200:
				raise AutomatError(code, reason)
			data = json.loads(response.read())
		finally:
			self.automat.close()
		#print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
		b = BuildRecord(self.automat, data['hash'])
		b.Update(data)
		return b

	def Dump(self):
		# Return the project as a python dictionary that can be encoded in JSON.
		data = {}
		data['name'] = self.name
		data['components'] = {}
		for cname in self.components:
			data['components'][cname] = {
				"name": self.components[cname].name,
				"url": self.components[cname].url,
				"revision": self.components[cname].revision
			}
		data['steps'] = []
		index = 0
		for s in self.steps:
			data['steps'].append({
				"description": self.steps[index].description,
				"directory": self.steps[index].directory,
				"command": self.steps[index].command,
				"env": self.steps[index].env,
			})
			index += 1
		data['env'] = self.env
		return data

	def AddComponent(self, name, url, revision):
		self.components[name] = Component(name, url, revision)

	def AddStep(self, description, directory, command, env):
		self.steps.append(BuildStep(description, directory, command, env))

	def SetEnv(self, name, value):
		self.env[name] = value

class CheckoutRecord:
	def __init__(self, name, url, revision, duration, status):
		self.name = name
		self.url = url
		self.revision = revision
		self.duration = duration
		self.status = status

class StepRecord:
	def __init__(self, directory, command, duration, status):
		self.directory = directory
		self.command = command
		self.duration = duration
		self.status = status

class BuildRecord:
	def __init__(self, automat, hash):
		self.automat = automat
		self.hash = hash

	def Get(self):
		# Contact the automat server to get the description of the project.
		self.automat.connect()
		try:
			self.automat.request("GET", "/builds/%s" % (self.hash,))
			response = self.automat.getresponse()
			data = json.loads(response.read())
		finally:
			self.automat.close()
		self.Update(data)

	def Update(self, data):
		# FIXME Check that the name is consistent
		self.name = data['name']
		self.duration = data['duration']
		self.components = {}
		for cname in data['components']:
			self.components[cname] = CheckoutRecord(data['components'][cname]['name'], data['components'][cname]['url'], data['components'][cname]['revision'], data['components'][cname]['duration'], data['components'][cname]['status'])
		self.steps = []
		for s in data['steps']:
			self.steps.append(StepRecord(s['directory'], s['command'], s['duration'], s['status']))
