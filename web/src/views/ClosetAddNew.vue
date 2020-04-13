<template>
  <b-container>
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
      disableAnalysis: true
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
        alias: this.analysis_props.alias
      }
      axios.post(`${consts.SERVER_BASE_URL}/clothes/`, data, config)
        .then(response => {
          // TODO: delete console.log .
          console.log(response)
          this.$router.push('/closet')
        }).catch((ex) => {
          // TODO: handle error.
          console.log(ex)
        })
    },
    handleModify: function () {
      this.disableAnalysis = false
    },
    handleImageUpdate: function (event) {
      var imageStr = event.split(',')[1]
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      axios.post(`${consts.SERVER_BASE_URL}/clothes/inference/`, { image: imageStr }, config)
        .then(response => {
          // TODO: delete console.log .
          console.log(response)
          this.image = response.data.image_url
          this.analysis_props.upper = response.data.upper_category
          this.analysis_props.lower = response.data.lower_category
        }).catch((ex) => {
          // TODO: handle errors.
        })
    }
  },
  created: function () {
    if (!localStorage.getItem('token')) {
      this.$router.push('/login')
      // TODO: 에러메세지 더 좋은걸로 바꾸기.
      alert('로그인해주세요!')
    }
  }
}
</script>

<style>

</style>
