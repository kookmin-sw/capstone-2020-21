<template>
  <div class="inline-block">
    <b-img blank :blank-color="colors[0]" style="width:25%; height:1rem"></b-img>
    <b-img blank :blank-color="colors[1]" style="width:12.5%; height:1rem"></b-img>
    <b-img blank :blank-color="colors[2]" style="width:12.5%; height:1rem"></b-img>
    <b-img blank :blank-color="colors[3]" style="width:12.5%; height:1rem"></b-img>
    <b-img blank :blank-color="colors[4]" style="width:12.5%; height:1rem"></b-img>
    <b-img blank :blank-color="colors[5]" style="width:25%; height:1rem">더웡</b-img>
    <p>{{ text }}</p>
  </div>
</template>

<script>
export default {
  props: [
    'index'
  ],
  computed: {
    colors: function () {
      if (this.index === 1) {
        return ['#87b0e6', '#87b0e6', '#87b0e6', 'white', 'white', 'white']
      } else if (this.index === 2) {
        return ['white', '#87b0e6', '#87b0e6', 'white', 'white', 'white']
      } else if (this.index === 3) {
        return ['white', 'white', '#87b0e6', '#d15664', 'white', 'white']
      } else if (this.index === 4) {
        return ['white', 'white', 'white', '#d15664', '#d15664', 'white']
      } else {
        return ['white', 'white', 'white', '#d15664', '#d15664', '#d15664']
      }
    },
    text: function () {
      if (this.index === 1) {
        return '추웠어요'
      } else if (this.index === 2) {
        return '적당히 추웠어요'
      } else if (this.index === 3) {
        return '딱 좋았어요'
      } else if (this.index === 4) {
        return '적당히 더웠어요'
      } else {
        return '더웠어요'
      }
    }
  }
}
</script>

<style>

</style>
