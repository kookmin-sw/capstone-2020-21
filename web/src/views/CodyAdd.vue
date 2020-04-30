<template>
  <div class="closet_add">
    <MainNavigation></MainNavigation>
    <div class="btn_back">
        <router-link to="/closet"><b-button class="back">뒤로가기</b-button></router-link>
    </div>
    <b-container>
      <b-row>
        <b-col class="text-center" md="7">
          <CodyDetailComponent></CodyDetailComponent>
        </b-col>
        <b-col class="text-center" md="4" offset-md="1">
          <router-link to="/closet/add">
            <b-button class="btn_add" size="sm" style="margin-right:10px">옷 등록하기</b-button>
          </router-link>
          <div class="show_clothes">
         <ClosetComponent :showCloset="false"></ClosetComponent>
        </div>
          <CodyDetailInfoComponent title="코디등록" v-bind:list="list"></CodyDetailInfoComponent>
        </b-col>
      </b-row>
    </b-container>
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
.btn_back{
    text-align: left;
}
.back{
    margin-left: 150px;
    margin-bottom: 20px;
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
