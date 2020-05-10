<template>
  <b-container>
    <b-row v-if="isBlankList">
      <b-col class="mb-2" cols=12>
        <b-card img-src="https://bit.ly/3a3Fff0" img-top img-fluid>
          <b-card-title>
            리뷰를 등록해주세요
          </b-card-title>
          <b-card-body>
            등록된 리뷰가 없습니다. 등록해주세요!
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
    <b-row v-else>
      <b-col class="mb-2 mt-2" cols=12 md=6 v-for="review in reviews" :key=review.id>
        <ClothesSetReviewCard :review="review" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ClothesSetReviewCard from '@/components/cards/ClothesSetReviewCard.vue'
export default {
  components: {
    ClothesSetReviewCard
  },
  props: [
    'reviews',
    'includeFilters'
  ],
  methods: {
    convertDate: function (targetDate) {
      return new Date(targetDate).toLocaleDateString()
    }
  },
  computed: {
    isBlankList: function () {
      return this.reviews.length === 0
    }
  }
}
</script>

<style>

</style>
