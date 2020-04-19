<template>
<b-container>
<div id="review-row" class="row justify-content-center align-items-center">
    <div id="review-column" class="col-md-4" style="margin-top:44px">
        <form id="review-form" class="form" action="" method="post">
            <h3 class="text-center">Review</h3>
            <div class="col-md-4 closet_set_img"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/logo.png')+ ')' }"></div>
            <!-- <div class="form-group text-left">
                <input type="date" name="time" class="date" v-bind:style="{ padding: '10px;' }" style="margin-right:20px"> <input type="time" class="time"> <span> ~ </span><input type="time" class="time">
            </div> -->
            <div>
                <b-form @submit="onSubmit" @reset="onReset" v-if="show">
                <b-form-group id="input-group-1" label="활동시간 :" label-for="input-group-1">
                    <b-row>
                    <b-col md="auto">
                    <b-calendar v-model="form.date" @context="onContextdate" locale="en-US"></b-calendar>
                    </b-col>
                    <b-col md="auto">
                    <b-time v-model="form.time" locale="en" @context="onContexttime"></b-time>
                    </b-col>
                    </b-row>
                </b-form-group>
                <b-form-group id="input-group-2" label="활동장소 :" label-for="input-group-2">
                    <b-form inline>
                    <label class="col-1" for="inline-form-custom-select-pref">시</label>
                    <b-form-select id="inline-form-custom-select-pref" class="col-3" v-model="form.si" :options="si" required></b-form-select>
                    <label class="col-1" for="inline-form-custom-select-pref">구</label>
                    <b-form-select id="inline-form-custom-select-pref" class="col-3" v-model="form.gu" :options="gu" required></b-form-select>
                    <label class="col-1" for="inline-form-custom-select-pref">동</label>
                    <b-form-select id="inline-form-custom-select-pref" class="col-2" v-model="form.dong" :options="dong" required></b-form-select>
                    </b-form>
                </b-form-group>
                <b-form-group id="input-group-3" label="만족도 :" label-for="input-3">
                    <b-form-input id="range-1" v-model="form.range" type="range" min="1" max="5"></b-form-input>
                    <b-row>
                    <b-col class="col-2 text-left">1</b-col>
                    <b-col class="col-3">2</b-col>
                    <b-col class="col-2 text-center">3</b-col>
                    <b-col class="col-3">4</b-col>
                    <b-col class="col-2 text-right">5</b-col>
                    </b-row>
                    <b-row>
                    <b-col class="col-4 text-left">추웠다</b-col>
                    <b-col class="col-4">적당했다</b-col>
                    <b-col class="col-4 text-right">더웠다</b-col>
                    </b-row>
                </b-form-group>
                <b-form-group id="input-group-4" label="한줄평 :" label-for="input-4">
                    <b-form-input id="input-2" v-model="form.comment" type="comment"></b-form-input>
                </b-form-group>
                <!-- <b-row>
                    <b-col md="auto">
                    <b-form-group id="input-group-3" label="시:" label-for="input-3" for="inline-form-custom-select-pref">
                        <b-form-select id="input-3" v-model="form.si" :options="si" required></b-form-select>
                    </b-form-group>
                    </b-col>
                    <b-col md="auto">
                    <b-form-group id="input-group-4" label="구:" label-for="input-4">
                        <b-form-select id="input-4" v-model="form.gu" :options="gu" required></b-form-select>
                    </b-form-group>
                    </b-col>
                    <b-col md="auto">
                    <b-form-group id="input-group-5" label="동:" label-for="input-5">
                        <b-form-select id="input-5" v-model="form.dong" :options="dong" required></b-form-select>
                    </b-form-group>
                    </b-col>
                </b-row> -->
                </b-form>
            </div>
            <div>
                <b-row>
                    <b-col class="col-6">
                        <b-button pill class="w-75" type="new_submit">새 리뷰 작성하기</b-button>
                    </b-col>
                    <b-col class="col-6">
                        <b-button pill class="w-75" type="submit">확인</b-button>
                    </b-col>
                </b-row>
            </div>
        </form>
    </div>
</div>
</b-container>
</template>

<script>
export default {
  name: 'reviewcomponent',
  data () {
    return {
      form: {
        date: '',
        time: '',
        comment: '',
        range: ''
      },
      si: ['서울특별시', '양주시', '고양시'],
      gu: ['성북구', '종로구', '강북구'],
      dong: ['정릉동', '돈암1동'],
      show: true
    }
  },
  methods: {
    onContextdate (ctx) {
      this.context = ctx
    },
    onContexttime (ctx) {
      this.context = ctx
    },
    onSubmit (evt) {
      evt.preventDefault()
    },
    onReset (evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.comment = ''
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>

<style scoped>
  @import url("../css/login.css ");
.closet_set_img {
background-position: center;
background-repeat: no-repeat;
width: 100%;
height: 240px;
position: relative;
display: block;
/* margin: auto; */
margin-bottom: 30px;
background-size: 100% 100%;
}
.date{
    border-radius: 4px;
    border-color: rgb(245, 245, 245);
}
.time{
    border-radius: 4px;
    border-color: rgb(245, 245, 245);
}
label {
    display: inline-block;
    margin-bottom: .5rem;
    text-align: left;
}
h3{
    padding-bottom: 20px;
}
.review-form{
    padding-top: 50px;
}
.text-left {
    text-align: left;
}
</style>
