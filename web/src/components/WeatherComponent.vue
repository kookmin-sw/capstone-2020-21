<template>
  <b-container>
    <b-row>
      <b-col>
        <h5 style="word-break: keep-all">
          위치 : {{ weatherData.location.name }}
        </h5>
        <b-button class="mb-3" variant="info" size="sm" @click="openLocationModal">
          <b-icon-arrow-clockwise/> 바꾸기
        </b-button>
      </b-col>
    </b-row>
    <b-row cols=12 align-h="center" align-v="center" align-content="center">
      <b-col class="h5 text-md-right" cols=12 md=6>
        <b-img src="../assets/hot.png" width="30px"></b-img>
        {{ weatherData.maxTemp }} / {{ weatherData.maxSenseTemp }} °C
      </b-col>
      <b-col class="h5 text-md-left" cols=12 md=6>
        <b-img src="../assets/cold.png" width="30px"></b-img>
        {{ weatherData.minTemp }} / {{ weatherData.minSenseTemp }} °C
      </b-col>
      <b-col class="h5" cols=12 md=3 lg=2>
        <b-img src="../assets/humidity.png" width="30px"></b-img>
        {{ weatherData.humidity }} %
      </b-col>
      <b-col class="h5" cols=12 md=3 lg=2>
        <b-img src="../assets/wind.png" width="30px"></b-img>
        {{ weatherData.windSpeed }} m/s
      </b-col>
      <b-col class="h5" cols=12 md=3 lg=2>
        <b-img src="../assets/rain.png" width="30px"></b-img>
        {{ weatherData.precipitation }} mm
      </b-col>
    </b-row>
    <b-modal ref="location-modal" title="위치 검색" ok-title="확인" cancel-title="취소">
      <b-container>
        <b-row class="mb-3" no-gutters>
          <b-col cols=10>
            <b-input v-model="keyword" type="search" placeholder="도/시를 입력해주세요"/>
          </b-col>
          <b-col cols=2>
            <b-button @click="handleLocationSearch">
              <b-icon-search/>
            </b-button>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-list-group>
              <b-list-group-item
                class="w-100"
                href="#"
                v-for="location of locations"
                :key="location.id"
                @click="handleLocationClick($event, location)">
                {{ location.location }}
              </b-list-group-item>
            </b-list-group>
          </b-col>
        </b-row>
      </b-container>
    </b-modal>
  </b-container>
</template>

<script>
import axios from 'axios'
import { BIconArrowClockwise, BIconSearch } from 'bootstrap-vue'
import consts from '@/consts.js'

export default {
  components: {
    BIconArrowClockwise,
    BIconSearch
  },
  props: [
    'weatherData'
  ],
  data: function () {
    return {
      'locations': [],
      'keyword': ''
    }
  },
  methods: {
    openLocationModal: function () {
      // TODO(mskwon1): implement this.
      this.$refs['location-modal'].show()
    },
    handleLocationClick: function (event, location) {
      this.weatherData.location.id = location.id
      this.weatherData.location.name = location.location

      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      this.fetchCurrentWeather(config)

      this.$refs['location-modal'].hide()
    },
    handleLocationSearch: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var vm = this
      var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/location_search/'
      url += '?search=' + vm.keyword
      axios.get(url, config)
        .then((response) => {
          vm.locations = response.data.results
        })
    },
    fetchCurrentWeather: function (config) {
      var vm = this
      var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/current_weather/'
      url += '?location=' + this.weatherData.location.id

      axios.get(url, config)
        .then((response) => {
          const {
            min_temperature,
            max_temperature,
            max_chill_temp,
            min_chill_temp,
            humidity,
            wind_speed,
            precipitation
          } = response.data

          vm.weatherData.minTemp = min_temperature
          vm.weatherData.maxTemp = max_temperature
          vm.weatherData.maxSenseTemp = max_chill_temp.toFixed(1)
          vm.weatherData.minSenseTemp = min_chill_temp.toFixed(1)
          vm.weatherData.humidity = humidity
          vm.weatherData.windSpeed = wind_speed
          vm.weatherData.precipitation = precipitation
        })
    }
  },
  created: function () {
    var token = window.localStorage.getItem('token')
    var config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    this.fetchCurrentWeather(config)
  }
}
</script>
