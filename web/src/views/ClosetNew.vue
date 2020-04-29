<template>
  <b-container>
      <b-row cols="1" cols-md="2">
          <b-col md="2">
              <ClassificationComponentNew :analysis_props.sync="analysis_props" :list="list" @click="SelectCate"/>
          </b-col>
          <b-col cols="12" md="10">
              <b-row align-h="end">
                  <b-button pill to="/closet/add">등록하기</b-button>
              </b-row>
              <b-row>
                  <ClosetComponentNew @update:image="handleImageShow"/>
              </b-row>
          </b-col>
      </b-row>
  </b-container>
</template>

<script>
import ClosetComponentNew from '@/components/ClosetComponentNew.vue'
import ClassificationComponentNew from '@/components/ClassificationComponentNew.vue'
import axios from 'axios'
import consts from '@/consts.js'
export default {
  components: {
    ClosetComponentNew,
    ClassificationComponentNew
  },
  data: function () {
    return {
      analysis_props: {
        upper: '',
        lower: ''
      },
      categories: consts.CLOTHES_CATEGORIES
    }
  },
  methods: {
    SelectCate: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
    }
    // handleImageShow: function (event) {
    //   var token = window.localStorage.getItem('token')
    //   var config = {
    //     headers: { Authorization: `Bearer ${token}`
    //   }
    //   // axios.get(`${}`)
    // }
  },
  created: function () {
    if (!localStorage.getItem('token')) {
      this.$router.push('/login')
      // TODO: 에러메세지 더 좋은걸로 바꾸기.
      alert('로그인해주세요!')
    }
  }
}
</script>

<style>

</style>
