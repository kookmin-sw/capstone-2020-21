<template>
  <b-overlay :show="isLoading">
    <b-container>
      <b-alert id="alert" v-model="showAlert" variant="danger" dismissible style="word-break: keep-all">
        {{ alertMessage }}
      </b-alert>
      <b-row align-h="center">
        <b-col cols=12 md=8 order-md="1" order="2">
          <b-row>
            <b-col cols=12 md=4>
              <ClassificationComponent :list="categories" @chooseCategory="handleChooseCategory" />
            </b-col>
            <b-col cols=12 md=8>
              <b-row>
                <template v-if="clothesExists">
                  <b-col v-for="clothe in clothes" :key="clothe.id" cols=12 lg=6 class="mb-3">
                    <ClothesCard class="mb-1" :clothes="clothe">
                      <template v-slot:additionalButton>
                        <b-button class="mt-1" variant="info" @click="handleAddClothes(clothe.id, clothe.image_url)">
                          추가하기
                        </b-button>
                      </template>
                    </ClothesCard>
                  </b-col>
                </template>
                <template v-else>
                  <b-col cols=12 class="mb-3 align-self-center">
                    <b-container class="border p-3">
                      등록된 옷이 없습니다
                      <br>
                      <b-button class="mt-3" variant="info" to="/closet/add">
                        옷 등록하러가기
                      </b-button>
                    </b-container>
                  </b-col>
                </template>
              </b-row>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols=12 md=4 order-md="2" order="1">
          <b-row>
            <b-col>
              <canvas class="border" ref="codyCanvas" />
            </b-col>
          </b-row>
          <b-row>
            <b-col v-for="clothe in includedClothes" :key="clothe.id" class="mb-1" cols=4>
              <b-img class="mb-1" :src="clothe.url" fluid />
              <b-button pill size="sm" variant="danger" @click="handleRemoveClothes(clothe.id, clothe.obj)">
                <b-icon-x/>
              </b-button>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form>
                <b-form-group label="코디 이름" label-for="cody-name">
                  <b-form-input id="cody-name" v-model="codyName" type="text"></b-form-input>
                </b-form-group>
                <b-form-group label="코디 스타일" label-for="cody-style">
                  <b-form-select id="cody-style" v-model="style" :options="styles"></b-form-select>
                </b-form-group>
              </b-form>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-button variant="info" @click="postCody">등록하기</b-button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </b-overlay>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'
import { fabric } from 'fabric'
import { BIconX } from 'bootstrap-vue'
import ClothesCard from '@/components/cards/ClothesCard.vue'
import ClassificationComponent from '@/components/ClassificationComponent.vue'

export default {
  name: 'CodyAdd',
  components: {
    BIconX,
    ClothesCard,
    ClassificationComponent
  },
  data: function () {
    return {
      canvas: undefined,
      clothes: [],
      includedClothes: [],
      codyName: '',
      style: '',
      showAlert: false,
      alertMessage: '',
      isLoading: false,
      currentCategories: { lower: '', upper: '' }
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
    },
    clothesExists: function () {
      return this.clothes.length !== 0
    }
  },
  methods: {
    handleAddClothes: function (id, url) {
      var clotheIds = this.includedClothes.map((clothe) => {
        return clothe.id
      })

      if (clotheIds.includes(id)) {
        this.alertMessage = '이미 추가된 옷입니다.'
        this.showAlert = true
        window.scrollTo(0, 0)
        return
      }

      var vm = this

      // Workaround for caching issue.
      // https://bit.ly/2YGaTNs
      url += '?please=work'
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
        vm.includedClothes.push({ id: id, obj: img, url: url })
      }, { crossOrigin: 'anonymous' })
    },
    handleRemoveClothes: function (id, obj) {
      this.canvas.remove(obj)
      this.includedClothes = this.includedClothes.filter((clothe) => {
        return clothe.id !== id
      })
    },
    handleChooseCategory: function (upper, lower) {
      this.currentCategories.upper = upper
      this.currentCategories.lower = lower
    },
    postCody: function () {
      this.isLoading = true
      var token = window.localStorage.getItem('token')
      var config = {
        headers: { Authorization: `Bearer ${token}` }
      }

      var clothes = this.includedClothes.map((clothe) => {
        return clothe.id
      })

      var data = {
        clothes: clothes,
        name: this.codyName,
        style: this.style,
        image: this.canvas.toDataURL().split(',')[1]
      }

      axios.post(`${consts.SERVER_BASE_URL}/clothes-sets/`, data, config)
        .then((response) => {
          var msg = `'${response.data.name}' 코디가 성공적으로 등록되었습니다!`
          this.$router.push({
            name: 'Bridge',
            params: {
              errorMessage: msg,
              destination: 'Cody',
              delay: 3,
              variant: 'success'
            }
          })
        }).catch((ex) => {
          this.isLoading = false
          this.alertMessage = '요청이 잘못되었습니다. 입력내용을 확인해주세요!'
          this.showAlert = true
          window.scrollTo(0, 0)
        })
    }
  },
  watch: {
    currentCategories: {
      deep: true,
      handler () {
        var vm = this
        if (window.localStorage.getItem('token')) {
          var token = window.localStorage.getItem('token')
          var config = {
            headers: { Authorization: `Bearer ${token}` }
          }
          if (vm.currentCategories.lower === '전체') {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true&upper_category=${vm.currentCategories.upper}`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
                this.alertMessage = '옷 정보를 받아오는데 실패했습니다. 오류가 계속될 경우 관리자에게 연락해주세요!'
                this.showAlert = true
              })
          } else {
            axios.get(`${consts.SERVER_BASE_URL}/clothes/?me=true&lower_category=${vm.currentCategories.lower}`, config)
              .then((response) => {
                vm.clothes = response.data.results
              }).catch((ex) => {
                this.alertMessage = '옷 정보를 받아오는데 실패했습니다. 오류가 계속될 경우 관리자에게 연락해주세요!'
                this.showAlert = true
              })
          }
        }
      }
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
        this.alertMessage = '옷 정보를 받아오는데 실패했습니다. 오류가 계속될 경우 관리자에게 연락해주세요!'
        this.showAlert = true
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
