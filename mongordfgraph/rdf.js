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
	});

