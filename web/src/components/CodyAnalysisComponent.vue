<template>
  <b-container>
    <b-col>
      <b-row class="justify-content-center mb-3">
        <h2>코디 정보</h2>
      </b-row>
      <b-row no-gutters class="mb-2">
        <b-col align-self="center" cols="6">
          <label class="mb-0" for="form-upper">스타일</label>
        </b-col>
        <b-col cols="8">
          <b-form-select id="form-upper"
                          v-model="analysis_props.upper"
                          :disabled="isDisabled"
                          :options="upper_categories" />
        </b-col>
      </b-row>
      <b-row no-gutters class="mb-2">
        <b-col align-self="center" cols="6">
          <label class="mb-0" for="form-alias">별칭</label>
        </b-col>
        <b-col cols="8">
          <b-form-input type="text"
                          id="form-alias"
                          v-model="analysis_props.alias"
                          :disabled="isDisabled" />
        </b-col>
      </b-row>
    </b-col>
  </b-container>
</template>

<script>
import consts from '@/consts.js'

export default {
  props: [
    'analysis_props',
    'isDisabled'
  ],
  data: function () {
    return {
      categories: consts.CLOTHES_CATEGORIES
    }
  },
  computed: {
    upper_categories: function () {
      var result = []
      for (var category of this.categories) {
        result.push(category.upper)
      }
      return result
    }
  },
  created: function () {
    this.upper = this.upper_category
  }
}
</script>

<style>

</style>
