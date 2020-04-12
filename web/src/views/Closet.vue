<template>
  <div class="closet">
    <MainNavigation></MainNavigation>
    <div class="container">
      <div class="add_container">
        <router-link to="/closet/add">
            <b-button class="btn_add" size="sm" style="margin-right:10px">등록하기</b-button>
          </router-link>
      </div>
      <div class="row">
        <ClassificationComponent v-bind:list="list"></ClassificationComponent>
        <div class="col-md-10 my_closet">
          <ClosetComponent :showCloset="true"></ClosetComponent>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ClosetComponent from '@/components/ClosetComponent.vue'
import ClassificationComponent from '@/components/ClassificationComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'
export default {
  name: 'Closet',
  components: {
    ClosetComponent,
    ClassificationComponent,
    MainNavigation
  },
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
  /* margin-top: 100px; */
  text-align: left;
  margin-left: 50px;
  margin-right: 50px;
}
.add_container{
  width:100%;
  text-align:right;
  margin-bottom: 20px;
}
.my_closet{
  background-color: #faf5ef;
  border-color: #d3f4ff;
  border-style: solid;
}
</style>
