<template>
  <div class="row" style="padding:20px">
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <a href="closet/detail">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
        <!-- <img src="../assets/hh.png" alt=""> -->
      </a>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <a href="#">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </a>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <a href="#">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </a>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <a href="#">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </a>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <a href="#">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </a>
    </div>
    <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <a href="#">
        <div class="txt">
          <p>상의 / 후드</p>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClosetComponent'
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

.closet_item > a {
  display: block;
  width: 100%;
  height: 100%;
}

.closet_item > a > .txt {
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

.closet_item > a:hover > .txt {display: block;}
</style>
