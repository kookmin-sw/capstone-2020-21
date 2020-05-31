<template>
  <b-container>
    <b-alert id="alert" v-model="showAlert" variant="danger" dismissible >
      {{ alertMessage }}
    </b-alert>
    <b-row cols=1>
      <b-col cols=12>
        <!-- 날씨 컴포넌트 -->
        <WeatherComponent class="border mb-3 p-3" :weatherData.sync="weatherProps" />
      </b-col>
    </b-row>
    <b-row cols=1 cols-md=2>
      <b-col cols=12 lg=4>
        <b-row>
          <b-col cols=12>
            <!-- 추천 카테고리 컴포넌트 -->
            <RecommendedCombinationsComponent class="border" :combinations="recommendedCombinations" />
          </b-col>
          <b-col cols=12 class="mt-3">
            <b-row>
              <b-col cols=12>
                <h4>최신 스타일</h4>
              </b-col>
              <b-col cols=12>
                <b-carousel controls indicators>
                  <b-carousel-slide
                    v-for="lookbook in lookbooks"
                    :key="lookbook.image"
                    :img-src="lookbook.image"
                    :caption-html="lookbook.brand + '<br><h5>' + lookbook.name + '</h5>'"
                    style="text-shadow: 0px 0px 4px #000">
                  </b-carousel-slide>
                </b-carousel>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
      <b-col class="mt-3 mt-lg-0" cols=12 lg=8>
        <b-row>
          <b-col cols=12>
            <!-- 리뷰 컴포넌트 -->
            <h4 class="mt-3 pb-0">유사한 날씨에 작성한 리뷰</h4>
            <ReviewListComponent :reviews="userReviews" />
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import WeatherComponent from '@/components/WeatherComponent'
import RecommendedCombinationsComponent from '@/components/RecommendedCombinationsComponent'
import ReviewListComponent from '@/components/ReviewListComponent'

export default {
  name: 'mainPage',
  components: {
    WeatherComponent,
    RecommendedCombinationsComponent,
    ReviewListComponent
  },
  data: function () {
    return {
      weatherProps: {
        minTemp: 0,
        maxTemp: 0,
        maxSenseTemp: 0,
        minSenseTemp: 0,
        location: {
          id: 0,
          name: '서울특별시'
        },
        humidity: 0,
        windSpeed: 0,
        precipitation: 0
      },
      recommendedCombinations: [],
      userReviews: [],
      showAlert: false,
      alertMessage: '',
      lookbooks: []
    }
  },
  watch: {
    weatherProps: {
      deep: true,
      handler () {
        var token = window.localStorage.getItem('token')
        var config = {
          headers: { Authorization: `Bearer ${token}` }
        }
        var vm = this
        var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/'
        url += '?maxTemp=' + vm.weatherProps.maxTemp
        url += '&minTemp=' + vm.weatherProps.minTemp
        url += '&windSpeed=' + vm.weatherProps.windSpeed
        url += '&humidity=' + vm.weatherProps.humidity
        url += '&me=true'

        axios.get(url, config)
          .then((response) => {
            vm.userReviews = response.data.results
          })
          .catch((ex) => {
            vm.showAlert = true
            vm.alertMessage = '리뷰를 받아오는데 실패했습니다. 오류가 계속되면 관리자에게 연락해주세요.'
          })

        url = consts.SERVER_BASE_URL + '/clothes/today_category/'
        url += '?maxTemp=' + vm.weatherProps.maxTemp
        url += '&minTemp=' + vm.weatherProps.minTemp
        url += '&windSpeed=' + vm.weatherProps.windSpeed
        url += '&humidity=' + vm.weatherProps.humidity

        axios.get(url, config)
          .then((response) => {
            vm.recommendedCombinations = response.data
          })
          .catch((response) => {
            vm.showAlert = true
            vm.alertMessage = '추천 카테고리를 받아오는데 실패했습니다. 오류가 계속되면 관리자에게 연락해주세요.'
          })
      }
    }
  },
  created: function () {
    var token = window.localStorage.getItem('token')
    var config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    var vm = this
    var url = consts.SERVER_BASE_URL + '/clothes/lookbook/'

    axios.get(url, config)
      .then((response) => {
        vm.lookbooks = response.data
      })
      .catch((ex) => {
        vm.showAlert = true
        vm.alertMessage = '룩북 데이터를 받아오는데 실패했습니다. 오류가 계속되면 관리자에게 연락해주세요.'
      })
  }
}
</script>

<style>

</style>
