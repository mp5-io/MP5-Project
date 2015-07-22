

function keyboardManage(){
	var delta = clock.getDelta(); // seconds.
	var moveDistance = 50; // 200 pixels per second
	var rotateAngle = Math.PI / 4 * delta;   // pi/2 radians (90 degrees) per second

	// local coordinates
	// local transformations
	// move forwards/backwards/left/right
	if ( keyboard.pressed("Z") )
		currentMesh.position.z -= moveDistance;
	if ( keyboard.pressed("S") )
		currentMesh.position.z += moveDistance;
	if ( keyboard.pressed("Q"))
		currentMesh.position.x -= moveDistance;
	if ( keyboard.pressed("D") )
		currentMesh.position.x += moveDistance;
	if ( keyboard.pressed("1"))
		currentMesh.position.y += moveDistance;
	if ( keyboard.pressed("2") )
		currentMesh.position.y -= moveDistance;

	// rotate left/right/up/down
	var rotation_matrix = new THREE.Matrix4().identity();
	if ( keyboard.pressed("A") )//Rotation en y
		currentMesh.rotateOnAxis( new THREE.Vector3(0,1,0), rotateAngle);
	if ( keyboard.pressed("E") )//Rotation en -y
		currentMesh.rotateOnAxis( new THREE.Vector3(0,1,0), -rotateAngle);
	if ( keyboard.pressed("W") )//Rotation en x
		currentMesh.rotateOnAxis( new THREE.Vector3(1,0,0), rotateAngle);
	if ( keyboard.pressed("C") )//Rotation en -x
		currentMesh.rotateOnAxis( new THREE.Vector3(1,0,0), -rotateAngle);
	if ( keyboard.pressed("W") )//Rotation en z
		currentMesh.rotateOnAxis( new THREE.Vector3(0,0,1), rotateAngle);
	if ( keyboard.pressed("R") )//Rotation en -z
		currentMesh.rotateOnAxis( new THREE.Vector3(0,0,1), -rotateAngle);
	if ( keyboard.pressed("F") )
	{
		currentMesh.position.set(0,25.1,0);
		currentMesh.rotation.set(0,0,0);
	}
	
	// camera motion
	if ( keyboard.pressed("up") )
		camera.position.x -= moveDistance*2;
	if ( keyboard.pressed("down") )
		camera.position.x += moveDistance*2;
	if ( keyboard.pressed("left") )
		camera.position.z -= moveDistance*2;
	if ( keyboard.pressed("right") )
		camera.position.z += moveDistance*2;
	controls.update();
}



