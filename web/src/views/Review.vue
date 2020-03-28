<template>
  <div class="review">
    <ReviewComponent/>
  </div>
</template>

<script>
// @ is an alias to /src
import ReviewComponent from '@/components/ReviewComponent.vue'

export default {
  name: 'review',
  components: {
    ReviewComponent
  }
}
</script>
