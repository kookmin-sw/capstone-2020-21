<template>
    <b-container>
        <b-row>
          <b-col md="4" cols="12" style="text-align:left">
            <b-button to="/cody">뒤로가기</b-button>
          </b-col>
          <b-col md="4" cols="12" style="text-align:center">
            <b-button to="/review">리뷰등록하기</b-button>
          </b-col>
          <b-col md="4" cols="12" style="text-align:right">
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
        <!-- review 보여주기 -->
        <b-row>
          <!-- <b-col md="4" cols="12" class="mb-3" v-for="review in clothes_set_review" :key="review.id">
            <ClothesSetReviewCard :clothes_set_review="review"/>
          </b-col> -->
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
      clothes_set_review: []
    }
  },
  props: [
    'review',
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
    if (vm.clothes_set_id === undefined) {
      alert('잘못된 접근입니다!')
      vm.$router.push('/cody')
    } else {
      if (!localStorage.getItem('token')) {
        vm.$router.push('/login')
        // TODO: 에러메세지 더 좋은걸로 바꾸기.
        alert('로그인해주세요!')
      } else {
        var clothesId = vm.clothes_set_id
        axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/${clothesId}/`)
          .then((response) => {
            console.log(response.data)
            vm.clothes_set = response.data

            vm.analysis_props.style = vm.clothes_set.style
            vm.analysis_props.name = vm.clothes_set.name
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
          alert('수정되었습니다!')
          vm.analysis_props.name = response.data.name
          vm.analysis_props.style = response.data.style
          vm.disableAnalysis = true
        }).catch((ex) => {
          // TODO: handle error.
          console.log(ex)
        })
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
          alert('삭제되었습니다!')
          vm.$router.push('/cody')
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
