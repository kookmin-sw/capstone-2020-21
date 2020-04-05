<template>
<nav class="navigation" style="margin-top:50px">
  <ul>
    <li class="home">
      <a href="/">Home</a>
    </li>
    <li>
      <a href="/login">Log_In</a>
    </li>
    <li>
      <a href="/signup">Sign_Up</a>
    </li>
  </ul>
</nav>
</template>

<script>
export default {}
</script>

<style>
.navigation{
    float: left;
    width: 100%;
    text-align: center;
}
.navigation ul{
    margin: 0;
    padding: 0;
    float: none;
    width: auto;
    list-style: none;
    display: inline-block;
}
.navigation ul li{
    float: left;
    width: auto;
    margin-right: 60px;
    position: relative;
}
.navigation ul li a{
    float: left;
    width: 100%;
    color: #333;
    padding: 16px 0;
    font-size: 16px;
    line-height: normal;
    text-decoration:none;
    box-sizing:border-box;
    text-transform: uppercase;
    font-family: 'Montserrat', sans-serif;      -webkit-transition:color 0.3s ease;
    transition:color 0.3s ease;
}
.navigation ul li a:hover{
  color:goldenrod;
}
</style>

<!--<template>
<div>
  <div id="mainnavigation" class="container-fluid">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/closet">Closet</router-link> |
      <router-link to="/cody">Cody</router-link> |
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
</style>-->
