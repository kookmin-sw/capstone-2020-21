<template>
  <b-overlay :show="isHovered" variant="dark" v-b-hover="handleHover">
    <b-card>
      <b-img :src="clothes_set.image_url" fluid style="height:10rem"/>
      <b-card-title>
        {{ clothes_set.name }}
      </b-card-title>
      <b-button pill variant="info">
        {{ clothes_set.style }}
      </b-button>
    </b-card>
    <template v-slot:overlay>
      <b-carousel controls indicators :interval="2000">
        <b-carousel-slide v-for="clothe in clothes_set.clothes" :key="clothe.id"
                          :img-src="clothe.image_url" style="height:8rem">
        <span class="p-1 text-light bg-dark font-weight-bold">
          {{ clothe.alias }}
        </span>
        </b-carousel-slide>
      </b-carousel>
      <b-button class="mt-3" variant="info" @click="handleClick">
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
    'clothes_set'
  ],
  methods: {
    handleClick: function () {
      this.$router.push({ name: 'CodyDetail', params: { clothes_set_id: this.clothes_set.id } })
    },
    handleHover: function (hovered) {
      this.isHovered = hovered
    }
  }
}
</script>

<style>

</style>
