'''This is the RDFLib/mongoDB storage backend'''

import rdflib

from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE


class MongoStore(Store):
	from pymongo import Connection
	def __init__(self, configuration=None, identifier=None):
		if configuration:
			self.open(configuration)
	
	#Database management methods
	def create(self, configuration):
		pass

	def open(self, configuration, create=False):
		self.name = configuration['name']
                self.connection = Connection(configuration['name'])
                self.instances = self.connection.triplestore
                self.namespaces = self.connection.namespaces
		self.js = self.connection.js

	def destroy(self, configuration):
		pass

	def gc(self):
		pass

	#RDF APIs
	def add(self, (subject, predicate, object), context, quoted=False):
		self.js.storeTriple(subject, predicate, object)

	def remove(self, (subject, predicate, object), context=None):
		self.js.removeTriple(subject, predicate, object)

	def triples_choices(self, (subject, predicate, object_),context=None):
		pass

	def triples(self, (subject, predicate, object), context=None):
		if subject:
			if self.instances.find({'_id':subject}).count() == 1:
				if predicate:
					if self.instances.find({'_id':subject, 'predicate.uri':predicate}).count()>0:
						if object:
							if self.instances.find().count() > 0:
								yield (subject, predicate, object), None
							else:
								pass
						else:
							i = self.instances.find_one({'_id':subject, 'predicate.uri':predicate})
							for o in i['predicate']:
								if o['uri']==predicate:	
									for u in o['value']:	
										yield(subject, predicate, u), None
					else:
						pass
				else:
					ps = self.instances.find_one({'_id':subject})
					if object:
						for p in ps['predicate']:
							for v in p['value']:
								if v == object:
									yield(subject, p['uri'], object), None
					else:
						for p in ps['predicate']:
							for v in p['value']:
								yield (subject, p['uri'], v), None
			else:
				pass						
						
		elif predicate:
			if self.instances.find({'predicate.uri':predicate}).count()>0:
				if object:
					
		elif object:
			pass
		else:
			for stree in self.instances.find():
				for p in stree['predicate']:
					for o in p['value']:
						yield (stree['_id'], p['uri'], o), None

	# variants of triples will be done if / when optimization is needed
	def __len__(self, context=None):
		i = 0
		for triple in self.triples((None, None, None)):
			i+=1
		return i

	def contexts(self, triple=None):
		return self.name

	# Optional Namespace methods
	def bind(self, prefix, namespace):
		self.js.registerNamespace(prefix, namespace)

	def prefix(self, namespace):
		ret = self.namespaces.find_one({'uri':namespace})
		if ret:
			return ret['_id']
		return None
	
	def namespace(self, prefix):
		ret = self.namespaces.find_one({'_id':prefix})
		if ret:
			return ret['uri']
		return None

	def namespaces(self):
		for ns in self.namespaces.find():
			yield ns['_id'], ns['uri']

	# Optional Transactional methods
	def commit(self):
		pass

	def rollback(self):
		pass

plugin.register('MongoRDF', Store, 'store','MongoStore')

