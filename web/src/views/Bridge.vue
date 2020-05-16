<template>
  <b-container class="mt-5">
    <template v-if="isDefault">
      <b-row>
        <b-col class="mb-3" cols="12">
          오류입니다
        </b-col>
        <b-col cols="12">
          <b-button @click="handleHome">
            홈으로 돌아가기
          </b-button>
        </b-col>
      </b-row>
    </template>
    <template v-else>
      <b-row>
        <b-col class="mb-3">
          {{ errorMessage }}
        </b-col>
      </b-row>
      <b-row>
        <b-col class="mb-3">
          <b-spinner :variant="variant"></b-spinner>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          {{ count }}초 뒤 이동합니다 ...
        </b-col>
      </b-row>
    </template>
  </b-container>
</template>

<script>
export default {
  props: [
    'errorMessage',
    'destination',
    'delay',
    'variant'
  ],
  data: function () {
    return {
      count: 0,
      isDefault: false
    }
  },
  methods: {
    handleHome: function () {
      this.$router.push('/')
    }
  },
  created: function () {
    if (this.errorMessage === undefined) {
      this.isDefault = true
    }
  },
  mounted: function () {
    var vm = this
    setTimeout(function () {
      vm.$router.replace({
        name: vm.destination
      })
    }, vm.delay * 1000)
    vm.count = vm.delay
    var countTime = setInterval(function () {
      vm.count = vm.count - 1
      if (vm.count === 0) {
        clearInterval(countTime)
      }
    }, 1000)
  }
}
</script>

<style>

</style>
