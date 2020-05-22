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
        <template v-if="clothesEmpty">
          <b-alert show class="m-2" style="word-break: keep-all" variant="warning">
            카테고리에 맞는 옷이 없습니다
          </b-alert>
        </template>
        <ClothesListComponent v-else imgOnly=true :clothes="clothes"/>
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
  computed: {
    categoryItems: function () {
      var result = []
      for (var category of Object.keys(this.categories)) {
        if (this.categories[category] === '') {
          result.push({ '대분류': category, '소분류': '-' })
        } else {
          result.push({ '대분류': category, '소분류': this.categories[category] })
        }
      }
      return result
    },
    clothesEmpty: function () {
      return this.clothes.length === 0
    }
  },
  watch: {
    categories: {
      deep: true,
      handler () {
        this.fetchClothes()
      }
    }
  },
  methods: {
    fetchClothes: function () {
      // TODO(mskwon1): exception handling when categories don't exist.
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      var targetCategories = []
      for (var category of Object.keys(this.categories)) {
        if (this.categories[category] !== '') {
          targetCategories.push(this.categories[category])
        }
      }

      var vm = this
      var url = consts.SERVER_BASE_URL + '/clothes/?me=True'

      if (targetCategories.length !== 0) {
        url += '&lower_category='

        for (var i in targetCategories) {
          url += targetCategories[i]
          if (parseInt(i) + 1 !== targetCategories.length) {
            url += ','
          }
        }

        axios.get(url, config)
          .then((response) => {
            vm.clothes = response.data.results
          })
      }
    }
  },
  created: function () {
    this.fetchClothes()
  }
}
</script>

<style>

</style>
