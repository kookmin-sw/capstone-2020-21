<template>
  <b-container>
    <b-row>
      <b-col>
        <b-card class="border-0">
          <b-card-title>
            추천 옷 조합
          </b-card-title>
          <b-alert id="categoryAlert" :show="categoryEmpty" variant="danger" style="word-break: keep-all">
            현재 날씨에 맞는 코디 정보가 없습니다
          </b-alert>
          <b-card v-for="combination in combinations"
                  :key="combination.combination"
                  style="word-break: keep-all"
                  class="mt-3"
                  v-b-toggle="combination.combination">
            <span>
              {{ combination.combination }}
            </span>
            <b-collapse :id="combination.combination" class="mt-1">
              <b-carousel controls>
                <b-carousel-slide v-for="image in combination.images" :key="image" :img-src="image">
                </b-carousel-slide>
              </b-carousel>
            </b-collapse>
          </b-card>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import { BIconArrowDown } from 'bootstrap-vue'

export default {
  components: {
    BIconArrowDown
  },
  props: [
    'combinations'
  ],
  data: function () {
    return {
    }
  },
  computed: {
    categoryEmpty: function () {
      return this.combinations.length === 0
    }
  }
}
</script>

<style>
  .carousel-control-prev-icon {
      background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23000' viewBox='0 0 8 8'%3E%3Cpath d='M5.25 0l-4 4 4 4 1.5-1.5-2.5-2.5 2.5-2.5-1.5-1.5z'/%3E%3C/svg%3E");
  }

  .carousel-control-next-icon {
      background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23000' viewBox='0 0 8 8'%3E%3Cpath d='M2.75 0l-1.5 1.5 2.5 2.5-2.5 2.5 1.5 1.5 4-4-4-4z'/%3E%3C/svg%3E");
  }
</style>
