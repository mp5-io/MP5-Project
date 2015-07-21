
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

    if (intersects.length > 0) {
        if (INTERSECTED != intersects[0].object) {

            INTERSECTED = intersects[0].object;
            INTERSECTED.currentHex = INTERSECTED.material.color.getHex();
            plane.position.copy(INTERSECTED.position);
            plane.lookAt(camera.position);

        }

        container.style.cursor = 'pointer';

    } else{
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
    if (intersects.length > 0) {

        controls.enabled = false;
        SELECTED = intersects[0].object;

                //Switch to another object, set the old color to the old object
        if(INTERSECTED){
        	currentMesh.material.color.setHex(INTERSECTED.currentHex);
        }

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
	    INTERSECTED.material.color.setHex( INTERSECTED.currentHex );
	    INTERSECTED = null;	
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
		currentMesh.position.x = Math.floor(currentMesh.position.x/50)*50+25;
		currentMesh.position.z = Math.floor(currentMesh.position.z/50)*50+25;
		reajustPosition(currentMesh);
    }
    
    container.style.cursor = 'auto';

}
