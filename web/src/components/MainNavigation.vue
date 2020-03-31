<!--<link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>-->
<!------ Include the above in your HEAD tag ---------->
<template>
<div class="wrapper">
<!--Navigation Start-->
<nav class="navigation">
  <ul>
    <li class="home">
      <a href="/">Home</a>
    </li>
    <li>
      <a href="/closet">Closet</a>
      <ul class="children sub-menu">
        <li>
          <a href="/closet/detail">Closet_Detail</a>
        </li>
      </ul>
    </li>
    <li>
      <a href="/cody">Cody</a>
      <ul class="children sub-menu">
        <li>
          <a href="/cody/detail">Cody_Detail</a>
        </li>
      </ul>
    </li>
    <li>
      <a href="/review">Review</a>
    </li>
  </ul>
</nav>
<!--Navigation End-->
</div>
</template>

<script>
export default {}
</script>

<style>
.wrapper{
  float:left;
  width:100%;
  min-height:250px;
}
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
.navigation ul li:last-child{
    margin: 0;
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
.navigation .children {
    position: absolute;
    top: 100%;
    z-index: 1000;
    margin: 0;
    padding: 0;
    left: 0;
    min-width: 240px;
    background-color: #fff;
    border: solid 1px #dbdbdb;
    opacity: 0;
    -webkit-transform-origin: 0% 0%;
    transform-origin: 0% 0%;
    -webkit-transition: opacity 0.3s, -webkit-transform 0.3s;
    transition: opacity 0.3s, -webkit-transform 0.3s;
    transition: transform 0.3s, opacity 0.3s;
    transition: transform 0.3s, opacity 0.3s, -webkit-transform 0.3s;
}
.navigation ul li .children {
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
    -webkit-transform: rotateX(-75deg);
    transform: rotateX(-75deg);
    visibility: hidden;
}
.navigation ul li:hover > .children {
    -webkit-transform: rotateX(0deg);
    transform: rotateX(0deg);
    opacity: 1;
    visibility: visible;
}
.navigation ul li .children .children{
  left: 100%;
  top: 0;
}
.navigation ul li.last .children{
  right: 0;
  left: auto;
}
.navigation ul li.last .children .children{
  right: 100%;
  left: auto;
}
.navigation ul li .children li{
  float: left;
  width: 100%;
  margin:0;
}
.navigation ul li .children  a {
    display: block;
    font-family: "Montserrat", sans-serif;
    text-transform: uppercase;
    font-weight: 700;
    font-size: 11px;
    color: #333;
    text-align: left;
    line-height: 1.5em;
    padding: 16px 30px;
    letter-spacing: normal;
    border-bottom: 1px solid #dbdbdb;
    -webkit-transition: background-color 0.3s ease;
    transition: background-color 0.3s ease;
}
.navigation ul li .children  a:hover{
  color: #fff;
  background-color:goldenrod;
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
