<template>
  <div class="modi">
    <b-button size="lg" v-on:click="f1">수정</b-button>
  </div>
</template>

<script>
// import { bus } from '../main'
export default {
  name: 'ClosetModifiedComponent',
  data () {
    return {
      context: 'changed',
      is_readonly: true
    }
  },
  methods: {
    f1: function () {
      if (this.is_readonly) {
        this.is_readonly = false
      } else {
        this.is_readonly = true
      }
    }
    // changeContext: function () {
    //   this.context = 'clicked'
    //   bus.$emit('contextChanged', 'clicked')
    // }
  }
}
</script>

<style>
.modi{
  display: inline-block;
  margin-right: 20px;
}
</style>
