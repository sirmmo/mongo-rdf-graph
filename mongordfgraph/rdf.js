s = db.system.js;

s.remove( { _id : "registerNameSpace" } );
s.remove( { _id : "storeTriple" } );
s.remove( { _id : "storeQuad" } );
s.remove( { _id : "sparql" } );
s.remove( { _id : "validateUri" } );

s.save( { 
	_id:"registerNameSpace", 
	value:function(short, uri) {
		db.namespaces.save({'_id':short, 'uri':uri});
	}
} );

s.save( {
	_id:"validateUri", 
	value:function(uri){
		var parts = uri.split(":");

		/*local "_" uris*/
		if (parts[0] == "_")
			return parts.join(":");

		/*regsitered qnames*/
		var ns = db.namespaces.find({'_id':parts[0]})
		if (ns.count()>0){
			parts[0] = ns[0]['uri'];
			return parts.join("");
		}

		/*full uris*/
		var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
		if (regexp.test(uri))
			return uri;
		throw "Non valid URI";
	}
} );

s.save( {
	_id:"validateObject",
	value:function(object){
		if (!("type" in object))
			throw "type must be set";
		if (!("value" in object))
			throw "value must be set";
		if ("lang" in object)
			if (object['lang'] == "")
				throw "lang must not be empty if set";
		if (!(object['type'] == "uri" || object['type'] =="literal" ||object['type']=="bnode"))
			throw "type must be in [uri, literal,bnode]";
		if (object['type'] == "uri")
			object['value'] = validateUri(object['value']);
		if ("datatype" in object)
			object['datatype'] = validateUri(object['datatype']);
		return object
	}
} );

s.save( {
	_id:"storeTriple",
	value:function(subject, predicate, object){
		ts = db.triplestore

		/*test valid arguments (subject must be uri)*/
		subject =  validateUri(subject);
		/*test valid arguments (predicate must be uri)*/
		predicate = validateUri(predicate);
		/*test valid arguments (object must be uri or Literal)*/
		object = validateObject(object);

		subj = ts.find({_id:subject});
		
		/*Do we have the subject?*/
		if (subj.count() == 0){
			/*Nope*/
			triple = {
				_id:subject, 
				predicate:[{
					uri:predicate, 
					value:[object]
				}]
			};
			db.triplestore.save(triple);
		}
		else{
			/*yep*/
			/*do we have the predicate and the subject?*/
			pred = ts.find({_id : subject, 'predicate.uri' : predicate})
			if (pred.count() == 0){
				db.triplestore.update({
					_id:subject
				}, {
					$push:{
						predicate:{
							uri:predicate,
							value:[object]
						}
					}
				}, false, true);
			} else {
				obj = ts.find({_id:subject, predicate:{uri:predicate, value:object}});
				if (obj.count() == 0){
					db.triplestore.update({
						_id:subject,
						'predicate.uri':predicate
					}, {
						$push:{
							'predicate.$.value':object
						}
					}, false, true);
				}

				else{}
			}
		}
	}
} );
