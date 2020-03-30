<template>
  <div class="closet_detail">
    <MainNavigation></MainNavigation>
    <b-button class="back">뒤로가기</b-button>
      <div class="container_1">
        <ClosetDetailComponent></ClosetDetailComponent>
        <ClosetDeletedComponent></ClosetDeletedComponent>
        <ClosetModifiedComponent></ClosetModifiedComponent>
      </div>
  </div>
</template>

<script>
import ClosetDetailComponent from '@/components/ClosetDetailComponent.vue'
import ClosetModifiedComponent from '@/components/ClosetModifiedComponent.vue'
import ClosetDeletedComponent from '@/components/ClosetDeletedComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'
export default {
  name: 'ClosetDetail',
  components: {
    ClosetDetailComponent,
    ClosetModifiedComponent,
    ClosetDeletedComponent,
    MainNavigation

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
    margin-left: 150px;
    margin-right: 150px;
    margin-top: 50px;

}
.back{
    text-align: left;
    margin-right: 900px;
}
</style>
