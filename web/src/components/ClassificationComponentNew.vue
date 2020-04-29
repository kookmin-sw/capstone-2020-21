<template>
  <b-container>
        <b-dropdown id="dropdown-dropright" dropright variant="outline-info" v-for="category in categories" :text="category.upper" class="m-2" size="lg" v-bind:key="category.upper">
            <b-dropdown-item v-for="detail in category.lower" v-bind:key="detail" @click="handleLower(detail,category.upper)">
            {{ detail }}
            </b-dropdown-item>
        </b-dropdown>
  </b-container>
</template>

<script>
import consts from '@/consts.js'
export default {
  props: [
    'category'
  ],
  data: function () {
    return {
    }
  },
  computed: {
    categories: function () {
      var categoryList = consts.CLOTHES_CATEGORIES.slice(0)
      for (var i in categoryList) {
        categoryList[i].lower.unshift('전체')
      }
      return categoryList
    }
  },
  methods: {
    handleLower: function (detail, upperInfo) {
      this.category.lower = detail
      this.category.upper = upperInfo
    }

  }
}
</script>

<style>

</style>
