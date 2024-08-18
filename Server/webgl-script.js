const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 조명 추가
const light = new THREE.HemisphereLight(0xffffff, 0x444444);
light.position.set(0, 200, 0);
scene.add(light);

// COLLADA 파일 로드
const loader = new THREE.ColladaLoader();
loader.load('model.dae', function (collada) {
  scene.add(collada.scene);
  renderer.render(scene, camera);
}, undefined, function (error) {
  console.error(error);
});

camera.position.z = 5;

// 애니메이션 루프
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

animate();