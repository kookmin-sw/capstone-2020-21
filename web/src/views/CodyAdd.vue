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
              <b-col v-for="clothe in clothes" :key="clothe.id" cols=12 lg=6 class="mb-3">
                <ClothesCard class="mb-1" :clothes="clothe">
                  <template v-slot:additionalButton>
                    <b-button class="mt-1" variant="info" @click="handleAddClothes(clothe.id, clothe.image_url)">
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
        <b-form>
          <b-form-group label="코디 이름" label-for="cody-name">
            <b-form-input id="cody-name" v-model="codyName" type="text"></b-form-input>
          </b-form-group>
          <b-form-group label="코디 스타일" label-for="cody-style">
            <b-form-select id="cody-style" v-model="style" :options="styles"></b-form-select>
          </b-form-group>
        </b-form>
        <b-button variant="info" @click="postCody">등록하기</b-button>
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
      canvas: undefined,
      clothes: [],
      includedClothes: {},
      codyName: '',
      style: '',
      currentIndex: 0
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
    },
    styles: function () {
      return [
        '심플',
        '스트릿',
        '정장',
        '데이트',
        '화려'
      ]
    }
  },
  methods: {
    handleAddClothes: function (id, url) {
      var vm = this
      fabric.Image.fromURL(url, function (img) {
        img.set({
          left: 0,
          top: 0,
          angle: 0
        })

        img.perPixelTargetFind = true
        img.hasControls = img.hasBorders = true

        // TODO(mskwon1): change size of image to fit in canvas

        vm.canvas.add(img)
      }, { crossOrigin: 'anonymous' })

      vm.includedClothes[id] = this.currentIndex
      this.currentIndex += 1
    },
    handleConvertURL: function () {
      console.log(this.canvas.toDataURL())
    },
    postCody: function () {
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      var data = {
        clothes: Object.keys(this.includedClothes),
        name: this.codyName,
        style: this.style,
        image: this.canvas.toDataURL().split(',')[1]
      }

      axios.post(`${consts.SERVER_BASE_URL}/clothes-sets/`, data, config)
        .then((response) => {
          console.log(response)
          alert('성공적으로 등록되었습니다!')
          this.$router.push({ name: 'Cody' })
        }).catch((ex) => {
          // TODO: error handling.
        })
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
    this.canvas = new fabric.Canvas(ref, {
      hoverCursor: 'pointer',
      selection: false,
      targetFindTolerance: 2,
      backgroundColor: 'white'
    })

    this.canvas.setWidth(500)
    this.canvas.setHeight(750)
    this.canvas.setDimensions({ width: '250px', height: '325px' }, { cssOnly: true })

    this.canvas.on({
      'object.modified': function (e) {
        e.target.opacity = 1
      }
    })
  }
}
</script>

<style>
.canvas-container {
  margin: 0 auto;
  margin-bottom: 1rem;
}
</style>
