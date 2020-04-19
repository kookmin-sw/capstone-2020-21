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
                    <b-form-input id="input-4" v-model="form.birth" type="birth"></b-form-input>
                </b-form-group>
                <b-form-group label-cols-sm="0" label-align-sm="right" class="mb-0">
                    <b-form-radio-group class="pt-2" :options="['남', '여']"></b-form-radio-group>
                </b-form-group>
            </div>
            <div>
              <b-row>
                  <b-col class="col-6" style="margin:0 auto">
                      <b-button pill class="w-75" type="new_submit">확인</b-button>
                  </b-col>
              </b-row>
            </div>
        </form>
    </div>
</div>
</b-container>
</template>

<!--<template>
<div>
  <link href="/views/css/login.css" rel="stylesheet">
  <div id="signup">
        <div class="container">
            <div id="signup-row" class="row justify-content-center align-items-center">
                <div id="signup-column" class="col-md-6">
                    <div id="signup-box" class="col-md-12">
                        <form id="signup-form" class="form signup-form" action="" method="post" style="padding-top:100px">
                            <h3 class="text-center">Signup</h3>
                            <div class="form-group text-left">
                                <label for="id">ID* :</label>
                                <input type="text" name="id" id="id" class="form-control" v-model="id" required>
                            </div>
                            <div class="form-group text-left">
                                <label for="password">PASSWORD* :</label>
                                <input type="text" name="password" id="password" class="form-control" v-model="password" required>
                            </div>
                            <div class="form-group text-left">
                                <label for="nickname">NICKNAME* :</label>
                                <input type="text" name="nickname" id="nickname" class="form-control" required>
                            </div>
                            <div class="form-group text-left">
                                <label for="birthday">BIRTH:</label>
                                <input type="text" name="birthday" id="birthday" class="form-control" placeholder="YY/MM/DD" v-model="birth">
                            </div>
                            <b-form-group label-cols-sm="0" label-align-sm="right" class="mb-0">
                                <b-form-radio-group class="pt-2" :options="['남', '여']"></b-form-radio-group>
                            </b-form-group>
                            <div class="form-group" style="margin-top:30px">
                                <input type="submit" name="submit" class="btn btn-md" value="Sign up">
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>-->

<script>
export default {
  name: 'signupcomponent',
  data () {
    return {
      form: {
        id: '',
        password: '',
        birth: ''
      }
    }
  }
}
</script>

<style>
</style>
