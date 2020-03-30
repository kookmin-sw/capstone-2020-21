<template>
<div class="col-md-3 left_side">
    <div class="row well" style="margin-top:90px">
      <p>hi</p>
    </div>
    <div class="row" style="text-align:right">
      <b-button class="btn_add" @click="goAdd()">펼쳐보기</b-button>
    </div>
    <div class="row">
        <div class="row" style="padding:30px">
            <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
                <a href="#">
                    <div class="txt">
                        <p>상의 / 후드</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
                <a href="#">
                    <div class="txt">
                        <p>상의 / 후드</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
                <a href="#">
                    <div class="txt">
                        <p>상의 / 후드</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
                <a href="#">
                    <div class="txt">
                        <p>상의 / 후드</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
                <a href="#">
                    <div class="txt">
                        <p>상의 / 후드</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4 closet_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
                <a href="#">
                    <div class="txt">
                        <p>상의 / 후드</p>
                    </div>
                </a>
            </div>
        </div>
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
.closet_item {
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 120px;
  position: relative;
  background-size: 100% 100%;
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
