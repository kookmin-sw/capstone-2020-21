<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols=12 md=8 order-md="1" order="2">
        <b-row>
          <b-col cols=12 md=4>
            <ClassificationComponent :list="categories" />
          </b-col>
          <b-col cols=12 md=8>
            <b-row>
              <b-col v-for="clothe in clothes" :key="clothe.id" cols=12 md=6 class="mb-3">
                <ClothesCard class="mb-1" :clothes="clothe">
                  <template v-slot:additionalButton>
                    <b-button class="mt-1" variant="info" @click="handleAddClothes(clothe.image_url)">
                      추가하기
                    </b-button>
                  </template>
                </ClothesCard>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
      <b-col cols=12 md=4 order-md="2" order="1">
        <canvas class="border" ref="codyCanvas" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import { fabric } from 'fabric'
import ClothesCard from '@/components/cards/ClothesCard.vue'
import ClassificationComponent from '@/components/ClassificationComponent.vue'

export default {
  name: 'CodyAdd',
  components: {
    ClothesCard,
    ClassificationComponent
  },
  data: function () {
    return {
      clothes: [],
      canvas: undefined
    }
  },
  computed: {
    categories: function () {
      const CLOTHES_CATEGORIES = consts.CLOTHES_CATEGORIES
      /*
        Workaround for deep copying nested objects
        ref: https://bit.ly/2y4vJLI
      */
      var categoryList = JSON.parse(JSON.stringify(CLOTHES_CATEGORIES))
      for (var i in categoryList) {
        categoryList[i].lower.unshift('전체')
      }
      return categoryList
    }
  },
  methods: {
    handleAddClothes: function (url) {
      var vm = this
      fabric.Image.fromURL(url, function (img) {
        img.set({
          left: 0,
          top: 0,
          angle: 0
        })

        img.perPixelTargetFind = true
        img.hasControls = img.hasBorders = true

        // img.scale(1)

        vm.canvas.add(img)
      }, { crossOrigin: 'anonymous' })
    },
    handleConvertURL: function () {
      console.log(this.canvas.toDataURL())
    }
  },
  created: function () {
    var token = window.localStorage.getItem('token')
    var config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    var vm = this
    axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true`, config)
      .then((response) => {
        vm.clothes = response.data.results
      }).catch((ex) => {
        // TODO: error handling.
      })
  },
  mounted: function () {
    const ref = this.$refs.codyCanvas
    console.log(ref.offsetWidth)
    this.canvas = new fabric.Canvas(ref, {
      hoverCursor: 'pointer',
      selection: false,
      targetFindTolerance: 2
    })

    this.canvas.setDimensions({ width: 250, height: 500 })

    this.canvas.on({
      // 'object:moving': function (e) {
      //   e.target.opacity = 0.5
      // },
      'object.modified': function (e) {
        e.target.opacity = 1
      }
    })
  }
}
</script>

<style>

</style>
