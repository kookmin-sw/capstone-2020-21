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
      <b-col class="mb-2 mt-2" cols=12 md=6 lg=4 v-for="review in reviews" :key=review.id>
        <b-card :img-src="review.clothes_set.image_url" img-top img-height="250px">
          <b-card-title>
            {{ review.clothes_set.name }}
          </b-card-title>
          <b-card-body>
            <b-button pill size="sm" variant="info">{{ review.clothes_set.style }}</b-button>
          </b-card-body>
          <b-card-body>
            {{ convertDate(review.start_datetime) }} ~ {{ convertDate(review.end_datetime) }}
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
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
