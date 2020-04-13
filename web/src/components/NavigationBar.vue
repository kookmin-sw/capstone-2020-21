<template>
  <b-navbar sticky class="shadow" toggleable="md" type="dark" style="background-color:#17A2B8">
    <b-navbar-brand class="font-weight-bold" to="/" style="font-size: large">
      <!-- 로고, OTTE 타이틀 -->
      <img src="../assets/logo.png" class="d-inline-block align-middle"
            style="width:32px; height:38px; margin-bottom:0; margin-right:5px" alt="logo">
      OTTE?
    </b-navbar-brand>

    <!-- 반응형 토글 -->
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <template v-if="isLoggedIn">
          <!-- 로그인시 -->
          <b-nav-item to="/closet">
            내 옷장
          </b-nav-item>
          <b-nav-item to="/cody">
            내 코디
          </b-nav-item>
          <b-nav-item @click="handleLogout">
            로그아웃
          </b-nav-item>
        </template>
        <template v-else>
          <!-- 비로그인시 -->
          <b-nav-item to="/login">
            로그인
          </b-nav-item>
          <b-nav-item to="/signup">
            회원가입
          </b-nav-item>
        </template>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  data: function () {
    return {
      isLoggedIn: false
    }
  },
  methods: {
    // TODO: implement logout function.
    handleLogout: function () {
      this.isLoggedIn = false
    },
    // TODO: implement login function, need to receive event from login component.
    handleLogin: function () {
      // to be implemented
      this.isLoggedIn = true
    }
  }
}
</script>
