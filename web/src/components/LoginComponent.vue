<template>
<div id="login-row" class="row justify-content-center align-items-center">
    <div id="login-column" class="col-md-4" style="margin-top:44px">
        <form id="login-form" class="form" action="" method="post">
            <h3 class="text-center">Login</h3>
            <div>
              <b-form-group id="input-group-1" label="ID :" label-for="input-1">
                  <b-form-input id="input-1" v-model="form.id" type="id"></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-1" label="PASSWORD :" label-for="input-2">
                  <b-form-input id="input-2" v-model="form.password" type="password"></b-form-input>
              </b-form-group>
            </div>
            <div>
              <b-row>
                  <b-col class="col-6" style="margin:0 auto">
                      <b-button pill class="w-75" type="new_submit" @click.prevent="handleLogin">확인</b-button>
                  </b-col>
              </b-row>
            </div>
        </form>
    </div>
</div>
</template>

<!-- <template> -->
<!-- <div>
  <div id="login">
        <div class="container">
            <div id="login-row" class="row justify-content-center align-items-center">
                <div id="login-column" class="col-md-6">
                    <div id="login-box" class="col-md-12">
                        <form id="login-form" class="form" action="" method="post">
                            <h3 class="text-center">Login</h3>
                            <div class="form-group text-left">
                                <label for="id">ID:</label><br/>
                                <input type="text" name="id" id="id" class="form-control" v-model="id">
                            </div>
                            <div class="form-group text-left">
                                <label for="password">PASSWORD:</label>
                                <input type="password" name="password" id="password" class="form-control" v-model="password">
                            </div>
                            <div class="form-group">
                                <input type="submit" name="submit" class="btn btn-md" value="Log In" @click.prevent="handleLogin">
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div> -->
<!-- </template> -->

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
      }
    }
  },
  methods: {
    handleLogin: function () {
      var token = ''
      axios.post(`${consts.SERVER_BASE_URL}/api/token/`, { username: this.id, password: this.password })
        .then(response => {
          // TODO: delete console.log .
          console.log(response)
          token = response.data.access
          window.localStorage.setItem('token', token)
          EventBus.$emit('login-success')
          this.$router.go(-1)
        })
        .then(ex => {
          // TODO: handle errors.
        })
    }
  }
}
</script>

<style scoped>
  @import url("../css/login.css ");
</style>
