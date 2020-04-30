<template>
  <b-overlay :show="isHovered" variant="dark" v-b-hover="handleHover">
    <b-card>
      <b-card-title>
        {{ clothes.alias }}
      </b-card-title>
      <b-img :src="clothes.image_url" fluid />
    </b-card>
    <template v-slot:overlay>
      <span class="text-light" style="word-break: keep-all">
        {{ clothes.upper_category }} / {{ clothes.lower_category }}
      </span>
      <b-button class="mt-1" variant="info" @click="handleClick">
        상세보기
      </b-button>
    </template>
  </b-overlay>
</template>

<script>
export default {
  data: function () {
    return {
      isHovered: false
    }
  },
  props: [
    'clothes'
  ],
  methods: {
    handleClick: function () {
      this.$router.push({ name: 'ClosetDetail', params: { clothes_id: this.clothes.id } })
    },
    handleHover: function (hovered) {
      this.isHovered = hovered
    }
  }
}
</script>

<style>

</style>
