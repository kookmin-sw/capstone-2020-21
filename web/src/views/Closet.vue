<template>
  <div class="closet">
    <MainNavigation></MainNavigation>
    <div class="container">
      <div class="add_container">
        <b-button class="btn_add" style="margin-right:10px" href="/closet/add">등록하기</b-button>
      </div>
      <div class="row">
        <ClassificationComponent :inCloset="true"></ClassificationComponent>
        <div class="col-md-10 my_closet">
          <ClosetComponent></ClosetComponent>
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
