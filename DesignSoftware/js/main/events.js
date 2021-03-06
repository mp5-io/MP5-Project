function onDocumentMouseMove(event) {

    event.preventDefault();

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    //

    raycaster.setFromCamera(mouse, camera);

    if (SELECTED) {
        var intersects = raycaster.intersectObject(plane);
        SELECTED.position.copy(intersects[0].point.sub(offset));
        return;

    }

    var intersects = raycaster.intersectObjects(objects);

    if (intersects.length > 0) { //If we hover over an object

        if (INTERSECTED != intersects[0].object) { //If this object is different from my previous focus

            INTERSECTED = intersects[0].object;//My current focus becomes this one
            INTERSECTED.originalHex = INTERSECTED.material.color.getHex();//We save its previous color
            plane.position.copy(INTERSECTED.position);//We move our plane
            //plane.lookAt(camera.position);

        }
        container.style.cursor = 'pointer';

    } else{
    	if(INTERSECTED)
    		INTERSECTED.material.color.setHex(INTERSECTED.originalHex);
    	INTERSECTED = null;
    	container.style.cursor = 'auto';
    }
}

function onDocumentMouseDown(event) {

    event.preventDefault();
    var vector = new THREE.Vector3(mouse.x, mouse.y, 0.5).unproject(camera);
    var raycaster = new THREE.Raycaster(camera.position, vector.sub(camera.position).normalize());
    var intersects = raycaster.intersectObjects(objects);
    switch ( event.button ) {
    case 0: // left 
    if (intersects.length > 0) {//If you have hover over an object and click on it

        controls.enabled = false;
        SELECTED = intersects[0].object; //SELECTED becomes this object



    	// restore previous intersection object (if it exists) to its original color
		if ( SELECTED ) 
			SELECTED.material.color.setHex( INTERSECTED.currentHex );
		// store reference to closest object as current intersection object
		SELECTED = intersects[0].object;
		// store color of closest object (for later restoration)
		SELECTED.currentHex = INTERSECTED.material.color.getHex();
		// set a new color for closest object
		SELECTED.material.color.setHex( 0xffff00 );

        
        //Reaffectation of GUI
		currentMesh= SELECTED;
		parameters.selected_mesh = INTERSECTED.name;

		document.getElementById('info').innerHTML = "Current focus : " +INTERSECTED.name;

        var intersects = raycaster.intersectObject(plane);
        offset.copy(intersects[0].point).sub(plane.position);

        container.style.cursor = 'move';

    }
        break;
    case 1: // middle
        break;
    case 2: // right
    if(INTERSECTED){
    	document.getElementById('info').innerHTML = "deselection";
    	SELECTED =null;
	    //currentMesh = null;
	}
	controls.enabled = true;
        break;
	}

    

}

function onDocumentMouseUp(event) {
	    //console.log(Math.floor(currentMesh.position.x/50));
    event.preventDefault();
    controls.enabled = true;

    if(INTERSECTED){
		currentMesh.position.x = Math.floor(currentMesh.position.x/25)*25;
		currentMesh.position.z = Math.floor(currentMesh.position.z/25)*25;
		reajustPosition(currentMesh);
    }
    
    container.style.cursor = 'auto';

}

function onDocumentKeyDown(event){
	switch( event.keyCode ) {

		/* Translations */
		case 107: translate(0,1,0);break; //stands for '+'  y+=1
		case 109: translate(0,-1,0);break; //stands for '-' y-=1
		case 100: translate(-1,0,0);break; //stands for '4' x-=1
		case 102: translate(1,0,0);break; //stands for '6'  x+=1
		case 104: translate(0,0,-1);break; //stands for '8' z-=1
		case 98: translate(0,0,1);break; //stands for '2'   z+=1

		case 101: resetCube();break; //stands for '2'

		/* Rotations */
		case 103: currentMesh.rotation.y += (de2ra(45));break; //rotation on y axis
		case 105: currentMesh.rotation.y -= (de2ra(45));break; //reverse rotation on y axis
		case 97: currentMesh.rotation.z += (de2ra(45));break; //rotation on y axis
		case 99: currentMesh.rotation.z -= (de2ra(45));break; //reverse rotation on y axis	

	}
}