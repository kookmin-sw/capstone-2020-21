<template>
  <b-overlay :show="isLoading">
    <b-container>
      <b-alert id="alert" v-model="showAlert" variant="danger" dismissible >
        {{ alertMessage }}
      </b-alert>
      <b-row cols="1" cols-md="2">
        <b-col class="mb-5 mb-md-0 pl-4 pr-4" cols="12" md="6">
            <ImageUploadComponent :image="image" @update:image="handleImageUpdate" />
        </b-col>
        <b-col cols="12" md="6">
          <b-row class="mb-3">
            <ImageAnalysisComponent :analysis_props.sync="analysis_props"
                                      :isDisabled="disableAnalysis" />
          </b-row>
          <b-row>
            <b-col cols="6">
              <b-button pill class="w-75" @click="handleModify">수정하기</b-button>
            </b-col>
            <b-col cols="6">
              <b-button pill class="w-75" @click="handleRegister">등록하기</b-button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </b-overlay>
</template>

<script>
import ImageUploadComponent from '@/components/ImageUploadComponent.vue'
import ImageAnalysisComponent from '@/components/ImageAnalysisComponent.vue'
import axios from 'axios'
import consts from '@/consts.js'

export default {
  components: {
    ImageUploadComponent,
    ImageAnalysisComponent
  },
  data: function () {
    return {
      image: 'https://bit.ly/3a3Fff0',
      analysis_props: {
        upper: '',
        lower: '',
        alias: ''
      },
      disableAnalysis: true,
      alertMessage: '',
      showAlert: false,
      isLoading: false
    }
  },
  methods: {
    handleRegister: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var data = {
        image_url: this.image,
        upper_category: this.analysis_props.upper,
        lower_category: this.analysis_props.lower,
      }
      if (this.analysis_props.alias !== '') {
        data['alias'] = this.analysis_props.alias
      }
      axios.post(`${consts.SERVER_BASE_URL}/clothes/`, data, config)
        .then(response => {
          this.$router.push({
            name: 'Bridge',
            params: {
              errorMessage: '옷이 성공적으로 등록되었습니다',
              destination: 'Closet',
              delay: 3,
              variant: 'success'
            }
          })
        }).catch((ex) => {
          this.alertMessage = '옷 등록에 실패했습니다. 오류가 계속 될 경우, 관리자에게 연락해주세요.'
          this.showAlert = true
        })
    },
    handleModify: function () {
      this.disableAnalysis = false
    },
    handleImageUpdate: function (event) {
      this.isLoading = true
      var imageStr = event.split(',')[1]
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      axios.post(`${consts.SERVER_BASE_URL}/clothes/inference/`, { image: imageStr }, config)
        .then(response => {
          this.image = response.data.image_url
          this.analysis_props.upper = response.data.upper_category
          this.analysis_props.lower = response.data.lower_category
          this.isLoading = false
        }).catch((ex) => {
          this.alertMessage = '옷 분석에 실패했습니다. 오류가 계속 될 경우, 관리자에게 연락해주세요.'
          this.showAlert = true
          this.isLoading = false
        })
    }
  },
  created: function () {
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
    }
  }
}
</script>

<style>

</style>
