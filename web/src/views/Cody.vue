<template>
    <b-container>
      <b-alert id="alert" v-model="showAlert" variant="danger" dismissible >
        {{ alertMessage }}
      </b-alert>
        <b-row class="mb-3 mr-1 justify-content-end">
            <b-button to="/cody/add">등록하기</b-button>
        </b-row>
        <b-row>
            <b-col md="2" cols="12">
                <ClassificationComponent :list="categories" @chooseCategory="handleLowerClick"/>
            </b-col>
            <b-col md="10" cols="12">
                <b-row>
                  <b-col cols="12">
                    <b-alert id="alert_cody" v-model="showCodyAlert" variant="danger" dismissible >
                      {{ noCodyMessage }}
                    </b-alert>
                  </b-col>
                </b-row>
                <b-row>
                    <b-col md="4" cols="12" class="mb-3"  v-for="clothe in clothes_set" :key="clothe.id">
                        <ClothesSetCard :clothes_set="clothe"/>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import ClassificationComponent from '@/components/ClassificationComponent.vue'
import ClothesSetCard from '@/components/cards/ClothesSetCard.vue'
import axios from 'axios'
import consts from '@/consts.js'
export default {
  components: {
    ClassificationComponent,
    ClothesSetCard
  },
  data: function () {
    return {
      currentCategories: { lower: '', upper: '' },
      clothes_set: [],
      alertMessage: '',
      noCodyMessage: '',
      showAlert: false,
      showCodyAlert: false
    }
  },
  computed: {
    categories: function () {
      const CODY_CATEGORIES = consts.CODY_CATEGORIES
      var categoryList = JSON.parse(JSON.stringify(CODY_CATEGORIES))
      for (var i in categoryList) {
        categoryList[i].lower.unshift('전체')
      }
      return categoryList
    }
  },
  methods: {
    handleLowerClick: function (upper, lower) {
      this.currentCategories.lower = lower
      this.currentCategories.upper = upper
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
    } else {
      var vm = this
      if (window.localStorage.getItem('token')) {
        var token = window.localStorage.getItem('token')
        var config = {
          headers: { Authorization: `Bearer ${token}` }
        }
        axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/?me=true`, config)
          .then((response) => {
            vm.clothes_set = response.data.results
            if (vm.clothes_set.length === 0) {
              this.noCodyMessage = '등록된 코디가 없습니다. 코디를 등록해 주세요'
              this.showCodyAlert = true
            }
          }).catch((ex) => {
            this.alertMessage = '코디를 불러올 수 없습니다. 다시 시도해주세요'
            this.showAlert = true
          })
      }
    }
  },
  watch: {
    currentCategories: {
      deep: true,
      handler () {
        var vm = this
        if (window.localStorage.getItem('token')) {
          var token = window.localStorage.getItem('token')
          var config = {
            headers: { Authorization: `Bearer ${token}` }
          }
          if (vm.currentCategories.lower === '전체') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/?me=true`, config)
              .then((response) => {
                vm.clothes_set = response.data.results
              }).catch((ex) => {
                this.alertMessage = '스타일의 전체 코디를 불러올 수 없습니다. 다시 시도해주세요'
                this.showAlert = true
              })
          } else if (vm.currentCategories.upper === '스타일') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/?me=true&style=${vm.currentCategories.lower}`, config)
              .then((response) => {
                vm.clothes_set = response.data.results
              }).catch((ex) => {
                this.alertMessage = '해당 스타일에 맞는 코디를 불러올 수 없습니다. 다시 시도해주세요'
                this.showAlert = true
              })
          } else if (vm.currentCategories.upper === '리뷰') {
            if (vm.currentCategories.lower === '등록') {
              axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/?me=true&review=true`, config)
                .then((response) => {
                  vm.clothes_set = response.data.results
                }).catch((ex) => {
                  this.alertMessage = '등록된 리뷰를 불러올 수 없습니다. 다시 시도해주세요'
                  this.showAlert = true
                })
            }
          }
        }
      }

    }

  }
}

</script>

<style>

</style>
