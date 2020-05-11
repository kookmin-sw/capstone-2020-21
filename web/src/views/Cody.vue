<template>
    <b-container>
        <b-row algin-h="end" class="mb-3 mr-1">
            <b-button to="/cody/add">등록하기</b-button>
        </b-row>
        <b-row>
            <b-col md="2" cols="12">
                <ClassificationComponent :list="categories" @chooseCategory="handleLowerClick"/>
            </b-col>
            <b-col md="10" cols="12">
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
      clothes_set: []
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
      this.$router.push('/login')
      // TODO: 에러메세지 더 좋은걸로 바꾸기.
      alert('로그인해주세요!')
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
            console.log(vm.clothes)
          }).catch((ex) => {
          // TODO: error handling.
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
              // TODO: error handling.
              })
          } else if (vm.currentCategories.upper === '스타일') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes-sets/?me=true&style=${vm.currentCategories.lower}`, config)
              .then((response) => {
                vm.clothes_set = response.data.results
              }).catch((ex) => {
              // TODO: error handling.
              })
          } else {
            axios.get(`${consts.SERVER_BASE_URL}/clothes-sets-review/?me=true`, config)
              .then((response) => {
                vm.clothes_set = response.data.results
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
