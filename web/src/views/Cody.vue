<template>
<b-container>
  <b-row class="row">
    <b-col cols="3">
      <ClassificationComponent v-bind:list="list"></ClassificationComponent>
    </b-col>
    <b-col cols="9">
      <router-link to="/cody/add">
        <b-button class="btn_add" size="sm">등록하기</b-button>
      </router-link>
      <CodyComponent/>
    </b-col>
  </b-row>
</b-container>
</template>

<script>
import ClassificationComponent from '@/components/ClassificationComponent.vue'
import CodyComponent from '@/components/CodyComponent.vue'

export default {
  name: 'Cody',
  components: {
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
.row {
  margin-top: 80px;
}
.btn_add {
  margin-bottom: 20px;
}
</style>
