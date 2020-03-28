<template>
  <div class="review">
    <MainNavigation/>
    <div class="add_container">
        <b-button class="btn btn_xs" style="margin-right:10px" @click="goAdd()">새 리뷰 작성하기</b-button>
    </div>
    <div class="col">
        <ReviewComponent/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ReviewComponent from '@/components/ReviewComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'

export default {
  name: 'review',
  components: {
    ReviewComponent,
    MainNavigation
  }
}
</script>
