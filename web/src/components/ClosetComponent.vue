<template>
  <div class="row" style="padding:20px">
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <div v-if="showCloset" class="show_more" @click="goDetail()">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </div>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/yb.png')+ ')' }" >
      <div v-if="showCloset" class="show_more" @click="goDetail()">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </div>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hb.png')+ ')' }" >
      <div v-if="showCloset" class="show_more" @click="goDetail()">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </div>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <div v-if="showCloset" class="show_more" @click="goDetail()">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClosetComponent',
  props: ['showCloset'],
  methods: {
    goDetail: function () {
      this.$router.push({ name: 'ClosetDetail' })
    }
  }
}
</script>

<style scoped>
.closet_item {
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 240px;
  position: relative;
}

.closet_item > .show_more {
  display: block;
  width: 100%;
  height: 100%;
}

.closet_item > .show_more > .txt {
  display: none;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  color:white;
  line-height: 240px;
  text-align: center;
}

.closet_item > div:hover > .txt {display: block;}
</style>
