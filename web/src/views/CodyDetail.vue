<template>
  <div class="cody_detail">
    <MainNavigation></MainNavigation>
    <div class="btn_back">
        <router-link to="/cody"><b-button class="back">뒤로가기</b-button></router-link>
    </div>
     <b-container>
      <b-row>
        <b-col class="text-center" md="7">
          <CodyDetailComponent></CodyDetailComponent>
        </b-col>
        <b-col class="text-center" md="4" offset-md="1">
          <form action="" @submit.prevent="sendPost">
            <ClosetDeletedComponent></ClosetDeletedComponent>
            <CodyDetailInfoComponent title="상세정보" v-bind:list="list"></CodyDetailInfoComponent>
          </form>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { bus } from '../main'
import CodyDetailComponent from '@/components/CodyDetailComponent.vue'
import ClosetDeletedComponent from '@/components/ClosetDeletedComponent.vue'
import MainNavigation from '@/components/MainNavigation.vue'
import CodyDetailInfoComponent from '@/components/CodyDetailInfoComponent.vue'
export default {
  name: 'CodyDetail',
  components: {
    CodyDetailComponent,
    ClosetDeletedComponent,
    MainNavigation,
    CodyDetailInfoComponent
  },
  data: function () {
    return {
      list: ['심플', '스트릿', '화려', '데이트', '정장']
    }
  },
  created () {
    bus.$on('contextChanged', (data) => {
      console.log(data)
      this.context = data
    })
  },
  methods: {
    done: function (event) {
      alert('등록되었습니다')
    }
  }
}
</script>

<style scoped>
.cody_detail{
    width: 100%;
    margin-right: auto;
    margin-left: auto;
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
