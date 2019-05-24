<template>
  <div id="app">
    <div class="toolbar" v-show="isToolBarShow">
      <input v-model="cloudjs" placeholder="点云源数据文件">
      <input v-model="url" placeholder="点云文件地址">
      <button :disabled="isButtonDisabled" @click="showCloudPoint()">确定</button>
    </div>
    <cloud-point v-if="isCloudPointShow" :cloudjs="cloudjs" :url="url"/>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      cloudjs: "",
      url: "",
      isCloudPointShow: false,
      isToolBarShow: true,
      isButtonDisabled: true
    }
  },
  components: {
    CloudPoint: () => 
              import ('./components/CloudPoint.vue')
  },
  methods: {
    showCloudPoint() {
      this.isCloudPointShow = true
      this.isToolBarShow = false 
    }
  },
  updated() {
    if (this.cloudjs != "" && this.url != "") {
      this.isButtonDisabled = false
    } else {
      this.isButtonDisabled = true
    }
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
