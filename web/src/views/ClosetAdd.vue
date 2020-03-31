<template>
  <div class="closet_add">
    <MainNavigation></MainNavigation>
    <div class="container_1">
        <ClosetAddComponent></ClosetAddComponent>
        <div class="information">
        <ClosetDetailInfoComponent title="분석결과"></ClosetDetailInfoComponent>
        <ClosetModifiedComponent></ClosetModifiedComponent>
        <b-button size="lg">확인</b-button>
        </div>
    </div>
  </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'
import ClosetModifiedComponent from '@/components/ClosetModifiedComponent.vue'
import ClosetDetailInfoComponent from '@/components/ClosetDetailInfoComponent.vue'
import ClosetAddComponent from '@/components/ClosetAddComponent.vue'
export default {
  name: 'ClosetAdd',
  components: {
    MainNavigation,
    ClosetModifiedComponent,
    ClosetDetailInfoComponent,
    ClosetAddComponent
  }

}
</script>

<style>
.closet_add {
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
</style>
