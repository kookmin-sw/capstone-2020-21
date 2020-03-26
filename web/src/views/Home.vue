<template>
  <div class="Home">
    <link href="vendor/fontawesome-free/css/all.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,300italic,400italic,700italic" rel="stylesheet" type="text/css">
    <HomeNavigation></HomeNavigation>
    <HomeComponent></HomeComponent>
    <Footer></Footer>
    <!-- <Home msg="This is Home page"/> -->
  </div>
</template>

<script>
import HomeComponent from '@/components/HomeComponent.vue'
import HomeNavigation from '@/components/HomeNavigation.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'Home',
  components: {
    HomeComponent,
    HomeNavigation,
    Footer
  }
}
</script>
