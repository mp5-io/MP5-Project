    plane = new THREE.Mesh(
        new THREE.PlaneBufferGeometry(2000, 2000, 8, 8),
        new THREE.MeshBasicMaterial({
            color: 0x000000,
            opacity: 0.25,
            transparent: true
        })
    );
    plane.rotation.x = -Math.PI/2;
    plane.visible = true;
    scene.add(plane);





    renderer = new THREE.WebGLRenderer({
        antialias: true
    });
    renderer.setClearColor(0xf0f0f0);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.sortObjects = false;

    renderer.shadowMapEnabled = true;
    renderer.shadowMapType = THREE.PCFShadowMap;


    container.appendChild(renderer.domElement);


    renderer.domElement.addEventListener('mousemove', onDocumentMouseMove, false);
    renderer.domElement.addEventListener('mousedown', onDocumentMouseDown, false);
    renderer.domElement.addEventListener('mouseup', onDocumentMouseUp, false);