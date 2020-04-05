<template>
  <div class="cody_detail">
    <MainNavigation></MainNavigation>
    <div class="btn_back">
        <router-link to="/cody"><b-button class="back">뒤로가기</b-button></router-link>
    </div>
    <div class="container_1">
        <CodyDetailComponent></CodyDetailComponent>
        <div class="information">
            <ClosetDeletedComponent></ClosetDeletedComponent>
            <ClosetDetailInfoComponent title="상세정보" upper="스타일"  starname="별칭"></ClosetDetailInfoComponent>
            <ClosetModifiedComponent></ClosetModifiedComponent>
            <b-button size="lg">확인</b-button>
        </div>
    </div>
  </div>
</template>

<script>
import CodyDetailComponent from '@/components/CodyDetailComponent.vue'
import ClosetModifiedComponent from '@/components/ClosetModifiedComponent.vue'
import ClosetDeletedComponent from '@/components/ClosetDeletedComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'
import ClosetDetailInfoComponent from '@/components/ClosetDetailInfoComponent.vue'
export default {
  name: 'CodyDetail',
  components: {
    ClosetModifiedComponent,
    CodyDetailComponent,
    ClosetDeletedComponent,
    MainNavigation,
    ClosetDetailInfoComponent
  }
}
</script>

<style scoped>
.cody_detail{
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
     width: 500px;
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
