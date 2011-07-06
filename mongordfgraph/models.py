import uuid 

class MongoRdfStore(object):
	def __init__(self, store_name="RDF", coll_name="RDF"):
		from pymongo.connection import Connection
		self._connection = Connection()
		self._db = self._connection[store_name]
		self._collection = self._db[coll_name]
		self._store_name = store_name
		self._coll_name = coll_name

	def get_store_name(self):
		return self._store_name

	def createResource(self, uri="%s/%s" % ("", str(uuid.uuid4()),), rtype = "rdf:Resource", node = True, BN=False):
		return Resource(uri, rtype, node, BN, self._collection)

	def createClass(self, uri="%s/%s" % ("", str(uuid.uuid4()),)):
		return Class(uri, self._collection)		

	def createProperty(self, uri="%s/%s" % ("", str(uuid.uuid4()),)):
		return Property(uri, self._collection)

	

class Resource(object):
       	def __init__(self, uri="%s/%s" % ("", str(uuid.uuid4()),), rtype = "rdf:Resource", node = True, BN=False, collection=None):
                self.uri = uri
       	        self.rtype = rtype
               	self.attributes = {}
		self.blank_node = BN
		self.is_node = node

      	def set_attribute(self, attribute, value, vtype="rdfs:Literal", language=None):
                if not self.attributes.has_key(attribute.uuid):
       	                self.attributes[attribute.uuid] = []
		att = {}
		att['value'] = value
		att['type'] = vtype
		if language:
			att['lang'] = language
               	self.attributes[attribute.uuid].append(att)
                return self

       	def save(self):
               	store.save(self._to_json())

        def _to_json(self):
       	        return{
               	        "uri":str(self.uri),
                       	"type":str(self.rtype),
                        "attributes":self.attributes
       	        }

	def to_json(self):
		itm_uri = "%s/%s" % ("", self.uuid,)
		x = {
			itm_uri: {
				'rdf:Type':[{"value":self.rtype, "type": "uri"}],				
			}
		}
		for att in self.attributes:	
			el = {}
			el['value']=att.value
			el['type'] =att.type
			el['lang'] =att.lang
			if not x[itm_uri].has_key(att.name):
				x[itm_uri][att.name] = []
			x[itm_uri][att.name].append(el)
		return x

class Class(Resource):
        def __init__(self, uri="%s/%s" % ("", str(uuid.uuid4()),), collection=None):
                super(Class, self).__init__(uri, "rdfs:Class")

        def to_json(self):
                jj = super(Klass, self).to_json()
                return jj

	@classmethod
	def get(self, klass_name):
		if True:
			pass

class Property(Resource):
        def __init__(self, uri="%s/%s" % ("", str(uuid.uuid4()),)):
                super(Property, self).__init__(uri, "rdf:Property")
                self.name = name

