<template>
  <div class="cody_detail_c">
    <div class="detail_box">
      <div class="detail_item" v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CodyDetailComponent'
}
</script>

<style>
.cody_detail_c{
  display: inline-block;
  margin-right: 100px;
  margin-left: 200px;
}
.detail_box{
  background-color: #faf5ef;
  border-color: #d3f4ff;
  border-style: solid;
  width: 500px;
  height: 500px;
  background-image: 100% 100%;
}
.detail_item{
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 450px;
  position: relative;
}
</style>
