<template>
  <div class="closet_add">
    <MainNavigation></MainNavigation>
    <div class="container_1">
      <CodyDetailComponent></CodyDetailComponent>
      <div class="information">
        <div class="add_container">
          <div class="list">
            <a href="">상의 |</a>
            <a href=""> 바지 |</a>
            <a href=""> 치마 |</a>
            <a href=""> 아우터 |</a>
            <a href=""> 원피스</a>
          </div>
          <router-link to="/closet/add">
            <b-button class="btn_add" size="sm" style="margin-right:10px">옷 등록하기</b-button>
          </router-link>

       </div>
       <div class="show_clothes">
         <ClosetComponent :showCloset="false"></ClosetComponent>
       </div>
        <CodyDetailInfoComponent title="코디등록" v-bind:list="list"></CodyDetailInfoComponent>
      </div>
    </div>
  </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'
import ClosetComponent from '@/components/ClosetComponent.vue'
import CodyDetailInfoComponent from '@/components/CodyDetailInfoComponent.vue'
import CodyDetailComponent from '@/components/CodyDetailComponent.vue'

export default {
  name: 'ClosetAdd',
  components: {
    ClosetComponent,
    MainNavigation,
    CodyDetailInfoComponent,
    CodyDetailComponent
  },
  data: function () {
    return {
      list: ['심플', '스트릿', '화려', '데이트', '정장']
    }
  }

}
</script>

<style scoped>
.list{
  margin-right: 150px;
  display: inline-block;
}
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
.show_clothes{
  overflow: scroll;
  width: 500px;
  height: 180px;
  margin-bottom: 20px;
}
.add_container{
  width:100%;
  text-align:right;
  margin-bottom: 20px;
}
.information{
    text-align: center;
    display: inline-block;
    position: absolute;
    top: 50%;
     margin-top: -200px;
     width: 500px;
     height: 500px;
}
</style>
