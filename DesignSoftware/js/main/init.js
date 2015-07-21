console.log("init.js amorced")
    // MAIN
    // standard global variables
var container, stats;
var camera, controls, scene, renderer;
var objects = [],
    plane;
var workingZone;

var GRIDSIZE = 5000;
var limitScale;

var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2(),
    offset = new THREE.Vector3(),
    INTERSECTED, SELECTED;

var clock = new THREE.Clock();

// Basic wireframe materials.
var darkMaterial = new THREE.MeshBasicMaterial( { color: 0x000088 } );
var wireframeMaterial = new THREE.MeshBasicMaterial( { color: 0x00ee00, wireframe: true, transparent: true } ); 
var multiMaterial = [ darkMaterial, wireframeMaterial ]; 

var gui = new dat.GUI();
var gui2 = new dat.GUI();
var currentMesh;
console.log("global variables ok")


init();
console.log("init done");
animate();


function init() {

	scene = new THREE.Scene();

    container = document.createElement('div');
    document.body.appendChild(container);

	var SCREEN_WIDTH = window.innerWidth, SCREEN_HEIGHT = window.innerHeight;
	var VIEW_ANGLE = 45, ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT, NEAR = 0.1, FAR = 20000;
	camera = new THREE.PerspectiveCamera( VIEW_ANGLE, ASPECT, NEAR, FAR);
	scene.add(camera);
	camera.position.set(500,1000,500);
	camera.lookAt(scene.position);
    console.log("camera ok");

    

    scene.add(new THREE.AmbientLight(0x505050));

    var light = new THREE.SpotLight(0xffffff, 1.5);
    light.position.set(0, 500, 2000);
    light.castShadow = true;

    light.shadowCameraNear = 200;
    light.shadowCameraFar = camera.far;
    light.shadowCameraFov = 50;

    light.shadowBias = -0.00022;
    light.shadowDarkness = 0.5;

    light.shadowMapWidth = 2048;
    light.shadowMapHeight = 2048;

    scene.add(light);
    console.log("light ok");

    //GLOBAL GRID
    var step = 50;
	var geometry = new THREE.Geometry();
	var material = new THREE.LineBasicMaterial( { color: 0x000000, opacity: 0.2, transparent: true } );
	var line = new THREE.Line( geometry, material, THREE.LinePieces );
	for ( var i = - GRIDSIZE; i <= GRIDSIZE; i += step ) {
		geometry.vertices.push( new THREE.Vector3( - GRIDSIZE, 0, i ) );
		geometry.vertices.push( new THREE.Vector3(   GRIDSIZE, 0, i ) );
		geometry.vertices.push( new THREE.Vector3( i, 0, - GRIDSIZE ) );
		geometry.vertices.push( new THREE.Vector3( i, 0,   GRIDSIZE ) );
	}
	scene.add( line );
	console.log("grid ok");

	//MAIN GRID
	workingZone = new THREE.Mesh(new THREE.PlaneGeometry(1000,1000), new THREE.MeshBasicMaterial( {color: 0xAFEEEE, opacity:0.1}));
	workingZone.rotation.x = -Math.PI/2;
		workingZone.position.y =-1;
	scene.add(workingZone);

	createShape("cube",50,25,25);
	createShape("sphere",50,100,200);
	createShape("cylinder",50,-100,200);
	currentMesh = objects[0];
	
    plane = new THREE.Mesh(
        new THREE.PlaneBufferGeometry(5000, 5000),
        new THREE.MeshBasicMaterial({
            color: 0x000000,
            opacity: 0.25,
            transparent: true
        })
    );
    plane.rotation.x = -Math.PI/2;
    plane.visible = false;
    scene.add(plane);
    console.log("plane ok");

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
    console.log("renderer ok");

    controls = new THREE.OrbitControls( camera, renderer.domElement );
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.3;
    console.log("controls ok");

    //GLOBAL AXES
	var axes = new THREE.AxisHelper(500);
	scene.add(axes);
	console.log("axes ok");

    renderer.domElement.addEventListener('mousemove', onDocumentMouseMove, false);
    renderer.domElement.addEventListener('mousedown', onDocumentMouseDown, false);
    renderer.domElement.addEventListener('mouseup', onDocumentMouseUp, false);
    document.addEventListener('keydown', onDocumentKeyDown, false );

    console.log("mouseListeners ok");
    
    window.addEventListener('resize', onWindowResize, false);
    initGui();
    initGuiShape();
    console.log("gui interface ok");


}

