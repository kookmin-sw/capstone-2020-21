<template>
    <div class="cody">
        <MainNavigation></MainNavigation>
        <div class="container">
            <div class="add_container">
            <router-link to="/cody/add">
              <b-button class="btn_add" size="sm" style="margin-right:10px">등록하기</b-button>
          </router-link>

            </div>
            <div class="row">
                <ClassificationComponent v-bind:list="list"></ClassificationComponent>
                <div class="col-md-10">
                  <CodyComponent></CodyComponent>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import MainNavigation from '@/components/MainNavigation.vue'
import ClassificationComponent from '@/components/ClassificationComponent.vue'
import CodyComponent from '@/components/CodyComponent.vue'
export default {
  name: 'Cody',
  components: {
    MainNavigation,
    ClassificationComponent,
    CodyComponent
  },
  data: function () {
    return {
      list: [
        {
          name: '스타일',
          details: ['전체', '심플', '스트릿', '화려', '데이트', '정장']
        },
        {
          name: '리뷰',
          details: ['전체', '미등록']
        }
      ]
    }
  }
}
</script>
<style scoped>
.cody {
    width: 100%;
    margin-right: auto;
    margin-left: auto;
    /* margin-top: 200px; */
}
.container_1{
   margin-top: 100px;
  text-align: left;
  /* margin-left: 50px;
  margin-right: 50px; */
}
.add_container{
  width:100%;
  text-align:right;
  margin-bottom: 20px;
}
</style>