<template>
  <div id="target" :style="{ height: '-webkit-fill-available' }">
  </div>
</template>

<script>
import * as THREE from 'three';
import * as threePotree from '@pix4d/three-potree-loader';

import { OrbitControls } from '../script/orbitControls';
import { fitCameraToPCO } from '../script/fitCameraToPCO';

export default {
    data() {
      return {
        serverConfig: {
            cloudjs: 'cloud.js',
            makeURL(path) {
              return `http://localhost:8000/resources/pointclouds/pontto/${path}`;
            },
        },
        targetID: 'target',
        renderer: new THREE.WebGLRenderer(),
        potree: new threePotree.Potree(),
        pco: null,
        camera: new THREE.PerspectiveCamera(50, NaN, 0.001, 100000),
        scene: new THREE.Scene(),
        gridSize: 2000,
        pointColorSelect: 3,
        pointShapeSelect: 2,
        pointSizeSelect: 0,
        materialSize: 1,
      }
    },
    mounted() {
        this.loadPOC()
    },
    methods: {
        loadPOC() {
            const el = document.getElementById(this.targetID);

            this.renderer.setClearColor(0xffffff);
            
            const orbitControls = new OrbitControls(this.camera, el);
            orbitControls.mouseButtons = {
                ORBIT: THREE.MOUSE.LEFT,
                ZOOM: THREE.MOUSE.MIDDLE,
                PAN: THREE.MOUSE.RIGHT,
            };
            orbitControls.panningMode = OrbitControls.HorizontalPanning;

            this.updateSize(el);
            
            window.addEventListener('resize', () => {
                this.updateSize(el);
            });

            el.appendChild(this.renderer.domElement);

            this.potree.loadPointCloud(this.serverConfig.cloudjs, this.serverConfig.makeURL).then(pco => {
                this.pco = pco
                this.pco.position.set(0, 0, 0);
                this.pco.material.size = this.materialSize;
                this.pco.material.pointColorType = this.pointColorSelect;
                this.pco.material.pointShapeType = this.pointShapeSelect;
                this.pco.material.pointSizeType = this.pointSizeSelect;
                this.pco.updateMatrixWorld(true);

                this.camera.position.set(50, 50, 50);
                this.camera.up = new THREE.Vector3(0, 0, 1);
                fitCameraToPCO(this.scene, this.camera, this.pco, 0.5, orbitControls);
                this.addGrid();

                this.scene.add(this.pco);

                requestAnimationFrame(this.initRender);
            })
            .catch((err) => {
                window.console.error(err);
            });
        },
        initRender() {
            requestAnimationFrame(this.initRender);
            this.potree.updatePointClouds([this.pco], this.camera, this.renderer);
            this.renderer.clear();
            this.renderer.render(this.scene, this.camera);

        },
        addGrid() {
            const gridXZ = new THREE.GridHelper(this.gridSize, 100, 0xEED5B7, 0xEED5B7);
            gridXZ.position.set(this.gridSize / 2, 0, this.gridSize / 2);
            this.scene.add(gridXZ);

            const gridXY = new THREE.GridHelper(this.gridSize, 100, 0xEED5B7, 0xEED5B7);
            gridXY.position.set(this.gridSize / 2, this.gridSize / 2, 0);
            gridXY.rotation.x = Math.PI/2;
            this.scene.add(gridXY);

            const gridYZ = new THREE.GridHelper(this.gridSize, 100, 0xEED5B7, 0xEED5B7);
            gridYZ.position.set(0, this.gridSize / 2, this.gridSize / 2);
            gridYZ.rotation.z = Math.PI/2;
            this.scene.add(gridYZ);
        },
        updateSize(el) {
            const { width, height } = el.getBoundingClientRect();
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(width, height);
        }
    }
}
</script>

<style scoped>
</style>
