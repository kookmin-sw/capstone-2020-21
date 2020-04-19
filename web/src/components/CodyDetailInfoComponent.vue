<template>
<div class="info">
    <div class="text">
        <h1>{{ title }}</h1>
        <p>스타일
            <select v-model="selected_s" v-bind:disabled="is_disabled">
              <option v-for="category in list" v-bind:key="category" v-bind:value="category">{{ category }}</option>
            </select>
        </p>
        <p>별칭
            <input type="text" class="form-control" v-model="selected_t" v-bind:readonly="is_readonly">
        </p>
        <button @click="f1" class="btn btn-success" style="margin-left: 150px" >수정하기</button>
        <button @click="done" class="btn btn-success" style="margin-left: 20px">등록</button>

    </div>
</div>
</template>

<script>
export default {
  name: 'CodyDetailInfoComponent',
  props: ['title', 'list'],
  data () {
    return {
      selected_s: '',
      selected_t: '',
      is_readonly: true,
      is_disabled: true
    }
  },
  methods: {
    f1: function () {
      if (this.is_readonly && this.is_disabled) {
        this.is_readonly = false
        this.is_disabled = false
      } else {
        this.is_readonly = true
        this.is_disabled = true
      }
    },
    done: function (event) {
      alert('등록되었습니다')
    }
  }
}
</script>

<style scoped>
.info{
    text-align: left;
    background-color: #faf5ef;
    border-color: #d3f4ff;
    border-style: solid;
    margin-bottom: 20px;
    position: relative;
}
.info > .text > p{
    margin-left: 20px;
    margin-top: 30px;
}
.info > .text > h1{
    margin-bottom: 50px;
    margin-top: 20px;
    text-align: center;
    text-decoration: underline;
}
</style>
