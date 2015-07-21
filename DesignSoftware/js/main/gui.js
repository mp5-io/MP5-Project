function initGui(){
	parameters = 
	{
		selected_mesh : currentMesh.name,
		scaleX:1, scaleY:1, scaleZ:1, scaleUniform:1,
		xPos: 0, yPos: 30, zPos: 0,
		rotationX:0, rotationY:0,rotationZ:0,
		color: "#ff0000", // color (change "#" to "0x")
		opacity: 1, 
		visible: true,
		axes:true,
		material: "Phong",
		wireframe:false,

		reset: function() { resetCube() }
	};


	gui.add(parameters, 'selected_mesh').listen();

	var f2 = gui.addFolder('Position');
	var cubeX = f2.add( parameters, 'xPos' ).min(-500).max(500).step(1).listen();
	var cubeY = f2.add( parameters, 'yPos' ).min(0).max(100).step(1).listen();
	var cubeZ = f2.add( parameters, 'zPos' ).min(-500).max(500).step(1).listen();
	
	cubeX.onChange(function(value) 
	{   currentMesh.position.x = value;   });
	cubeY.onChange(function(value) 
	{   currentMesh.position.y = value;   });
	cubeZ.onChange(function(value) 
	{   currentMesh.position.z = value;   });
	f2.open();
	
	var f1 = gui.addFolder('Scale');
	//We fix a maximum scale : currentSize*scale <= sizeFloor
	limitScale = GRIDSIZE/currentMesh.Size;
	f1.add(parameters, 'scaleX', 1, 10,1).onChange( function(value) { 
       currentMesh.scale.x = value;
    });
    f1.add(parameters, 'scaleY', 1, 10,1).onChange( function(value) {
       currentMesh.scale.y = value;
    });
    f1.add(parameters, 'scaleZ', 1, 10,1).onChange( function(value) {
       currentMesh.scale.z = value;
    });
    f1.add(parameters, 'scaleUniform', 1, 10,1).onChange( function(value) {
       currentMesh.scale.z = value;
       currentMesh.scale.y = value;
       currentMesh.scale.x = value;
    });
    f1.close();

    var f3 = gui.addFolder('Rotation');
    f3.add(parameters, 'rotationX', -180, 180).onChange( function() {
       currentMesh.rotation.x = de2ra(parameters.rotationX);
    });
    f3.add(parameters, 'rotationY', -180, 180).onChange( function() {
       currentMesh.rotation.y = de2ra(parameters.rotationY);
    });
    f3.add(parameters, 'rotationZ', -180, 180).onChange( function() {
       currentMesh.rotation.z = de2ra(parameters.rotationZ);
    });
    f3.close();

	var cubeColor = gui.addColor( parameters, 'color' ).name('Color').listen();
	cubeColor.onChange(function(value) // onFinishChange
	{   currentMesh.material.color.setHex( value.replace("#", "0x") );  
	});
	
	var cubeOpacity = gui.add( parameters, 'opacity' ).min(0).max(1).step(0.01).name('Opacity').listen();
	cubeOpacity.onChange(function(value)
	{   currentMesh.material.opacity = value;   });
	
	
	var cubeVisible = gui.add( parameters, 'visible' ).name('Visible?').listen();
	cubeVisible.onChange(function(value) 
	{   currentMesh.visible = value;	
		currentMesh.axes.visible = value;
	});
	
	var cubeAxes= gui.add(parameters, 'axes').name('Axes?').listen();
	cubeAxes.onChange(function(value) 
	{   currentMesh.axes.visible = value; 	});

	gui.add(parameters,'wireframe').name("Wireframe?").onChange( function(value){
		currentMesh.material.wireframe = value;
	});

	gui.add( parameters, 'reset' ).name("Reset Cube Parameters");


}


function initGuiShape(){
	
	gui2.domElement.style.position = 'absolute';
	gui2.domElement.style.left='0px';
	elements = {
		number:2,
		cube: function() { displayShape("cube") },
		sphere: function() { displayShape("sphere") },
		cylinder: function(){ displayShape("cylinder")},
		dome: function() { displayShape("dome") },
		pyramid: function() { displayShape("pyramid") },
		cone: function() { displayShape("cone") },
		octahedron: function() { displayShape("octahedron") },
		torus: function() { displayShape("torus") },
		prism: function() { displayShape("prism") },
		tetrahedron: function() { displayShape("tetrahedron") },
		octahedron: function() { displayShape("octahedron") },
		icosahedron: function() { displayShape("icosahedron") }
	};
	gui2.add(elements, 'number').name("generated shapes:").listen();
	var shapes = gui2.addFolder('shapes');
	for(e in elements){
		if(e!="number")
			shapes.add(elements,e).name(e);
	}
	
}

function displayShape(mesh){
	var limitX = (objects.length-3)%10;
	var limitZ = Math.floor((objects.length-2)/10);
	var x = (100*limitX)-475;
	var z = (100*limitZ)-475;
	
	createShape(mesh,50,x,z);
	
	elements.number+=1;
}



function updateCube(currentMesh){
	currentMesh.material.wireframe = parameters.wireframe;
	currentMesh.scale.x = parameters.scaleX;
	currentMesh.scale.y = parameters.scaleY;
	currentMesh.scale.z = parameters.scaleZ;
	currentMesh.rotation.x = parameters.rotationX;
	currentMesh.rotation.y = parameters.rotationY;
	currentMesh.rotation.z = parameters.rotationZ;
	currentMesh.material.color.setHex( parameters.color.replace("#", "0x") );
	currentMesh.material.opacity = parameters.opacity;  
	currentMesh.material.transparent = true;
	currentMesh.visible = parameters.visible;
	currentMesh.axes.visible = parameters.axes;
	setLimit(currentMesh);
	reajustPosition(currentMesh);
}


function resetCube(){
	parameters.x = 0+INTERSECTED.floorOffset*INTERSECTED.scale.x;
	parameters.y = 30+INTERSECTED.floorOffset*INTERSECTED.scale.y;
	parameters.z = 0+INTERSECTED.floorOffset*INTERSECTED.scale.z;
	parameters.scaleX = 1;
	parameters.scaleY = 1;
	parameters.scaleZ = 1;
	parameters.rotationX = 0;
	parameters.rotationY = 0;
	parameters.rotationX = 0;
	parameters.color = "#ff0000";
	parameters.opacity = 1;
	parameters.visible = true;
	parameters.axes = true;
	parameters.material = "Phong";
	parameters.wireframe = false;
	currentMesh.position.set(0,0,0);
	currentMesh.rotation.set(0,0,0);
	updateCube(currentMesh);
}
