<template>
    <b-container>
        <b-row>
          <b-col md="6" cols="12" style="text-align:left">
            <b-button to="/closet">뒤로가기</b-button>
          </b-col>
          <b-col md="6" cols="12" style="text-align:right">
            <b-button @click="deleteClothe">삭제하기</b-button>
          </b-col>
        </b-row>
        <b-row>
            <b-col md="6" cols="12">
              <b-img fluid :src="currentImage"/>
            </b-col>
            <b-col md="6" cols="12">
              <b-row>
                <ImageAnalysisComponent :analysis_props.sync="analysis_props" :isDisabled="disableAnalysis" />
              </b-row>
              <b-row>
                <b-col cols="6">
                  <b-button pill class="w-75" @click="handleModify">수정하기</b-button>
                </b-col>
                <b-col cols="6">
                  <b-button pill class="w-75" @click="handleUpdateRegister">확인하기</b-button>
                </b-col>
              </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import ImageAnalysisComponent from '@/components/ImageAnalysisComponent.vue'
export default {
  components: {
    ImageAnalysisComponent
  },
  data: function () {
    return {
      currentImage: '',
      clothes: [],
      analysis_props: {
        upper: '',
        lower: '',
        alias: ''
      },
      disableAnalysis: true
    }
  },
  props: [
    'clothes_id'
  ],
  created: function () {
    var vm = this
    if (!localStorage.getItem('token')) {
      vm.$router.push('/login')
      // TODO: 에러메세지 더 좋은걸로 바꾸기.
      alert('로그인해주세요!')
    } else {
      // TODO : localStorage에 token이 없을 때 어떻게 처리할 지
      if (window.localStorage.getItem('token')) {
        var token = window.localStorage.getItem('token')
        var config = {
          headers: { Authorization: `Bearer ${token}` }
        }
        var clothesId = vm.clothes_id
        axios.get(`${consts.SERVER_BASE_URL}/clothes/${clothesId}/`)
          .then((response) => {
            vm.clothes = response.data
            vm.currentImage = vm.clothes.image_url
            vm.analysis_props.upper = vm.clothes.upper_category
            vm.analysis_props.lower = vm.clothes.lower_category
            vm.analysis_props.alias = vm.clothes.alias
          }).catch((ex) => {
            // TODO: error handling.
          })
      } else {
        alert('회원가입 해주세요')
      }
    }
  },
  methods: {
    handleModify: function () {
      this.disableAnalysis = false
    },
    handleUpdateRegister: function () {
      var vm = this
      var clothesId = vm.clothes_id
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var data = {
        image_url: vm.image,
        upper_category: vm.analysis_props.upper,
        lower_category: vm.analysis_props.lower,
        alias: vm.analysis_props.alias
      }
      axios.patch(`${consts.SERVER_BASE_URL}/clothes/${clothesId}/`, data, config)
        .then(response => {
          // TODO: delete console.log .
          vm.$router.push('/closet')
        }).catch((ex) => {
          // TODO: handle error.
          console.log(ex)
        })
    },
    deleteClothe: function () {
      var vm = this
      var clothesId = vm.clothes_id
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      axios.delete(`${consts.SERVER_BASE_URL}/clothes/${clothesId}/`, config)
        .then(response => {
          console.log(response)
          // TODO: delete console.log .
          vm.$router.push('/closet')
        }).catch((ex) => {
          // TODO: handle error.
          console.log(ex)
        })
    }
  }
}
</script>

<style>

</style>
