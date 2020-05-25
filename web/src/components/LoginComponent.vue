<template>
<b-container>
<div id="login-row" class="row justify-content-center align-items-center">
    <div id="login-column" class="col-md-4" style="margin-top:44px">
        <form id="login-form" class="form" action="" method="post">
            <b-alert id="LoginAlert" v-model="showAlert" variant="danger" dismissible style="word-break: keep-all">
              {{ alertMessage }}
            </b-alert>
            <h3 class="text-center">Login</h3>
              <b-form-group id="input-group-1" label="ID :" label-for="input-1">
                  <b-form-input id="input-1" v-model="form.id"></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-1" label="PASSWORD :" label-for="input-2">
                  <b-form-input id="input-2" v-model="form.password" type="password"></b-form-input>
              </b-form-group>
              <b-row>
                  <b-col class="col-6" style="margin:0 auto">
                      <b-button pill class="w-75" @click.prevent="handleLogin">확인</b-button>
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
import { EventBus } from '@/event-bus.js'

export default {
  name: 'logincomponent',
  data () {
    return {
      form: {
        id: '',
        password: ''
      },
      alertMessage: '',
      showAlert: false
    }
  },
  methods: {
    handleLogin: function () {
      var token = ''
      axios.post(`${consts.SERVER_BASE_URL}/api/token/`, { username: this.form.id, password: this.form.password })
        .then(response => {
          token = response.data.access
          window.localStorage.setItem('token', token)
          EventBus.$emit('login-success')
          this.$router.push('/mainpage')
        })
        .catch(ex => {
          this.alertMessage = '로그인에 실패했습니다. 오류가 계속 될 경우, 관리자에게 연락해주세요.'
          this.showAlert = true
        })
    }
  }
}
</script>

<style scoped>
</style>
