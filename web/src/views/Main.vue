<template>
  <b-container>
    <b-row cols=1>
      <b-col cols=12>
        <!-- 날씨 컴포넌트 -->
        <WeatherComponent class="border mb-3 p-3" :weatherData.sync="weatherProps" />
      </b-col>
    </b-row>
    <b-row cols=1 cols-md=2>
      <b-col cols=12 lg=4>
        <!-- 추천 카테고리 컴포넌트 -->
        <RecommendedCategoriesComponent class="border" :categories="recommendedCategories" />
      </b-col>
      <b-col class="mt-3 mt-lg-0" cols=12 lg=8>
        <!-- 리뷰 컴포넌트 -->
        <h4 class="mt-3 pb-0">유사한 날씨에 작성한 리뷰</h4>
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
  name: 'mainPage',
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
        location: {
          id: 0,
          name: '서울특별시'
        },
        humidity: 0,
        windSpeed: 0,
        precipitation: 0
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
    var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/'
    url += '?limit=10&max_sensible_temp=' + vm.weatherProps.maxTemp
    url += '&min_sensible_temp=' + vm.weatherProps.minTemp
    // TODO(mskwon1): decomment this after testing.
    // url += '&review=3'
    // url += '&me=true'

    axios.get(url, config)
      .then((response) => {
        vm.userReviews = response.data.results
      })

    url = consts.SERVER_BASE_URL + '/clothes/today_category/'
    url += '?max_sensible_temp=' + vm.weatherProps.maxTemp
    url += '&min_sensible_temp=' + vm.weatherProps.minTemp
    axios.get(url, config)
      .then((response) => {
        vm.recommendedCategories = response.data
      })

    // TODO(mskwon1) : implement current weather fetch code.
    // url = consts.SERVER_BASE_URL + '/clothes-set-reviews/current_weather/'
  }
}
</script>

<style>

</style>
