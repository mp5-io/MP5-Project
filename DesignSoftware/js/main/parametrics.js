function createGraph()
{
	console.log("createIn");
	uRange = uMax - uMin;
	vRange = vMax - vMin;
	xFunc = Parser.parse(xFuncText).toJSFunction( ['u','v'] );	
	yFunc = Parser.parse(yFuncText).toJSFunction( ['u','v'] );	
	zFunc = Parser.parse(zFuncText).toJSFunction( ['u','v'] );
	meshFunction = function(u0, v0) 
	{
		var u = uRange * u0 + uMin;
		var v = vRange * v0 + vMin;
		var x = xFunc(u,v);
		var y = yFunc(u,v);
		var z = zFunc(u,v);
		if ( isNaN(x) || isNaN(y) || isNaN(z) )
			return new THREE.Vector3(0,0,0); // TODO: better fix
		else
			return new THREE.Vector3(x, y, z);
	};
	
	// true => sensible image tile repeat...
	graphGeometry = new THREE.ParametricGeometry( meshFunction, segments, segments, true );
	
	
	graphMesh = new THREE.Mesh( graphGeometry, wireframeMaterial );
	scene.add(graphMesh);
	console.log("createOut");
}