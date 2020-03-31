<template>
  <div class="closet_detail">
    <MainNavigation></MainNavigation>
    <div class="btn_back">
        <router-link to="/closet"><b-button class="back">뒤로가기</b-button></router-link>
    </div>
    <div class="container_1">
        <ClosetDetailComponent></ClosetDetailComponent>
        <div class="information">
        <ClosetDeletedComponent></ClosetDeletedComponent>
        <ClosetDetailInfoComponent title="상세정보"></ClosetDetailInfoComponent>
        <ClosetModifiedComponent></ClosetModifiedComponent>
        <b-button size="lg">확인</b-button>
        </div>
    </div>

  </div>
</template>

<script>
import ClosetDetailComponent from '@/components/ClosetDetailComponent.vue'
import ClosetModifiedComponent from '@/components/ClosetModifiedComponent.vue'
import ClosetDeletedComponent from '@/components/ClosetDeletedComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'
import ClosetDetailInfoComponent from '@/components/ClosetDetailInfoComponent.vue'
export default {
  name: 'ClosetDetail',
  components: {
    ClosetDetailComponent,
    ClosetModifiedComponent,
    ClosetDeletedComponent,
    MainNavigation,
    ClosetDetailInfoComponent
  }
}
</script>

<style scoped>
.closet_detail{
    width: 100%;
    margin-right: auto;
    margin-left: auto;
}
.container_1{
    text-align: left;
    margin-top: 40px;
    display: inline-block;
    width: 100%;
    height: 100%;

}
.information{
    text-align: center;
    display: inline-block;
    position: absolute;
    top: 50%;
     margin-top: -200px;
     width: 300px;
     height: 300px;

}
.btn_back{
    text-align: left;
}
.back{
    margin-left: 150px;
    margin-bottom: 20px;
}
</style>
