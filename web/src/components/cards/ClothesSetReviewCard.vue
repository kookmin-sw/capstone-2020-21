<template>
  <b-overlay :show="isHovered" variant="dark" v-b-hover="handleHover">
    <b-card>
      <b-img :src="review.clothes_set.image_url" fluid style="height:10rem"/>
      <b-card-title>
        {{ review.clothes_set.name }}
      </b-card-title>
      <b-button pill variant="info">
        {{ review.clothes_set.style }}
      </b-button>
      <b-card-body>
        <!-- TODO(mskwon1): this should be component indicating review. -->
        <p class="mb-1 font-weight-bold">후기</p>
        <p class="m-auto w-75"><ReviewIndexComponent :index="review.review" /></p>
        <p class="mb-1 mt-1 font-weight-bold">한줄평</p>
        <p class="mb-0" style="word-break: keep-all">{{ review.comment }}</p>
      </b-card-body>
    </b-card>
    <template v-slot:overlay>
      <p class="text-light" style="word-break:keep-all">
        <!-- TODO(mskwon1): this should be stirng, not numeric. -->
        {{ review.location }}
        <br>
        {{ convertDate(review.start_datetime) }} ~ {{ convertDate(review.end_datetime) }}
      </p>
      <p class="text-light">
        <b-img src="@/assets/hot.png" width="30px" />
        {{ review.max_temp }} / {{ round(review.max_sensible_temp, 1) }} °C
      </p>
      <p class="text-light">
        <b-img src="@/assets/cold.png" width="30px" />
        {{ review.min_temp }} / {{ round(review.min_sensible_temp, 1) }} °C
      </p>
      <p class="text-light">
        <b-img src="@/assets/humidity.png" width="30px" />
        {{ round(review.humidity, 1) }} %
      </p>
      <p class="text-light">
        <b-img src="@/assets/wind.png" width="30px" />
        {{ round(review.wind_speed, 1) }} m/s
      </p>
      <p class="text-light">
        <b-img src="@/assets/rain.png" width="30px" />
        {{ round(review.precipitation, 1) }} mm
      </p>
    </template>
  </b-overlay>
</template>

<script>
import ReviewIndexComponent from '@/components/ReviewIndexComponent.vue'

export default {
  components: {
    ReviewIndexComponent
  },
  data: function () {
    return {
      isHovered: false
    }
  },
  props: [
    'review'
  ],
  methods: {
    handleClick: function () {
      // TODO(mskwon1): figure out where to redirect to.
    },
    handleHover: function (hovered) {
      this.isHovered = hovered
    },
    convertDate: function (targetDate) {
      return new Date(targetDate).toLocaleDateString()
    },
    round: function (num, to) {
      return num.toFixed(to)
    }
  }
}
</script>

<style>

</style>
