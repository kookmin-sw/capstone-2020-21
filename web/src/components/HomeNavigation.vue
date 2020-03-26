<template>
<div>
  <link href="/views/css/login.css" rel="stylesheet">
  <div id="homenavigation" class="container-fluid">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/Signup">Signup</router-link> |
    </div>
    <router-view/>
  </div>
</div>
</template>

<script>
export default {}
</script>

<style lang="scss">
#nav {
  padding: 30px;
  a {
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
