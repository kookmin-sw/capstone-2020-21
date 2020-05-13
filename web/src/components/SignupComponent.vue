<template>
<b-container>
<div id="signup-row" class="row justify-content-center align-items-center">
    <div id="signup-column" class="col-md-4" style="margin-top:44px">
        <form id="signup-form" class="form" action="" method="post">
            <h3 class="text-center">Signup</h3>
            <div>
                <b-form-group id="input-group-1" label="ID* :" label-for="input-1">
                    <b-form-input id="input-1" v-model="form.id" type="id"></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="PASSWORD* :" label-for="input-2">
                    <b-form-input id="input-2" v-model="form.password" type="password"></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-3" label="NICKNAME* :" label-for="input-3">
                    <b-form-input id="input-3" v-model="form.nickname" type="nickname"></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-4" label="BIRTH :" label-for="input-4">
                    <b-form-input id="input-4" v-model="form.birth" type="birth" placeholder="yyyy-mm-dd"></b-form-input>
                </b-form-group>
                <b-form-group label-cols-sm="0" label-align-sm="right" class="mb-0">
                    <b-form-radio-group class="pt-2" :options="['남자', '여자']" v-model="form.gender" type="gender"></b-form-radio-group>
                </b-form-group>
            </div>
            <div>
              <b-row>
                  <b-col class="col-6" style="margin:0 auto">
                      <b-button pill class="w-75" type="new_submit" @click.prevent="handleSignup">확인</b-button>
                  </b-col>
              </b-row>
            </div>
        </form>
    </div>
</div>
</b-container>
</template>

<script>
import axios from 'axios'
import consts from '@/consts.js'

export default {
  name: 'signupcomponent',
  data () {
    return {
      form: {
        id: '',
        password: '',
        nickname: '',
        birth: '',
        gender: ''
      }
    }
  },
  methods: {
    handleSignup: function () {
      var token = ''
      axios.post(`${consts.SERVER_BASE_URL}/users/`, { username: this.form.id, password: this.form.password, nickname: this.form.nickname, gender: this.form.gender, birthday: this.form.birth })
        .then(response => {
        // TODO: delete console.log .
          console.log(response)
          token = response.data.access
          window.localStorage.setItem('token', token)
          this.$router.replace('/login/')
        })
        .then(ex => {
        // TODO: handle errors.
        })
    }
  }
}
</script>

<style>
</style>
