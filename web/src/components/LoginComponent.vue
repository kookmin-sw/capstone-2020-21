<template>
<div>
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
                                <input type="text" name="password" id="password" class="form-control" v-model="password">
                            </div>
                            <div class="form-group">
                                <input type="submit" name="submit" class="btn btn-md" value="Log In">
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
  name: 'logincomponent',
  data () {
    return {
      id: '',
      password: ''
    }
  }
}
</script>

<style scoped>
  @import url("../css/login.css ");
</style>
