<template>
  <div class="main">
    <MainNavigation/>
    <div class="container">
      <div class="add_container">
        날씨 api 가져오는 부분
      </div>
      <div class="row">
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
        <TextRecommend />
        <div class="col-md-8">
          <CodyComponent/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'
import TextRecommend from '@/components/TextRecommend.vue'
// import MainComponent from '@/components/MainComponent.vue'
import CodyComponent from '@/components/CodyComponent.vue'
export default {
  name: 'main',
  components: {
    MainNavigation,
    TextRecommend,
    CodyComponent
  }

}
</script>
<style scoped>
#filtering {
    padding: 0px;
    margin-bottom: 10px;
    font-size: small;
    text-align: left;
    margin-left: 420px;
}
.closet {
    width: 100%;
    margin-right: auto;
    margin-left: auto;
    /* margin-top: 200px; */
}
.container_1{
  margin-top: 100px;
  text-align: left;
  margin-left: 50px;
}
.add_container{
  width:100%;
  text-align:right;
  margin-bottom: 20px;
}
</style>
