<template>
<div class="my_closet">
  <div class="row" style="padding:20px">
    <div class="col-md-6 cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <div class="box">
        <div class="txt">
            <b-button href="/cody/detail" style="margin-right:20px;">상세보기</b-button>
            <b-button href="/review">리뷰보기</b-button>
        </div>
      </div>
    </div>
    <div class="col-md-6 cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <div class="box">
        <div class="txt">
            <b-button href="/cody/detail" style="margin-right:20px;">상세보기</b-button>
            <b-button href="/review">리뷰보기</b-button>
        </div>
      </div>
    </div>
    <div class="col-md-6 cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <div class="box">
        <div class="txt">
            <b-button href="/cody/detail" style="margin-right:20px;">상세보기</b-button>
            <b-button href="/review">리뷰보기</b-button>
        </div>
      </div>
    </div>
    <div class="col-md-6 cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }" >
      <div class="box">
        <div class="txt">
            <b-button href="/cody/detail" style="margin-right:20px;">상세보기</b-button>
            <b-button href="/review">리뷰보기</b-button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'CodyComponent'
}
</script>

<style scoped>
.my_closet{
  background-color: #faf5ef;
  border-color: #d3f4ff;
  border-style: solid;
}
.cody_item {
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 400px;
  position: relative;
}

.box {
  display: block;
  width: 100%;
  height: 100%;
}

.cody_item > .box > .txt {
  display: none;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  color:white;
  line-height: 400px;
  text-align: center;
}

.cody_item > .box:hover > .txt {display: block;}
</style>
