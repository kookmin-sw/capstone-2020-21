<template>
  <b-container fluid class="p-4">
  <b-row>
    <!-- v-for 4 -->
    <b-col v-for="item in dataResult" md="4" class="pb-4 pt-4" v-bind:key="item" >
      <router-link :to="'/closet/' + item.id + '/detail'">
      <div style="position: relative;" v-b-hover="handleHover">
        <div v-if="isHovered">
          <span class="is-hover" :class="isHovered ? 'text-danger' : ''" ></span>
        </div>
        <b-img  fluid :src="item.image_url" alt="">
        </b-img>
      </div>
      </router-link>
    </b-col>

  </b-row>
</b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import { EventBus } from '@/event-bus.js'

export default {
  data () {
    return {
      isHovered: false,
      dataResult: ''

    }
  },
  methods: {
    goDetail: function () {
      this.$router.push({ name: 'ClosetDetail' })
    },
    handleHover (hovered) {
      this.isHovered = hovered
    }
  },
  created: function () {
    var vm = this
    if (window.localStorage.getItem('token')) {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      axios.get(`${consts.SERVER_BASE_URL}/users/11/clothes/`, config)
        .then((response) => {
          vm.dataResult = response.data.results
          console.log(vm.dataResult)
        }).catch((ex) => {
          // TODO: error handling.
        })
    }
  }
}
</script>

<style>
.is-hover {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
