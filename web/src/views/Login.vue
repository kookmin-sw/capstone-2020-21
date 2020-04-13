<template>
  <div class="login">
    <Login/>
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/LoginComponent.vue'

export default {
  name: 'login',
  components: {
    Login
  }
}
</script>
