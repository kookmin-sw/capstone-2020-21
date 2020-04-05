<template>
  <div class="login">
    <MainNavigation/>
    <ReviewComponent/>
  </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'
import ReviewComponent from '@/components/ReviewComponent.vue'
export default {
  name: 'review',
  components: {
    MainNavigation,
    ReviewComponent
  }
}
</script>

<style>

</style>