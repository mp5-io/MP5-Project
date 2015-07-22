/*MAIN FILE*/

console.log("----------MAIN----------")
// standard global variables
var container, stats;
var camera, controls, scene, renderer;


var currentMesh;

var GRIDSIZE = 5000;
var workingZone;

var objects = [],
    plane;

var limitScale;

var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2(),
    offset = new THREE.Vector3(),
    INTERSECTED, SELECTED;

var gui = new dat.GUI();
var gui2 = new dat.GUI();

console.log("global variables ok");

// Basic wireframe materials.
var darkMaterial = new THREE.MeshBasicMaterial( { color: 0x000088 } );
var wireframeMaterial = new THREE.MeshBasicMaterial( { color: 0x00ee00, wireframe: true, transparent: true } ); 
var multiMaterial = [ darkMaterial, wireframeMaterial ]; 
console.log("materials ok");

	  //////////////////////////////
	 //   VARIABLES PARAMETRICS  //	
	//////////////////////////////

var xFuncText = "u^2 + sin(v)";
var xFunc = Parser.parse(xFuncText).toJSFunction( ['u','v'] );
var yFuncText = "u^2 + sin(v)";
var yFunc = Parser.parse(yFuncText).toJSFunction( ['u','v'] );
var zFuncText = "u^2 + sin(v)";
var zFunc = Parser.parse(zFuncText).toJSFunction( ['u','v'] );

// parameters for the equations
var a = 0.01, b = 0.01, c = 0.01, d = 0.01;

var meshFunction;
var segments = 20, 
	uMin = 0.01, uMax = 0.02, uRange = uMax - uMin,
	vMin = 0.01, vMax = 0.02, vRange = vMax - vMin,
	zMin = -10, zMax = 10, zRange = zMax - zMin;
	
var xMin = xMax = yMin = yMax = 0; // for autosizing window
	
var graphGeometry;
var gridMaterial, wireMaterial, vertexColorMaterial;
var graphMesh;



console.log("parametrics variables ok");
	  /////////////////////////
	 //  END  PARAMETRICS   //	
	/////////////////////////



console.log("--------INITIATION-------");
//START
init();
animate();
console.log("MyMiniDesigner successfully initiated");


$.ajax({
  type: "POST",
  url: "python/geometry.py",
}).done(function( coucou ) {
	console.log();
});


xFuncText = ("a*cos(u)*cos(v)*cos(alpha)-b*cos(u)*sin(v)*sin(alpha)+100");
yFuncText = ("b*cos(u)*sin(v)*cos(alpha)+a*cos(u)*cos(v)*sin(alpha)+100");
zFuncText = ("c*sin(v)+100");
uMin = (0); uMax = (6.28);
vMin = (0); vMax = (6.28);
a = 10;
b = 20;
c = 20;
alpha= 0;
segments = (20);//WARNING !!!! COMPLEXITY EXPLODE, set at 40

createGraph();
