<template>
  <div class="main">
    <MainNavigation/>
    <div class="container_1">
      <div class="add_container">
        날씨 api 가져오는 부분
      </div>
      <div class="row">
        <TextRecommend/>
        <MainComponent/>
      </div>
    </div>
  </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'
import TextRecommend from '@/components/TextRecommend.vue'
import MainComponent from '@/components/MainComponent.vue'
export default {
  name: 'main',
  components: {
    MainNavigation,
    TextRecommend,
    MainComponent
  }

}
</script>
<style scoped>
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
