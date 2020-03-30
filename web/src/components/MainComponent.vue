<template>
<div class="col-md-9">
    <div id="filtering" class="container-fluid">
        <div id="nav">
            <router-link to="/">최신등록순</router-link> |
            <router-link to="/">날씨별</router-link> |
            <router-link to="/">심플</router-link> |
            <router-link to="/">스트릿</router-link> |
            <router-link to="/">화려</router-link> |
            <router-link to="/">데이트</router-link> |
            <router-link to="/">정장</router-link> |
        </div>
    </div>
    <div class="row my_closet" style="padding:20px">
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
</template>

<script>
export default {
  name: 'main'
}
</script>

<style scoped>
.my_closet{
  background-color: #faf5ef;
  border-color: #d3f4ff;
  border-style: solid;
}
.closet_item {
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 240px;
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
