<template>
<div class="info">
    <div class="text">
        <h1>{{ title }}</h1>
        <p>{{ upper }}</p>
        <p>{{ lower }}</p>
        <p>{{ starname }}</p>
    </div>
</div>
</template>

<script>
export default {
  name: 'ClosetDetailInfoComponent',
  props: ['title', 'upper', 'lower', 'starname']
}
</script>

<style scoped>
.info{
    text-align: left;
    background-color: #faf5ef;
    border-color: #d3f4ff;
    border-style: solid;
    margin-bottom: 20px;
    position: relative;
}
.info > .text > p{
    margin-left: 20px;
    margin-top: 30px;
}
.info > .text > h1{
    margin-bottom: 50px;
    margin-top: 20px;
    text-align: center;
    text-decoration: underline;
}
</style>
