<template>
    <b-container>
        <b-row>
          <b-col md="6" cols="12" style="text-align:left">
            <b-button to="/cody">뒤로가기</b-button>
          </b-col>
          <b-col md="6" cols="12" style="text-align:right">
            <b-button @click="deleteCody">삭제하기</b-button>
          </b-col>
        </b-row>
        <b-row>
            <b-col md="6" cols="12">
                <!-- <b-img fluid :src="clothes.image_url"/> -->
            </b-col>
            <b-col md="6" cols="12">
                <b-row>
                  <CodyAnalysisCompoonent/>
                </b-row>
                <b-row>
                    <b-col cols="6">
                        <b-button pill class="w-75" @click="handleModify">수정하기</b-button>
                    </b-col>
                    <b-col cols="6">
                        <b-button pill class="w-75" @click="handleUpdate">확인하기</b-button>
                    </b-col>
                </b-row>
            </b-col>

        </b-row>

    </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import CodyAnalysisCompoonent from '@/components/CodyAnalysisComponent.vue'
export default {
  components: {
    CodyAnalysisCompoonent
  },
  data: function () {
    return {
      categories: consts.CODY_CATEGORIES
    }
  },
  created: function () {

  }

}
</script>

<style>

</style>
