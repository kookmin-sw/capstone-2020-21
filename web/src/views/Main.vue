<template>
  <b-container>
    <b-row>
      <b-col>
        <!-- 날씨 컴포넌트 -->
        <WeatherComponent />
      </b-col>
    </b-row>
    <b-row cols=1 cols-md=2>
      <b-col cols=12 cols-md=4>
        <!-- 추천 카테고리 컴포넌트 -->
        <RecommendedCategoriesComponent />
      </b-col>
      <b-col cols=12 cols-md=8>
        <!-- 리뷰 컴포넌트 -->
        <ReviewListComponent :reviews="userReviews"
                              :maxTemp="weatherProps.maxTemp"
                              :minTemp="weatherProps.minTemp" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import WeatherComponent from '@/components/WeatherComponent'
import RecommendedCategoriesComponent from '@/components/RecommendedCategoriesComponent'
import ReviewListComponent from '@/components/ReviewListComponent'

export default {
  name: 'main',
  components: {
    WeatherComponent,
    RecommendedCategoriesComponent,
    ReviewListComponent
  },
  data: function () {
    return {
      weatherProps: {
        minTemp: 4,
        maxTemp: 22,
        location: 0
      },
      recommendedCategories: [],
      userClothes: [],
      userReviews: []
    }
  },
  created: function () {
    var token = window.localStorage.getItem('token')
    var config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    var vm = this
    axios.get(`${consts.SERVER_BASE_URL}/clothes-set-reviews/?limit=10&max_sensible_temp=${vm.weatherProps.maxTemp}&min_sensible_temp=${vm.weatherProps.minTemp}`, config)
      .then((response) => {
        vm.userReviews = response.data.results
      })
  }
}
</script>

<style>

</style>
