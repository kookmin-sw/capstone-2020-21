<template>
  <div class="login">
    <HomeNavigation/>
    <Login/>
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/LoginComponent.vue'
import HomeNavigation from '@/components/HomeNavigation.vue'

export default {
  name: 'login',
  components: {
    Login,
    HomeNavigation
  }
}
</script>
