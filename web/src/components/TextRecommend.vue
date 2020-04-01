<template>
<div class="col-md-3 left_side">
    <div class="well" style="margin-top:90px">
      <p>hi</p>
    </div>
    <div class="" style="text-align:right">
      <b-button v-b-toggle.collapse-1>펼쳐보기</b-button>
      <b-collapse id="collapse-1" class="mt-2">
          <b-card>
              <div class="row" style="padding:10px">
              <!-- <p class="card-text">Collapse contents Here</p> -->
                <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
                <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
                <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
                <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
                <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
                <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
              </div>
          </b-card>
      </b-collapse>
    </div>
</div>
</template>

<script>
export default {
  name: 'textrecommend'
}
</script>

<style scoped>
.left_side{
    display: inline-block;
}
.my_closet{
  background-color: #faf5ef;
  border-color: #d3f4ff;
  border-style: solid;
}
.hh{
  background-color: black;
  border-color: #d3f4ff;
  border-style: solid;
}
.closet_item {
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 120px;
  position: relative;
  background-size: 100% 100%;
}
</style>
