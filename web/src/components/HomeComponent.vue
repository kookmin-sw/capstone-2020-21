<template>
<div>

  <div id="home">
      <!-- Header -->
  <header class="masthead d-flex">
    <div class="container text-center my-auto">
      <img src="../assets/logo.png" width="250" alt="로고">
      <h1 class="mb-1">OTTE 옷때?</h1>
      <h3 class="mb-5">
        <span class='text-primary'>O</span>
        <em>utfit </em><span class='text-primary'>T</span><em>oday </em>wea<span class='text-primary'>T</span><em>h</em><span class='text-primary'>E</span><em>r</em>
      </h3>
      <a class="btn btn-primary btn-xl" @click="goAbout()">about</a>
    </div>
    <div class="overlay"></div>
  </header>

  <!-- About -->
  <section class="content-section bg-light" id="about">
    <div class="container text-center">
      <div class="row">
        <div class="col-lg-10 mx-auto">
          <h1>OTTE? is the perfect website for you</h1>
        <br/>

          <p class="lead mb-5">Many people search for what to wear before going out in order to find appropriate clothes set for the weather. <br/>But even
          if they go through this process of searching, there are cases where they feel colder or hotter than what they have
          thought after getting out. Because every people feels different on how hot or cold about the same weather and also has
          different clothes to choose from, we are trying to help them resolve the problem<br/><br/>
          <span class="font-weight-bold"><mark>"What to wear today"</mark></span></p>
          <p class="lead mb-5">focusing on
          individual information.<br/><span class="lead mb-5">'OTTE?' stands for Outfit Today weaThEr, and it is a web service that helps the user to find appropriate clothes set for
          the weather they are about to face.</span></p>
          <br/>
        <br/>
          <a class="btn btn-dark btn-xl" @click="goDevelopers()">Developers</a>
        </div>
      </div>
    </div>
  </section>

  <!-- developers -->
  <section class="content-section bg-primary text-white text-center" id="developers">
    <div class="container">
      <div class="content-section-heading">
        <h3 class="text-secondary mb-0">Developers</h3>
        <h2 class="mb-5">Who we are?</h2>
      </div>
      <div class="row">
        <div class="col-12 col-md-6 col-lg-4">
          <span class="service-icon rounded-circle mx-auto mb-3" style="padding:8px 10px 0px 0px;">
            <img src="../assets/hh.png" class="img-circle" style="width: 100px; height: auto;" alt="현화">
          </span>
          <h5>
            <strong>송현화</strong>
          </h5>
          <p class="text-faded mb-0">User Interface 디자인, 프론트엔드 개발</p>
        <br/>
        </div>
        <div class="col-12 col-md-6 col-lg-4">
          <span class="service-icon rounded-circle mx-auto mb-3" style="padding:3px 4px 0px 0px;">
            <img src="../assets/jh.png" class="img-circle" style="width: 130px; height: auto;" alt="재호">
          </span>
          <h5>
            <strong>이재호</strong>
          </h5>
          <p class="text-faded mb-0">AWS 연결, API 서버 개발</p>
          <br/>
        </div>
        <div class="col-12 col-md-6 col-lg-4">
          <span class="service-icon rounded-circle mx-auto mb-3" style="padding:3px 10px 0px 0px;">
            <img src="../assets/yb.png" class="img-circle" style="width: 120px; height: auto;" alt="예빈">
          </span>
          <h5>
            <strong>정예빈</strong>
          </h5>
          <p class="text-faded mb-0">User Interface 디자인, 프론트엔드 개발</p>
          <br/>
        </div>
        <div class="col-12 col-md-6 col-lg-4">
          <span class="service-icon rounded-circle mx-auto mb-3" style="padding:10px">
            <img src="../assets/ms.png" class="img-circle" style="width: 125px; height: auto;" alt="민수">
          </span>
          <h5>
            <strong>권민수</strong>
          </h5>
          <p class="text-faded mb-0">API 서버 개발, 옷 분류 모델 개발</p>
          <br/>
        </div>
        <div class="col-12 col-md-6 col-lg-4">
          <span class="service-icon rounded-circle mx-auto mb-3" style="padding:3px 4px 0px 0px;">
            <img src="../assets/hb.png" class="img-circle" style="width: 120px; height: auto;" alt="효빈">
          </span>
          <h5>
            <strong>황효빈</strong>
          </h5>
          <p class="text-faded mb-0">AWS 연결, 데이터베이스 구축, API 서버 개발</p>
          <br/>
        </div>
        <div class="col-12 col-md-6 col-lg-4">
          <span class="service-icon rounded-circle mx-auto mb-3" style="padding:18px">
            <img src="../assets/gg.png" class="img-circle" style="width: 120px; height: auto;" alt="가구">
          </span>
          <h5>
            <strong>주가구</strong>
          </h5>
          <p class="text-faded mb-0">유닛 테스팅, 로고 제작</p>
          <br/>
        </div>
        </div>
    </div>
  </section>
  </div>
</div>
</template>

<script>

export default {
  name: 'HomeComponent',
  methods: {
    goAbout: function () {
      document.getElementById('about').scrollIntoView()
    },
    goDevelopers: function () {
      document.getElementById('developers').scrollIntoView()
    }
  }
}
</script>

<style>
    @import url("../css/Home.css");
    * {
    scroll-behavior: smooth;
  }
</style>
