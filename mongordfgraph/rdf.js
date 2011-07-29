s = db.system.js;

s.remove( { _id : "registerNameSpace" } );
s.remove( { _id : "storeTriple" } );
s.remove( { _id : "storeQuad" } );
s.remove( { _id : "sparql" } );

s.save( { 
	_id:"registerNameSpace", 
	value:function(short, uri) {
		db.namespaces.save({'_id':short, 'uri':uri});
		}
	} );

s.save( {
	_id:"storeTriple",
	value:function(subject, predicate, object){

		/*test valid arguments (subject must be uri)*/
		/*test valid arguments (predicate must be uri)*/
		/*test valid arguments (object must be uri or Literal)*/

		subj = db.triplestore.find({_id:subject});
		if (subj.count() == 0){
			db.triplestore.save({subject:{predicate:[object]}});
		}
	}
	} );