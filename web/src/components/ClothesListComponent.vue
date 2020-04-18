<template>
  <b-container>
    <b-row v-if="isBlankList">
      <b-col class="mb-2" cols=12>
        <b-card img-src="https://bit.ly/3a3Fff0" img-top img-fluid>
          <b-card-title>
            옷 등록해주세요
          </b-card-title>
          <b-card-body>
            등록된 옷이 없습니다. 등록해주세요!
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
    <b-row v-else>
      <b-col class="mb-2 mt-2" cols=4 v-for="clothe in clothes" :key=clothe.id @click="handleClothesClick(clothe.id)">
        <template v-if="imgOnly">
          <b-img :src="clothe.image_url" fluid />
        </template>
        <template v-else>
          <b-card :img-src="clothe.image_url" img-top>
            <b-card-title>
              {{ clothe.alias }}
            </b-card-title>
          </b-card>
        </template>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  props: [
    'clothes',
    'imgOnly'
  ],
  computed: {
    isBlankList: function () {
      return this.clothes.length === 0
    }
  },
  methods: {
    handleClothesClick: function (id) {
      this.$router.push({ name: 'ClosetDetail', params: { clothes_id: id } })
    }
  }
}
</script>

<style>

</style>
