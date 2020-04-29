<template>
    <b-container>
        <b-row align-h="end" class="mb-3 mr-1">
            <b-button to="/closet/add">등록하기</b-button>
        </b-row>
        <b-row>
            <b-col md="2" cols="12">
                <ClassificationComponent :category.sync="currentCategories"/>
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
import ClassificationComponent from '@/components/ClassificationComponentNew.vue'
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
  created: function () {
    var vm = this
    // TODO : localStorage에 token이 없을 때 어떻게 처리할 지
    if (window.localStorage.getItem('token')) {
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
