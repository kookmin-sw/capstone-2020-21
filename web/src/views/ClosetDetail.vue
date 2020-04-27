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
        <ClosetDetailInfoComponent title="상세정보" v-bind:list="list"></ClosetDetailInfoComponent>
      </div>
    </div>
  </div>
</template>

<script>
import { bus } from '../main'
import ClosetDetailComponent from '@/components/ClosetDetailComponent.vue'
import ClosetDeletedComponent from '@/components/ClosetDeletedComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'
import ClosetDetailInfoComponent from '@/components/ClosetDetailInfoComponent.vue'
export default {
  name: 'ClosetDetail',
  components: {
    ClosetDetailComponent,
    ClosetDeletedComponent,
    MainNavigation,
    ClosetDetailInfoComponent
  },
  props: [
    'clothes_id'
  ],
  data: function () {
    return {
      list: [
        {
          name: '상의',
          details: ['전체', '후드티', '반팔티셔츠', '긴팔티셔츠', '반팔셔츠', '긴팔셔츠', '맨투맨', '터틀넥', '니트', '블라우스', '끈나시', '민소매']
        },
        {
          name: '바지',
          details: ['전체', '반바지', '핫팬츠', '슬랙스', '청바지', '골덴바지', '트레이닝바지']
        },
        {
          name: '치마',
          details: ['전체', '미니스커트', '롱스커트']
        },
        {
          name: '아우터',
          details: ['전체', '블레이져', '숏패딩', '조끼패딩', '롱패딩', '야구점퍼', '항공점퍼', '바람막이', '야상', '무스탕', '코트', '트랙탑', '가죽자켓', '청자켓', '가디건']
        }
      ]
    }
  },
  created () {
    bus.$on('contextChanged', (data) => {
      console.log(data)
      this.context = data
    })
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
