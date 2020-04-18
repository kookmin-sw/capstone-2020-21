<template>
  <b-container>
    <b-row>
      <b-col>
        <b-card class="border-0">
          <b-card-title>
            추천 카테고리
          </b-card-title>
          <b-table hover :items="categoryItems" />
        </b-card>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <h5>내 옷들</h5>
        <ClothesListComponent imgOnly=true :clothes="clothes"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import ClothesListComponent from '@/components/ClothesListComponent'

export default {
  components: {
    ClothesListComponent
  },
  props: [
    'categories'
  ],
  data: function () {
    return {
      clothes: []
    }
  },
  created: function () {
    var token = window.localStorage.getItem('token')
    var config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    var vm = this
    var url = consts.SERVER_BASE_URL + '/clothes/?limit=10'

    axios.get(url, config)
      .then((response) => {
        vm.clothes = response.data.results
      })
  },
  computed: {
    categoryItems: function () {
      var result = []
      for (var category of Object.keys(this.categories)) {
        // TODO(mskwon1) : 해당되는 소분류가 없을시 오류처리.
        result.push({ '대분류': category, '소분류': this.categories[category] })
      }
      return result
    }
  }
}
</script>

<style>

</style>
