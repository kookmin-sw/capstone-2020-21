<template>
  <b-container>
    <b-alert id="alert" v-model="showAlert" variant="danger" dismissible style="word-break: keep-all">
      {{ alertMessage }}
    </b-alert>
    <b-overlay :show="isLoading">
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
      <b-row align-h="center">
        <b-form-datepicker v-if="isGlobal"
                            class="w-50 mb-3 text-center"
                            v-model="date"
                            locale="en-US"
                            size="sm"
                            placeholder="날짜 선택"
                            :min="minDate"
                            :max="maxDate"
                            right
                            :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
                            @input="fetchGlobalWeather()">
        </b-form-datepicker>
      </b-row>
      <b-row align-h="center">
        <b-button class="ml-1 mb-3" variant="success" size="sm" @click="toggleGlobal">
          <template v-if="isGlobal">
            국내날씨 보기
          </template>
          <template v-else>
            세계날씨 보기
          </template>
        </b-button>
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
    </b-overlay>
    <b-modal ref="location-modal" title="위치 검색" ok-title="확인" cancel-title="취소">
      <b-container>
        <b-alert id="locationModalAlert" v-model="showLocationModalAlert" variant="danger" dismissible style="word-break: keep-all">
          {{ locationModalAlertMessage }}
        </b-alert>
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
    <b-modal ref="global-modal" title="세계 위치 검색" ok-title="확인" cancel-title="취소">
      <b-container>
        <b-alert id="globalModalAlert" v-model="showGlobalModalAlert" variant="danger" dismissible style="word-break: keep-all">
          {{ globalModalAlertMessage }}
        </b-alert>
        <b-row class="mb-3" no-gutters>
          <b-col cols=10>
            <b-input v-model="keyword" type="search" placeholder="도시명을 입력해주세요"/>
          </b-col>
          <b-col cols=2>
            <b-button @click="handleGlobalSearch">
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
                @click="handleGlobalClick($event, location)">
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
      date: new Date().toISOString().split('T')[0],
      locations: [],
      keyword: '',
      isGlobal: false,
      locationModalAlertMessage: '',
      showLocationModalAlert: false,
      globalModalAlertMessage: '',
      showGlobalModalAlert: false,
      showAlert: false,
      alertMessage: '',
      isLoading: false
    }
  },
  computed: {
    minDate: function () {
      return new Date().toISOString().split('T')[0]
    },
    maxDate: function () {
      var max = new Date()
      max.setDate(max.getDate() + 15)
      return max.toISOString().split('T')[0]
    }
  },
  methods: {
    openLocationModal: function () {
      if (this.isGlobal) {
        this.$refs['global-modal'].show()
      } else {
        this.$refs['location-modal'].show()
      }
    },
    handleGlobalClick: function (event, location) {
      this.weatherData.location.id = location.id
      this.weatherData.location.name = location.location

      this.fetchGlobalWeather()

      this.locations = []
      this.keyword = ''
      this.$refs['global-modal'].hide()
    },
    handleGlobalSearch: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var vm = this
      var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/global_search/'
      url += '?search=' + vm.keyword
      axios.get(url, config)
        .then((response) => {
          vm.locations = response.data.results
        })
        .catch((ex) => {
          vm.showGlobalModalAlert = true
          vm.globalModalAlertMessage = '검색결과를 받아오는데 실패했습니다. 오류가 계속 될 경우 관리자에게 알려주세요.'
        })
    },
    handleLocationClick: function (event, location) {
      this.weatherData.location.id = location.id
      this.weatherData.location.name = location.location

      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      this.fetchCurrentWeather(config)

      this.locations = []
      this.keyword = ''
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
        .catch((ex) => {
          vm.showLocationModalAlert = true
          vm.locationModalAlertMessage = '검색결과를 받아오는데 실패했습니다. 오류가 계속 될 경우 관리자에게 알려주세요.'
        })
    },
    fetchCurrentWeather: function (config) {
      var vm = this
      var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/current_weather/'
      url += '?location=' + this.weatherData.location.id
      this.isLoading = true

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
          this.isLoading = false
        })
        .catch((ex) => {
          this.showAlert = true
          this.alertMessage = '날씨정보를 받아오는데 실패했습니다. 오류가 계속 될 경우 관리자에게 알려주세요.'
          this.isLoading = false
        })
    },
    fetchGlobalWeather: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      var vm = this
      var url = consts.SERVER_BASE_URL + '/clothes-set-reviews/global_weather/'
      url += '?city_name=' + this.weatherData.location.name
      url += '&date=' + this.date
      this.isLoading = true

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
          vm.weatherData.windSpeed = wind_speed.toFixed(1)
          vm.weatherData.precipitation = precipitation.toFixed(1)
          this.isLoading = false
        })
        .catch((ex) => {
          this.showAlert = true
          this.alertMessage = '날씨정보를 받아오는데 실패했습니다. 오류가 계속 될 경우 관리자에게 알려주세요.'
          this.isLoading = false
        })
    },
    toggleGlobal: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      if (this.isGlobal) {
        this.isGlobal = false
        this.weatherData.location.id = '0'
        this.weatherData.location.name = '서울특별시'
        this.fetchCurrentWeather(config)
      } else {
        this.isGlobal = true
        this.weatherData.location.id = '1689973'
        this.weatherData.location.name = 'San Francisco'
        this.fetchGlobalWeather()
      }
    }
  },
  mounted: function () {
    var token = window.localStorage.getItem('token')
    var config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    this.fetchCurrentWeather(config)
  }
}
</script>
