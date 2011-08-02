'''This is the RDFLib/mongoDB storage backend'''

import rdflib

from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE


class MongoStore(Store):
	def __init__(self, configuration=None, identifier=None):
		pass

	#Database management methods
	def create(self, configuration):
		pass

	def open(self, configuration, create=False):
		pass

	def destroy(self, configuration):
		pass

	def gc(self):
		pass

	#RDF APIs
	def add(self, (subject, predicate, object), context, quoted=False):
		pass

	def remove(self, (subject, predicate, object), context=None):
		pass

	def triples_choices(self, (subject, predicate, object_),context=None):
		pass

	def triples(self, (subject, predicate, object), context=None):
		pass

	# variants of triples will be done if / when optimization is needed
	def __len__(self, context=None):
		pass

	def contexts(self, triple=None):
		pass

	# Optional Namespace methods
	def bind(self, prefix, namespace):
		pass

	def prefix(self, namespace):
		pass
	
	def namespace(self, prefix):
		pass

	def namespaces(self):
		pass

	# Optional Transactional methods
	def commit(self):
		pass

	def rollback(self):
		pass

