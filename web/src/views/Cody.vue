<template>
    <div class="cody">
        <MainNavigation></MainNavigation>
        <div class="container">
            <div class="add_container">
            <b-button class="btn_add" style="margin-right:10px" href="/cody/add">등록하기</b-button>
            </div>
            <div class="row">
                <ClassificationComponent :inCloset="false"></ClassificationComponent>
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
