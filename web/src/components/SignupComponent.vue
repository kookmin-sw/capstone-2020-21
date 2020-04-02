<template>
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
                            <!-- <div class="rad_style">
                                <div class="radio" style="margin-right:10px">
                                    <label>
                                        <input type="radio" name="optionsRadios" id="optionsRadios1" value="option1" checked>
                                        남
                                    </label>
                                </div>
                                <div class="radio">
                                    <label>
                                        <input type="radio" name="optionsRadios" id="optionsRadios2" value="option2">
                                        여
                                    </label>
                                </div>
                            </div> -->
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
</template>

<script>
export default {
  name: 'signupcomponent',
  data () {
    return {
      id: '',
      password: '',
      birth: ''
    }
  }
}
</script>

<style>
/* .rad_style{
    position: relative;
    margin: 20px 0px;
    align-items: center;
} */
</style>
