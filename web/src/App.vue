<template>
  <div id="app">
    <NavigationBar/>
    <router-view class="mt-3"/>
    <Footer/>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: {
    NavigationBar,
    Footer
  }
}
</script>

<style>
html, body {
  height: 100%;
}
a, button {
  outline: none;
}
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  background-color: white;
}
body{
  background:transparent !important;
}
</style>
