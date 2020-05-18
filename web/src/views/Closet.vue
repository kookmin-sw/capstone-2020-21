<template>
    <b-container>
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
      clothes: []
    }
  },
  computed: {
    categories: function () {
      const CLOTHES_CATEGORIES = consts.CLOTHES_CATEGORIES
      /*
        Workaround for deep copying nested objects
        ref: https://bit.ly/2y4vJLI
      */
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
      this.$router.push('/login')
      // TODO: 에러메세지 더 좋은걸로 바꾸기.
      alert('로그인해주세요!')
    } else {
      var vm = this
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true`, config)
        .then((response) => {
          vm.clothes = response.data.results
        }).catch((ex) => {
          // TODO: error handling.
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
          if (vm.currentCategories.lower === '전체') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true&upper_category=${vm.currentCategories.upper}`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
              // TODO: error handling.
              })
          } else {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true&lower_category=${vm.currentCategories.lower}`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
              // TODO: error handling.
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
