<template>
  <div>
    <b-row class="mb-3 justify-content-center">
      <b-img fluid-grow :src="image" />
    </b-row>
    <b-row>
      <b-form-file placeholder="이미지파일 업로드"
                    drop-placeholder="여기 놓아주세요!"
                    browse-text="찾아보기"
                    accept="image/jpeg, image/png, image/gif"
                    @change="onFileChange" />
    </b-row>
  </div>
</template>

<script>
export default {
  props: [
    'image'
  ],
  methods: {
    onFileChange (e) {
      var files = e.target.files || e.dataTransfer.files
      if (!files.length) return
      this.createImage(files[0])
    },
    createImage (file) {
      var reader = new FileReader()
      var vm = this
      reader.onload = (e) => {
        vm.$emit('update:image', e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

}
</script>

<style>

</style>
