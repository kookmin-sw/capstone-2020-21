import Vue from 'vue'
import Router from 'vue-router'
import Login from './views/Login.vue'
import Signup from './views/Signup.vue'
import Home from './views/Home.vue'
import Closet from './views/Closet.vue'
import Review from './views/Review.vue'
import ClosetDetail from './views/ClosetDetail.vue'
import Main from './views/Main.vue'
import ClosetAdd from './views/ClosetAdd.vue'
import Cody from './views/Cody.vue'
import CodyAdd from './views/CodyAdd.vue'
import CodyDetail from './views/CodyDetail.vue'
import Bridge from './views/Bridge.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/closet',
      name: 'Closet',
      component: Closet
    },
    {
      path: '/review',
      name: 'Review',
      component: Review,
      props: true
    },
    {
      path: '/closet/detail',
      name: 'ClosetDetail',
      component: ClosetDetail,
      props: true
    },
    {
      path: '/mainpage',
      name: 'Main',
      component: Main
    },
    {
      path: '/closet/add',
      name: 'ClosetAdd',
      component: ClosetAdd
    },
    {
      path: '/cody',
      name: 'Cody',
      component: Cody
    },
    {
      path: '/cody/add',
      name: 'CodyAdd',
      component: CodyAdd
    },
    {
      path: '/cody/detail',
      name: 'CodyDetail',
      component: CodyDetail,
      props: true
    },
    {
      path: '/bridge',
      name: 'Bridge',
      component: Bridge,
      props: true
    }
  ]
})
