<template>
<div class="main">
    <div class="add_container">
        날씨 api 가져오는 부분
    </div>
    <div id="filtering" class="container-fluid">
        <div id="nav filtering">
            <router-link to="/">최신등록순</router-link> |
            <router-link to="/">날씨별</router-link> |
            <router-link to="/">심플</router-link> |
            <router-link to="/">스트릿</router-link> |
            <router-link to="/">화려</router-link> |
            <router-link to="/">데이트</router-link> |
            <router-link to="/">정장</router-link> |
        </div>
    </div>
    <div class="row my_cody" style="padding:20px">
        <div class="col-md-6" style="margin-bottom:10px">
            <div class="cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
            <div class="review"></div>
        </div>
        <div class="col-md-6">
            <div class="cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
            <div class="review"></div>
        </div>
        <div class="col-md-6" style="margin-bottom:10px">
            <div class="cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
            <div class="review"></div>
        </div>
        <div class="col-md-6">
            <div class="cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" ></div>
            <div class="review"></div>
        </div>
        <!-- <div class="col-md-6 cody_item"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }" >
            <a href="#">
                <div class="txt">
                    <p>상의 / 후드</p>
                </div>
            </a>
        </div> -->
    </div>
</div>
</template>

<script>
export default {
  name: 'main'
}
</script>

<style scoped>
.main{
    margin-top: 150px;
}
#filtering {
    padding: 0px;
    margin-bottom: 10px;
    font-size: small;
}
.my_cody{
  background-color: #faf5ef;
  border-color: rgb(143, 203, 223);
  border-style: solid;
}
.cody_item {
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 240px;
  position: relative;
  background-size: 100% 100%;
  border-color: rgb(143, 203, 223);
  border-style: solid;
}

.cody_item > a {
  display: block;
  width: 100%;
  height: 100%;
}

.cody_item > a > .txt {
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

.cody_item > a:hover > .txt {display: block;}

.review{
    height: 100px;
    background-color: #faf5ef;
    border-color: rgb(143, 203, 223);
    border-style: solid;
}
</style>
