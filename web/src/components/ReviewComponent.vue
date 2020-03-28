<template>
<div id="review-row" class="row justify-content-center align-items-center">
    <div id="review-column" class="col-md-6">
        <form id="review-form" class="form" action="" method="post">
            <h3 class="text-center">Review</h3>
            <div class="col-md-4 closet_set_img"  v-bind:style="{ backgroundImage: 'url(' +require('../assets/hh.png')+ ')' }"></div>
            <!-- <div class="form-group text-left">
                <label for="place">활동 시간:</label><br/>
                <input type="datetime-local" name="place" class="form-control" placeholder="datetime-local input"><span>〜</span><input type="time">
            </div> -->
            <div class="form-group text-left">
                <label for="time">활동 시간:</label><br/>
                <input type="date" name="time" v-bind:style="{ padding: '10px;' }"> <input type="time"> <span>〜</span><input type="time">
            </div>
            <div class="form-group text-left">
                <label for="place">활동 장소:</label><br/>
                <input type="text" name="place" id="place" class="form-control">
            </div>
            <div class="form-group text-left">
                <label for="comment">한줄평:</label>
                <input type="text" name="comment" id="comment" class="form-control">
            </div>
            <div class="form-group">
                <input type="submit" name="submit" class="btn btn-md" value="확인">
            </div>
        </form>
    </div>
</div>
</template>

<script>
export default {
  name: 'reviewcomponent'
}
</script>

<style scoped>
  @import url("../css/login.css ");
.closet_set_img {
background-position: center;
background-repeat: no-repeat;
width: 100%;
height: 240px;
position: relative;
display: block;
margin: 0px auto;
}
label {
    display: inline-block;
    margin-bottom: .5rem;
    text-align: left;
}
h3{
    padding-bottom: 20px;
}
.review-form{
    padding-top: 50px;
}
.text-left {
    text-align: left;
    border-color: red;
}
</style>
