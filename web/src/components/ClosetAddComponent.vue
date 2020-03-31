<template>
  <div class="clothes_add">
      <div class="add_box">
          <div class="add_item">
            <div v-if="!image">
                <h3>옷과 색이 다른 배경에서 촬영해주세요</h3>
                <input type="file" @change="onFileChange">
            </div>
            <div v-else>
                <img :src="image" />
                <button @click="removeImage">Remove image</button>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'ClosetAddComponent',
  data () {
    return {
      image: ''
    }
  },
  methods: {
    onFileChange (e) {
      console.log('test', e)
      var files = e.target.files || e.dataTransfer.files
      if (!files.length) { return }
      this.createImage(files[0])
    },
    createImage (file) {
      var image = new Image()
      var reader = new FileReader()
      var vm = this

      reader.onload = (e) => {
        vm.image = e.target.result
      }
      reader.readAsDataURL(file)
    },
    removeImage: function (e) {
      this.image = ''
    }
  }
}
</script>

<style>
.clothes_add{
  display: inline-block;
  margin-right: 200px;
  margin-left: 200px;
}
.add_box{
  background-color: #faf5ef;
  border-color: #d3f4ff;
  border-style: solid;
  width: 500px;
  height: 500px;
  background-image: 100% 100%;
  text-align: center;
}
.add_item{
    margin-top: 200px;
}
img {
  width: 30%;
  margin: auto;
  display: block;
  margin-bottom: 10px;
}
</style>
