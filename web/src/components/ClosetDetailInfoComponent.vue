<template>
<div class="info">
    <div class="text">
        <h1>{{ title }}</h1>
        <p>대분류 :</p>
        <p>소분류 :</p>
        <p>별칭 :</p>
    </div>
</div>
</template>

<script>
export default {
  name: 'ClosetDetailInfoComponent',
  props: ['title']
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
