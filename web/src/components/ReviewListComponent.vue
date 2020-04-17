<template>
  <b-container>
    <b-row>
      <b-col class="mb-3" cols=12 md=4 v-for="review in reviews" :key=review.id>
        <b-card :img-src="review.clothes_set.image_url" img-top img-height="300">
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
  }
}
</script>

<style>

</style>
