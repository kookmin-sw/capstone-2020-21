<template>
  <b-container>
    <b-row cols=1>
      <b-col cols=12>
        <ReviewComponent clothes_sets_id=60 :locationData.sync="locationProps"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ReviewComponent from '@/components/ReviewComponent.vue'
export default {
  name: 'review',
  components: {
    ReviewComponent
  },
  data: function () {
    return {
      locationProps: {
        location: {
          id: 0,
          name: '서울특별시'
        }
      }
    }
  }
}
</script>

<style>

</style>
