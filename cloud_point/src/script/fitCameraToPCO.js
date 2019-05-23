import * as THREE from 'three';

const defaultOffset = 1.25;

export function fitCameraToPCO(scene, camera, pco, offset = defaultOffset, controls) {
  const boundingBox = pco.pcoGeometry.tightBoundingBox;
  const center = boundingBox.getCenter();
  const size = boundingBox.getSize();
  const maxDim = Math.max(size.x, size.y, size.z);

  const fov = camera.fov * (Math.PI / 180); // Degree2Radian
  let cameraZ = Math.abs(maxDim / 2 * Math.tan(fov * 2)); //Applied fifonik correction
  cameraZ *= offset; // zoom out a little so that pcos don't fill the screen

  scene.updateMatrixWorld(); // Update world positions
  var pcoWorldPosition = new THREE.Vector3();
  pcoWorldPosition.setFromMatrixPosition(pco.matrixWorld);

  const directionVector = camera.position.sub(pcoWorldPosition);
  const unitDirectionVector = directionVector.normalize();
  camera.position.copy(unitDirectionVector.multiplyScalar(cameraZ));
  camera.lookAt(pcoWorldPosition);

  const cameraToFarEdge = cameraZ - boundingBox.min.z;

  camera.far = cameraToFarEdge * 3;
  camera.updateProjectionMatrix();

  if (controls) {
	controls.target.set(center.x, center.y, 0);

	// prevent camera from zooming out far enough to create far plane cutoff
	controls.maxDistance = cameraToFarEdge * 2;

	controls.update();
  } else {
	camera.lookAt(center);
  }
}
