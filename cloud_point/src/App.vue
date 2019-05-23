<template>
  <div id="app">
    <cloud-point/>
  </div>
</template>

<script>
import CloudPoint from './components/CloudPoint.vue'

export default {
  name: 'app',
  components: {
    CloudPoint
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: -webkit-fill-available;
}
</style>
