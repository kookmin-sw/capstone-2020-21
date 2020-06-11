<template>
<b-container>
  <b-row class="justify-content-center align-items-center">
    <b-col cols="12" md="7">
      <form id="review-form" class="form" action="" method="post">
        <b-alert id="SignupAlert" v-model="showAlert" variant="danger" dismissible style="word-break: keep-all">
          {{ alertMessage }}
        </b-alert>
        <h3 class="text-center text-top">리뷰   작성</h3>
        <b-img fluid :src="imageURL"/>
        <b-form-group label="활동장소 :" lable-for="input-1" class="text-left">
          <b-row id="input-1">
            <b-col md="auto" style="margin:0 auto">
              <h5 style="word-break: keep-all">
                위치 : {{ locationData.location.name }}
              </h5>
            </b-col>
            <b-col md="auto">
              <b-button class="mb-3" variant="info" size="sm" @click="openLocationModal">
                <b-icon-arrow-clockwise/> 바꾸기
              </b-button>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group label="활동시작시간 :" label-for="input-2" class="text-left text-top">
          <b-row id="input-2">
            <b-col md="auto" style="margin:0 auto">
              <b-form-datepicker :min="min" :max="max" v-model="form.start_date" locale="en-US"></b-form-datepicker>
            </b-col>
            <b-col md="auto" style="margin:0 auto">
              <b-form-timepicker v-model="form.start_time" locale="en"></b-form-timepicker>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group label="활동끝난시간 :" label-for="input-3" class="text-left text-top">
          <b-row id="input-3">
            <b-col md="auto" style="margin:0 auto">
              <b-form-datepicker :min="min" :max="max" v-model="form.end_date" locale="en-US"></b-form-datepicker>
            </b-col>
            <b-col md="auto" style="margin:0 auto">
              <b-form-timepicker v-model="form.end_time" locale="en"></b-form-timepicker>
            </b-col>
          </b-row>
        </b-form-group>
        <b-form-group label="만족도 :" label-for="input-4" class="text-left text-top">
          <b-form-input id="input-4" v-model="form.range" type="range" min="1" max="5"></b-form-input>
          <b-row>
            <b-col class="col-2 text-left">1</b-col>
            <b-col class="col-3 text-center">2</b-col>
            <b-col class="col-2 text-center">3</b-col>
            <b-col class="col-3 text-center">4</b-col>
            <b-col class="col-2 text-right">5</b-col>
          </b-row>
          <b-row>
            <b-col class="col-4 text-left">추웠다</b-col>
            <b-col class="col-4 text-center">적당했다</b-col>
            <b-col class="col-4 text-right">더웠다</b-col>
          </b-row>
        </b-form-group>
        <b-form-group label="한줄평 :" label-for="input-5" class="text-left text-top">
          <b-form-input id="input-5" v-model="form.comment"></b-form-input>
        </b-form-group>

        <b-modal ref="location-modal" title="위치 검색" ok-title="확인" cancel-title="취소">
          <b-container>
            <b-alert id="locationModalAlert" v-model="showLocationModalAlert" variant="danger" dismissible style="word-break: keep-all">
              {{ locationModalAlertMessage }}
            </b-alert>
            <b-row class="mb-3" no-gutters>
              <b-col cols="10">
                <b-input v-model="keyword" type="search" placeholder="도/시를 입력해주세요"/>
              </b-col>
              <b-col cols="2">
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
        <b-row>
          <b-col class="col-6" style="margin:0 auto">
              <b-button pill class="w-75" @click="submit">등록하기</b-button>
          </b-col>
        </b-row>
      </form>
    </b-col>
  </b-row>
</b-container>
</template>

<script>
import consts from '@/consts.js'
import axios from 'axios'
import { BIconArrowClockwise, BIconSearch } from 'bootstrap-vue'

export default {
  name: 'reviewcomponent',
  components: {
    BIconArrowClockwise,
    BIconSearch
  },
  data: function () {
    return {
      form: {
        start_date: '',
        end_date: '',
        start_time: '',
        end_time: '',
        comment: '',
        range: '3'
      },
      imageURL: '',
      'locations': [],
      'keyword': '',
      min: '',
      max: '',
      minlimit: '',
      showAlert: false,
      alertMessage: '',
      locationModalAlertMessage: '',
      showLocationModalAlert: false
    }
  },
  props: [
    'clothes_set_id',
    'locationData'
  ],
  methods: {
    getImageId: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var url = consts.SERVER_BASE_URL + '/clothes-sets/'
      url += this.clothes_set_id + '/'
      axios.get(url, config)
        .then(response => {
          console.log(response)
          this.imageURL = response.data.image_url
        }).catch((ex) => {
          this.alertMessage = '코디 이미지를 불러오지 못하였습니다. 오류가 계속 될 경우, 관리자에게 연락해주세요.'
          this.showAlert = true
        })
    },
    setDate: function () {
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())

      const minDate = new Date(today)
      minDate.setDate(minDate.getDate() - 6)

      const maxDate = new Date(today)
      maxDate.setDate(maxDate.getDate())

      this.min = minDate
      this.max = maxDate
    },
    submit: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var data = {
        clothes_set: Number(this.clothes_set_id),
        start_datetime: this.form.start_date + 'T' + this.form.start_time,
        end_datetime: this.form.end_date + 'T' + this.form.end_time,
        location: Number(this.locationData.location.id),
        review: Number(this.form.range),
        comment: this.form.comment
      }
      console.log(data)
      axios.post(`${consts.SERVER_BASE_URL}/clothes-set-reviews/`, data, config)
        .then(response => {
          this.$router.push({
            name: 'Bridge',
            params: {
              errorMessage: '리뷰가 성공적으로 등록되었습니다',
              destination: 'Cody',
              delay: 3,
              variant: 'success'
            }
          })
        }).catch((ex) => {
          this.alertMessage = '리뷰 등록에 실패했습니다. 오류가 계속 될 경우, 관리자에게 연락해주세요.'
          this.showAlert = true
        })
    },
    openLocationModal: function () {
      this.$refs['location-modal'].show()
    },
    handleLocationClick: function (event, location) {
      this.locationData.location.id = location.id
      this.locationData.location.name = location.location

      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

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
        }).catch((ex) => {
          vm.showLocationModalAlert = true
          vm.locationModalAlertMessage = '검색결과를 받아오는데 실패했습니다. 오류가 계속 될 경우 관리자에게 알려주세요.'
        })
    }
  },
  created: function () {
    this.getImageId()
    this.setDate()
    var vm = this
    if (vm.clothes_set_id === undefined) {
      alert('잘못된 접근입니다!')
      vm.$router.push('/login')
    }
  }
}
</script>

<style scoped>
  @import url("../css/login.css ");
h3{
    padding-bottom: 20px;
}
.text-top{
    padding-top: 30px;
}
</style>
