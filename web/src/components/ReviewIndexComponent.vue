<template>
  <div class="inline-block">
    <b-img blank blank-color="white" :style="styles[0]"></b-img>
    <b-img blank blank-color="#87b0e6" :style="styles[1]"></b-img>
    <b-img blank blank-color="#d15664" :style="styles[2]"></b-img>
    <b-img blank blank-color="white" :style="styles[3]"></b-img>
    <p style="word-break: keep-all">{{ text }}</p>
  </div>
</template>

<script>
export default {
  props: [
    'index'
  ],
  computed: {
    styles: function () {
      if (this.index === 1) {
        return [
          { width: 0 + '%', height: 1 + 'rem' },
          { width: 50 + '%', height: 1 + 'rem' },
          { width: 0 + '%', height: 1 + 'rem' },
          { width: 50 + '%', height: 1 + 'rem' }
        ]
      } else if (this.index === 2) {
        return [
          { width: 25 + '%', height: 1 + 'rem' },
          { width: 25 + '%', height: 1 + 'rem' },
          { width: 0 + '%', height: 1 + 'rem' },
          { width: 50 + '%', height: 1 + 'rem' }
        ]
      } else if (this.index === 3) {
        return [
          { width: 25 + '%', height: 1 + 'rem' },
          { width: 25 + '%', height: 1 + 'rem' },
          { width: 25 + '%', height: 1 + 'rem' },
          { width: 25 + '%', height: 1 + 'rem' }
        ]
      } else if (this.index === 4) {
        return [
          { width: 50 + '%', height: 1 + 'rem' },
          { width: 0 + '%', height: 1 + 'rem' },
          { width: 25 + '%', height: 1 + 'rem' },
          { width: 25 + '%', height: 1 + 'rem' }
        ]
      } else {
        return [
          { width: 50 + '%', height: 1 + 'rem' },
          { width: 0 + '%', height: 1 + 'rem' },
          { width: 50 + '%', height: 1 + 'rem' },
          { width: 0 + '%', height: 1 + 'rem' }
        ]
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
