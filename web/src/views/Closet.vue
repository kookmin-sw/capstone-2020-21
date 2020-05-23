<template>
    <b-container>
      <b-alert id="alert" v-model="showAlert" variant="danger" dismissible >
        {{ alertMessage }}
      </b-alert>
        <b-row align-h="end" class="mb-3 mr-1">
            <b-button to="/closet/add">등록하기</b-button>
        </b-row>
        <b-row>
            <b-col md="2" cols="12">
                <ClassificationComponent :list="categories"
                                          @chooseCategory="handleLowerClick"/>
            </b-col>
            <b-col md="10" cols="12">
              <b-row>
                <b-col cols="12">
                  <b-alert id="alert_clothe" v-model="showClotheAlert" variant="danger" dismissible >
                    {{ noClotheMessage }}
                  </b-alert>
                </b-col>
              </b-row>
                <b-row>
                    <b-col v-for="clothe in clothes" :key="clothe.id" md="4" cols="12" class="mb-3">
                        <ClothesCard :clothes="clothe"/>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import ClassificationComponent from '@/components/ClassificationComponent.vue'
import ClothesCard from '@/components/cards/ClothesCard.vue'
import axios from 'axios'
import consts from '@/consts.js'

export default {
  components: {
    ClassificationComponent,
    ClothesCard
  },
  data: function () {
    return {
      currentCategories: { lower: '', upper: '' },
      clothes: [],
      alertMessage: '',
      noClotheMessage: '',
      showAlert: false,
      showClotheAlert: false
    }
  },
  computed: {
    categories: function () {
      const CLOTHES_CATEGORIES = consts.CLOTHES_CATEGORIES
      var categoryList = JSON.parse(JSON.stringify(CLOTHES_CATEGORIES))
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
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true`, config)
        .then((response) => {
          vm.clothes = response.data.results
          if (vm.clothes.length === 0) {
            this.noClotheMessage = '등록된 옷이 없습니다. 옷을 등록해 주세요'
            this.showClotheAlert = true
          }
        }).catch((ex) => {
          this.alertMessage = '옷을 불러올 수 없습니다. 다시 시도해주세요'
          this.showAlert = true
        })
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
          if (vm.currentCategories.upper === '전체') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
                this.alertMessage = '전체 옷을 불러올 수 없습니다. 다시 시도해주세요'
                this.showAlert = true
              })
          } else if (vm.currentCategories.lower === '전체') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true&upper_category=${vm.currentCategories.upper}`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
                this.alertMessage = '해당 카테고리의 전체 옷을 불러올 수 없습니다. 다시 시도해주세요'
                this.showAlert = true
              })
          } else {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true&lower_category=${vm.currentCategories.lower}`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
                this.alertMessage = '해당 소분류 카테고리를 불러올 수없습니다. 다시 시도해주세요'
                this.showAlert = true
              })
          }
        }
      }
    }
  }
}
</script>

<style>

</style>
