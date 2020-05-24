<template>
    <b-container>
      <b-alert id="alert" v-model="showAlert" variant="success" dismissible >
        {{ alertMessage }}
      </b-alert>
        <b-row>
          <b-col cols="4" class="text-left">
            <b-button to="/cody">뒤로가기</b-button>
          </b-col>
          <b-col cols="4" class="text-center">
            <b-button @click="handleReviewClick">리뷰등록하기</b-button>
          </b-col>
          <b-col cols="4" class="text-right">
            <b-button @click="deleteCody">삭제하기</b-button>
          </b-col>
        </b-row>
        <b-row>
            <b-col md="6" cols="12">
                <b-img fluid :src="clothes_set.image_url"/>
            </b-col>
            <b-col md="6" cols="12">
                <b-row>
                  <b-col>
                    <b-row class="justify-content-center mb-3">
                      <h2>코디 정보</h2>
                    </b-row>
                    <b-row no-gutters class="mb-2">
                      <b-col align-self="center" cols="4">
                        <label class="mb-0" for="form-style">스타일</label>
                      </b-col>
                      <b-col cols="8">
                        <b-form-select id="form-style"
                                 :disabled="disableAnalysis"
                                 :options="style_categories"
                                 v-model="analysis_props.style"/>
                      </b-col>
                    </b-row>
                    <b-row no-gutters class="mb-2">
                      <b-col align-self="center" cols="4">
                        <label class="mb-0" for="form-name">별칭</label>
                      </b-col>
                      <b-col cols="8">
                        <b-form-input type="text"
                                        id="form-name"
                                        :disabled="disableAnalysis"
                                        v-model="analysis_props.name"/>
                      </b-col>
                    </b-row>
                  </b-col>
                </b-row>
                <b-row class="mb-3">
                    <b-col cols="6">
                        <b-button pill class="w-75" @click="handleModify">수정하기</b-button>
                    </b-col>
                    <b-col cols="6">
                        <b-button pill class="w-75" @click="handleUpdate">확인하기</b-button>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <b-row>
          <b-col cols="12">
            <b-alert id="alert_review" v-model="showReviewAlert" variant="danger" dismissible >
              {{ noReviewMessage }}
            </b-alert>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="4" cols="12" class="mb-3" v-for="cody_review in reviews" :key="cody_review.id">
            <ClothesSetReviewCard :review="cody_review"/>
          </b-col>
        </b-row>
    </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import ClothesSetReviewCard from '@/components/cards/ClothesSetReviewCard.vue'
export default {
  components: {
    ClothesSetReviewCard
  },
  data: function () {
    return {
      categories: consts.CODY_CATEGORIES,
      clothes_set: {
        name: '',
        style: '',
        id: 0,
        owner: '',
        image_url: '',
        clothes: []
      },
      analysis_props: {
        style: '',
        name: ''
      },
      disableAnalysis: true,
      reviews: [],
      alertMessage: '',
      noReviewMessage: '',
      showAlert: false,
      showReviewAlert: false
    }
  },
  props: [
    'clothes_set_id'
  ],
  computed: {
    style_categories: function () {
      for (var category of this.categories) {
        return category.lower
      }
      return []
    }

  },
  created: function () {
    this.style = this.style_category
    var vm = this
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
      if (vm.clothes_set_id === undefined) {
        this.$router.push({
          name: 'Bridge',
          params: {
            errorMessage: '해당 코디가 없습니다.',
            destination: 'Cody',
            delay: 3,
            variant: 'danger'
          }
        })
      } else {
        var clothesId = vm.clothes_set_id
        axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/${clothesId}/`)
          .then((response) => {
            vm.clothes_set = response.data
            vm.analysis_props.style = vm.clothes_set.style
            vm.analysis_props.name = vm.clothes_set.name
          }).catch((ex) => {
            this.alertMessage = '해당 코디를 불러올 수 없습니다. 다시 시도해주세요'
            this.showAlert = true
          })
        axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/${clothesId}/clothes-set-reviews`)
          .then((response) => {
            vm.reviews = response.data.results
            if (vm.reviews.length === 0) {
              this.noReviewMessage = '등록된 리뷰가 없습니다. 리뷰를 등록해 주세요'
              this.showReviewAlert = true
            }
          }).catch((ex) => {
            this.alertMessage = '리뷰를 불러올 수 없습니다. 다시 시도해주세요'
            this.showAlert = true
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
      var clothesId = vm.clothes_set_id
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      var data = {
        image_url: vm.image,
        name: vm.analysis_props.name,
        style: vm.analysis_props.style
      }
      axios.patch(`${consts.SERVER_BASE_URL}/clothes-sets/${clothesId}/`, data, config)
        .then(response => {
          this.alertMessage = '코디 정보를 수정했습니다.'
          this.showAlert = true
          vm.analysis_props.name = response.data.name
          vm.analysis_props.style = response.data.style
          vm.disableAnalysis = true
        }).catch((ex) => {
          this.alertMessage = '해당 코디를 수정할 수 없습니다. 다시 시도해주세요'
          this.showAlert = true
          console.log(ex)
        })
    },
    handleReviewClick: function () {
      this.$router.push({ name: 'Review', params: { clothes_set_id: this.clothes_set_id } })
    },
    deleteCody: function () {
      var vm = this
      var clothesId = vm.clothes_set_id
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      axios.delete(`${consts.SERVER_BASE_URL}/clothes-sets/${clothesId}/`, config)
        .then(response => {
          this.$router.push({
            name: 'Bridge',
            params: {
              errorMessage: '해당 코디가 삭제되었습니다.',
              destination: 'Cody',
              delay: 3,
              variant: 'success'
            }
          })
        }).catch((ex) => {
          this.alertMessage = '해당 코디를 삭제할 수 없습니다. 다시 시도해주세요'
          this.showAlert = true
          console.log(ex)
        })
    }
  }

}
</script>

<style>

</style>
