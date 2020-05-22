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
              <b-img fluid :src="clothes.image_url"/>
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
                  <b-button pill class="w-75" @click="handleUpdate">확인하기</b-button>
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
      clothes: {
        alias: '',
        image_url: '',
        lower_category: '',
        upper_category: '',
        id: 0,
        owner: ''
      },
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
    if (vm.clothes_id === undefined) {
      alert('잘못된 접근입니다!')
      vm.$router.push('/closet')
    } else {
      if (!localStorage.getItem('token')) {
        this.$router.push({
          name: 'Bridge',
          params: {
            errorMessage: '로그인이 필요한 서비스입니다.',
            destination: 'login',
            delay: 3,
            variant: 'danger'
          }
        })
      } else {
        var clothesId = vm.clothes_id
        axios.get(`${consts.SERVER_BASE_URL}/clothes/${clothesId}/`)
          .then((response) => {
            vm.clothes = response.data
            vm.analysis_props.upper = vm.clothes.upper_category
            vm.analysis_props.lower = vm.clothes.lower_category
            vm.analysis_props.alias = vm.clothes.alias
          }).catch((ex) => {
          // TODO: error handling.
          })
      }
    }
  },
  methods: {
    handleModify: function () {
      this.disableAnalysis = false
    },
    handleUpdate: function () {
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
          alert('수정되었습니다!')
          vm.analysis_props.alias = response.data.alias
          vm.analysis_props.upper = response.data.upper_category
          vm.analysis_props.lower = response.data.lower_category
          vm.disableAnalysis = true
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
          alert('삭제되었습니다!')
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
