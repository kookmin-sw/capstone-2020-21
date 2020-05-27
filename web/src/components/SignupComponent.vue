<template>
<b-container>
<div id="signup-row" class="row justify-content-center align-items-center">
    <div id="signup-column" class="col-md-4" style="margin-top:44px">
        <form id="signup-form" class="form" action="" method="post">
          <b-alert id="LoginAlert" v-model="showAlert" variant="danger" dismissible style="word-break: keep-all">
            {{ alertMessage }}
          </b-alert>
            <h3 class="text-center">Signup</h3>
              <b-form-group id="input-group-1" label="ID* :" label-for="input-1">
                  <b-form-input id="input-1" v-model="form.id"></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-2" label="PASSWORD* :" label-for="input-2">
                  <b-form-input id="input-2" v-model="form.password" type="password"></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-3" label="NICKNAME* :" label-for="input-3">
                  <b-form-input id="input-3" v-model="form.nickname"></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-4" label="BIRTH :" label-for="input-4">
                  <b-form-input id="input-4" v-model="form.birth" placeholder="yyyy-mm-dd"></b-form-input>
              </b-form-group>
              <b-form-group label-cols-sm="0" label-align-sm="right" class="mb-0">
                  <b-form-radio-group class="pt-2" :options="['남자', '여자']" v-model="form.gender"></b-form-radio-group>
              </b-form-group>
              <b-row>
                <b-col class="col-6" style="margin:0 auto">
                    <b-button pill class="w-75" @click.prevent="handleSignup">확인</b-button>
                </b-col>
              </b-row>
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
      },
      alertMessage: '',
      showAlert: false
    }
  },
  methods: {
    handleSignup: function () {
      var token = ''
      axios.post(`${consts.SERVER_BASE_URL}/users/`, { username: this.form.id, password: this.form.password, nickname: this.form.nickname, gender: this.form.gender, birthday: this.form.birth })
        .then(response => {
          token = response.data.access
          window.localStorage.setItem('token', token)
          this.$router.replace('/login/')
        })
        .catch(ex => {
          this.alertMessage = '회원 가입에 실패했습니다. 오류가 계속 될 경우, 관리자에게 연락해주세요.'
          this.showAlert = true
        })
    }
  }
}
</script>

<style>
</style>
