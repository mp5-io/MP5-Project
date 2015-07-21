
	///////////
	// ROW 1 //
	///////////
	
	// cube
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.CubeGeometry(50, 50, 50, 1, 1, 1), 
		multiMaterial );
	shape.position.set(-200, 50, 100);
	scene.add( shape );
	// icosahedron
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.IcosahedronGeometry( 40, 0 ), // radius, subdivisions
		multiMaterial );
	shape.position.set(-100, 50, 100);
	scene.add( shape );
	// octahedron
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.OctahedronGeometry( 40, 0 ), 
		multiMaterial );
	shape.position.set(0, 50, 100);
	scene.add( shape );
	// tetrahedron
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.TetrahedronGeometry( 40, 0 ), 
		multiMaterial );
	shape.position.set(100, 50, 100);
	scene.add( shape );
	// sphere
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.SphereGeometry( 40, 32, 16 ), 
		multiMaterial );
	shape.position.set(200, 50, 100);
	scene.add( shape );
	
	///////////
	// ROW 2 //
	///////////
	
	// cube
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.CubeGeometry(50, 50, 50, 2, 2, 2), 
		multiMaterial );
	shape.position.set(-200, 50, 0);
	scene.add( shape );
	// icosahedron
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.IcosahedronGeometry( 40, 1 ), // radius, subdivisions
		multiMaterial );
	shape.position.set(-100, 50, 0);
	scene.add( shape );
	// octahedron
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.OctahedronGeometry( 40, 1 ), 
		multiMaterial );
	shape.position.set(0, 50, 0);
	scene.add( shape );
	// tetrahedron
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.TetrahedronGeometry( 40, 1 ), 
		multiMaterial );
	shape.position.set(100, 50, 0);
	scene.add( shape );
	// dome
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		new THREE.SphereGeometry( 40, 32, 16, 0, 2 * Math.PI, 0, Math.PI / 2 ), 
		multiMaterial );
	// should set material to doubleSided = true so that the 
	//   interior view does not appear transparent.
	shape.position.set(200, 50, 0);
	scene.add( shape );
	
	///////////
	// ROW 3 //
	///////////
	
	// cylinder
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// radiusAtTop, radiusAtBottom, height, segmentsAroundRadius, segmentsAlongHeight,
		new THREE.CylinderGeometry( 30, 30, 80, 20, 4 ), 
		multiMaterial );
	shape.position.set(-200, 50, -100);
	scene.add( shape );
	
	// cone
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// radiusAtTop, radiusAtBottom, height, segmentsAroundRadius, segmentsAlongHeight,
		new THREE.CylinderGeometry( 0, 30, 100, 20, 4 ), 
		multiMaterial );
	shape.position.set(-100, 50, -100);
	scene.add( shape );
	
	// pyramid
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// radiusAtTop, radiusAtBottom, height, segmentsAroundRadius, segmentsAlongHeight,
		new THREE.CylinderGeometry( 0, 30, 100, 4, 4 ), 
		multiMaterial );
	shape.position.set(0, 50, -100);
	scene.add( shape );
	// torus
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
	    // radius of entire torus, diameter of tube (less than total radius), 
		// segments around radius, segments around torus ("sides")
		new THREE.TorusGeometry( 25, 10, 8, 4 ),
		multiMaterial );
	shape.position.set(100, 50, -100);
	scene.add( shape );
	// torus knot
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// total knot radius, tube radius, number cylinder segments, sides per cyl. segment,
		//  p-loops around torus, q-loops around torus
		new THREE.TorusKnotGeometry( 30, 8, 60, 10, 2, 3 ), 
		multiMaterial );
	shape.position.set(200, 50, -100);
	scene.add( shape );
	///////////
	// ROW 4 //
	///////////
	
	// prism
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// radiusAtTop, radiusAtBottom, height, segmentsAroundRadius, segmentsAlongHeight,
		new THREE.CylinderGeometry( 30, 30, 80, 6, 4 ), 
		multiMaterial );
	shape.position.set(-200, 50, -200);
	scene.add( shape );
	
	// cone - truncated
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// radiusAtTop, radiusAtBottom, height, segmentsAroundRadius, segmentsAlongHeight,
		new THREE.CylinderGeometry( 10, 30, 100, 20, 4 ), 
		multiMaterial );
	shape.position.set(-100, 50, -200);
	scene.add( shape );
	
	// pyramid - truncated
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// radiusAtTop, radiusAtBottom, height, segmentsAroundRadius, segmentsAlongHeight,
		new THREE.CylinderGeometry( 15, 30, 100, 6, 4 ), 
		multiMaterial );
	shape.position.set(0, 50, -200);
	scene.add( shape );
	// torus
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
	    // radius of entire torus, diameter of tube (less than total radius), 
		// sides per cylinder segment, cylinders around torus ("sides")
		new THREE.TorusGeometry( 30, 20, 16, 40 ),
		multiMaterial );
	shape.position.set(100, 50, -200);
	scene.add( shape );
	// torus knot
	var shape = THREE.SceneUtils.createMultiMaterialObject( 
		// total knot radius, tube radius, number cylinder segments, sides per cyl. segment,
		//  p-loops around torus, q-loops around torus
		new THREE.TorusKnotGeometry( 30, 6, 160, 10, 3, 7 ), 
		multiMaterial );
	shape.position.set(200, 50, -200);
	scene.add( shape );