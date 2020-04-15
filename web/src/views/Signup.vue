<template>
  <div class="signup">
    <Signup/>
  </div>
</template>

<script>
// @ is an alias to /src
import Signup from '@/components/SignupComponent.vue'
// import HomeNavigation from '@/components/HomeNavigation.vue'

export default {
  name: 'signup',
  components: {
    Signup
  }
}
</script>
