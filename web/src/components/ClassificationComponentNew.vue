<template>
  <b-container>
        <b-dropdown id="dropdown-dropright" dropright variant="outline-info" v-for="category in categories" :text="category.upper" class="m-2" size="lg" v-bind:key="category.upper">
            <b-dropdown-item v-for="detail in category.lower" v-bind:key="detail">
            {{ detail }}
            </b-dropdown-item>
        </b-dropdown>
  </b-container>
</template>

<script>
import consts from '@/consts.js'
export default {
  props: [
    'analysis_props'
  ],
  data: function () {
    return {
      categories: consts.CLOTHES_CATEGORIES
    }
  },
  methods: {

  }
}
</script>

<style>

</style>
