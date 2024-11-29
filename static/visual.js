import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'

// Variables for the balls and gravity
let balls = [];
let gravity = -5;  // Gravity effect on the balls (negative for downward acceleration)
let bounceFactor = 0.8;  // How much the balls bounce back after hitting the plane
let ballHeight = 20000;  // Balls' initial height above the plane
let ballSpeed = 0;  // Speed for bounce

// Set up the canvas and scene
const canvas = document.getElementById('canvas')
const background = "#002135"
const meshColor = "#0b3233"
const old_amplitudes = [-3.72162238e-02]
const splits = 5
let amplitudes = window.amplitudes

for(let i = 0; i < old_amplitudes.length; i+= splits){
  amplitudes.push(old_amplitudes[i])
}
//console.log(amplitudes.length)
//console.log(old_amplitudes.length)
var camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 400000)
camera.position.z = 10000;
camera.position.y = 10000;

var scene = new THREE.Scene();
scene.fog = new THREE.Fog(background, 1, 300000);

const planeSize = 1245000;
const planeDefinition = 100;

var planeGeo = new THREE.PlaneGeometry(planeSize, planeSize, planeDefinition, planeDefinition);
var plane = new THREE.Mesh(planeGeo, new THREE.MeshStandardMaterial({
  color: meshColor,
  wireframe: true,
  roughness:0
}));

plane.rotation.x -= Math.PI * 0.5;
scene.add(plane);

var renderer = new THREE.WebGLRenderer({alpha: false, canvas: canvas});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(background, 1);

updatePlane();

// Function to update the plane's geometry (wave effect)
function updatePlane() {
  const position = planeGeo.attributes.position;
  const count = position.count;

  if (!planeGeo.userData._myZ) {
    planeGeo.userData._myZ = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      const z = Math.random() * 1000 - 500;
      planeGeo.userData._myZ[i] = z;
      position.array[i * 3 + 2] = z;
    }
  }
  position.needsUpdate = true;
}

// Function to create a ball with random starting position
function createBall() {
  const ballGeometry = new THREE.SphereGeometry(1400, 32, 32);
  const ballMaterial = new THREE.MeshStandardMaterial({ color: Math.random() * 0xffffff });
  let ball = new THREE.Mesh(ballGeometry, ballMaterial);
  ball.position.set(Math.random() * 1000000 - 500000, ballHeight, Math.random() * 1000000 - 1000000);  // Random position
  scene.add(ball);
  return {
    mesh: ball,
    velocity: 0  // Initial velocity
  };
}

// Create multiple balls
for (let i = 0; i < 2000; i++) {
  balls.push(createBall());
}

// Add light to the scene
const light = new THREE.HemisphereLight(0xffffbb, 0x080820, 12);
scene.add(light);

let lastLogTime = 0;
let amplitude = 15;
let amplitude_number = 0
let count = 0; // Frame-based counter
let amplitude_tick = 0
function render() {
  requestAnimationFrame(render);

  const position = planeGeo.attributes.position;
  const _myZ = planeGeo.userData._myZ;
  const countVertices = position.count;

  // Update the plane geometry with wave movement
  for (let i = 0; i < countVertices; i++) {
    position.array[i * 3 + 2] =
      Math.sin(i * 0.2 + count * 0.05) * (_myZ[i] * amplitude);
  }

  const currentTime = performance.now();
  if (currentTime - lastLogTime >= 31.3335561497*splits) {
  //   let average_amplitude = 0
  //   if (amplitude_number > 20){
  //   for(let i = 1; i < 21;i++){
  //     average_amplitude += amplitudes[amplitude_number-i]
  //   average_amplitude/20
  //   }
  // }
    if(amplitude_number>0){
    amplitude_tick = ((amplitudes[amplitude_number] - amplitudes[amplitude_number-1]) * 0.03191466666) * 100
    lastLogTime = currentTime;
    //console.log(amplitude_tick)
    }
    amplitude_number++;

  }
  amplitude += amplitude_tick
  position.needsUpdate = true;

  // Update camera for circular motion
  const x = camera.position.x;
  const z = camera.position.z;
  // camera.position.x = x * Math.cos(0.001) + z * Math.sin(0.001) - 10;
  // camera.position.z = z * Math.cos(0.001) - x * Math.sin(0.001) - 10;
  camera.lookAt(new THREE.Vector3(0, 8000, 0));

  // Update each ball's position with gravity
  balls.forEach(ball => {
    ball.velocity += gravity;  // Apply gravity to the ball (downward force)
    ball.mesh.position.y += ball.velocity;  // Update ball's vertical position

    // Collision detection with the wavy plane
    const planeZAtBall = getPlaneHeightAt(ball.mesh.position.x, ball.mesh.position.z);
    if (ball.mesh.position.y <= planeZAtBall + ball.mesh.geometry.parameters.radius) {
      // Ball hits the plane: apply bounce
      ball.mesh.position.y = planeZAtBall + ball.mesh.geometry.parameters.radius;  // Reset ball's height to plane level
      ball.velocity *= -bounceFactor;  // Reverse velocity and apply bounce effect (dampen the bounce)
    }
  });

  count += 1;
  renderer.render(scene, camera);
}

// Get the plane's height at the ball's x and z position
function getPlaneHeightAt(x, z) {
  const position = planeGeo.attributes.position;
  const gridSize = planeDefinition + 1;
  const i = Math.floor((x + planeSize / 2) / (planeSize / gridSize));
  const j = Math.floor((z + planeSize / 2) / (planeSize / gridSize));
  const index = (i + j * gridSize) * 3 + 2; // Get the Z value at the (i, j) vertex
  return position.array[index];
}

window.addEventListener('resize', onWindowResize, false);

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

render();