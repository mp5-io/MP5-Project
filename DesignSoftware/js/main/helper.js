function createShape(type, size, x, z){
	var material = new THREE.MeshPhongMaterial( { color: 0x9B2D30  ,transparent: true,opacity:0.9 });
	var myMesh = objects[objects.length];
	/*floorOffset represents the offset to set the object at y = 0
	For example, a cube is defined by its center's position, so if its size is 50, its center's position is (25,25,25)
	So we have to put an negative offset of 25. */
	switch(type){
		case "cube":
		myMesh = new THREE.Mesh(new THREE.BoxGeometry(size, size, size),material);
		myMesh.floorOffset = size/2;
		break;
		case "sphere":
		myMesh = new THREE.Mesh(new THREE.SphereGeometry( size, 32, 16 ),material);
		myMesh.floorOffset = size;
		break;
		case "cylinder":
		myMesh = new THREE.Mesh(new THREE.CylinderGeometry( size, size, size, 20, 4 ),material);
		myMesh.floorOffset = size/2;
		break;
		case "dome":
		myMesh = new THREE.Mesh(new THREE.SphereGeometry( size, 32, 16, 0, 2 * Math.PI, 0, Math.PI / 2 ),material);
		myMesh.floorOffset = 0;
		break;
		case "pyramid":
		myMesh = new THREE.Mesh(new THREE.CylinderGeometry( 0, size, size, 4, 4 ),material);
		myMesh.floorOffset = size/2;
		myMesh.rotation.set(0,de2ra(45),0);
		break;
		case "cone":
		myMesh = new THREE.Mesh(new THREE.CylinderGeometry( 10, size, 100, 20, 4 ),material);
		myMesh.floorOffset = size;
		break;
		case "octahedron":
		myMesh = new THREE.Mesh(new THREE.OctahedronGeometry( size, 0 ),material);
		myMesh.floorOffset = size;
		break;
		case "torus":
		myMesh = new THREE.Mesh(new THREE.TorusGeometry( size, size, 8, 4 ),material);
		myMesh.floorOffset = size*2;
		break;
		case "tetrahedron":
		myMesh = new THREE.Mesh(new THREE.TetrahedronGeometry( size, 0 ),material);
		myMesh.floorOffset = size/2;
		break;
		case "prism":
		myMesh = new THREE.Mesh(new THREE.CylinderGeometry( size, size, size, 6, 4 ),material);
		myMesh.floorOffset = size/2;
		break;
		case "icosahedron":
		myMesh = new THREE.Mesh(new THREE.IcosahedronGeometry( size,1 ),material);
		myMesh.floorOffset = size;
		break;
		default:
		console.log("Shape not defined, generation aborded");
		return;
		break;
	}
	
	myMesh.position.set(x,myMesh.floorOffset,z);

	myMesh.axes = new THREE.AxisHelper(70);
	myMesh.axes.position = myMesh.position;

	myMesh.material.color.setRGB( Math.random(),Math.random(), Math.random());

	setLimit(myMesh);
	myMesh.name="mesh" +objects.length;
	objects.push(myMesh);
	scene.add(myMesh);
	currentMesh = myMesh;
	

	console.log("shape created");
}


//Define extreme coordinates of the object, its lowest x,y,z & highest x,y,z
function setLimit(mesh){
	mesh.minX = mesh.position.x - mesh.floorOffset * mesh.scale.x;
	mesh.maxX = mesh.position.x + mesh.floorOffset * mesh.scale.x;
	mesh.minY = mesh.position.y - mesh.floorOffset * mesh.scale.y;
	mesh.maxY = mesh.position.y + mesh.floorOffset * mesh.scale.y;
	mesh.minZ = mesh.position.z - mesh.floorOffset * mesh.scale.z;
	mesh.maxZ = mesh.position.z + mesh.floorOffset * mesh.scale.z;
	//console.log(mesh.minZ +" " +mesh.minY +" " +mesh.minX);
}

function reajustPosition(mesh){
	if (INTERSECTED) {
        setLimit(mesh);
        if(INTERSECTED.minY < 0){ //Object moved under the plane
        	INTERSECTED.position.y = INTERSECTED.floorOffset*INTERSECTED.scale.y;
        }
        /*if(INTERSECTED.maxX > 500){ //Object moved  too far in x
        	INTERSECTED.position.x = -INTERSECTED.floorOffset*INTERSECTED.scale.x+500;
        }
        if(INTERSECTED.minX < -500){ //Object moved  too far in x
        	INTERSECTED.position.x = INTERSECTED.floorOffset*INTERSECTED.scale.x-500;
        }
        if(INTERSECTED.maxZ > 500){ //Object moved  too far in z
        	INTERSECTED.position.z = -INTERSECTED.floorOffset*INTERSECTED.scale.z+500;
        }
        if(INTERSECTED.minZ < -500){ //Object moved  too far in z
        	INTERSECTED.position.z = +INTERSECTED.floorOffset*INTERSECTED.scale.z-500;
        }*/
        plane.position.copy(INTERSECTED.position);
        SELECTED = null;
    }
    setLimit(mesh);
}

var de2ra = function(degree) { return degree*(Math.PI/180);};

function translate(dx, dy, dz){
	currentMesh.position.x	+= dx * 50;
	currentMesh.position.y	+= dy * 50;
	currentMesh.position.z	+= dz * 50;
}

function render() 
{
	controls.update();
	renderer.render( scene, camera );
}

function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame( animate );
	render();	
}