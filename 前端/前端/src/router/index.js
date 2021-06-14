import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ReaderHome from '../views/ReaderHome.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'

import Welcome from '../components/Welcome.vue'
import Users from '../components/User/Users.vue'
import BookList from '../components/Books/BookList.vue'
import RecordList from '../components/Record/RecordList.vue'
import BorrowList from '../components/Borrow/BorrowList.vue'
import ReturnList from '../components/Return/ReturnList.vue'
import BuyBookList from '../components/BuyBook/BuyBookList.vue'

import ReaderUsers from '../components/User/ReaderUsers.vue'
import ReaderBookList from '../components/Books/ReaderBookList.vue'
import ReaderRecordList from '../components/Record/ReaderRecordList.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/Reader',
    name: 'ReaderHome',
    component: ReaderHome,
    redirect: '/Reader/Welcome',//这样就默认到home就直接去Welcome下面
    meta: { title: "图书馆信息管理系统" },
    children: [
      {
        path: '/Reader/Welcome',
        name: 'Welcome',
        component: Welcome,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/Reader/2',
        name: 'ReaderUsers',
        component: ReaderUsers,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/Reader/1',
        name: 'ReaderBookList',
        component: ReaderBookList,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/Reader/3',
        name: 'ReaderRecordList',
        component: ReaderRecordList,
        meta: { title: "图书馆信息管理系统" },
      },

    ]//在此处定义Home页面下的子路由
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    redirect: '/Welcome',//这样就默认到home就直接去Welcome下面
    meta: { title: "图书馆信息管理系统" },
    children: [
      {
        path: '/Welcome',
        name: 'Welcome',
        component: Welcome,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/2',
        name: 'Users',
        component: Users,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/1',
        name: 'BookList',
        component: BookList,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/3',
        name: 'RecordList',
        component: RecordList,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/4',
        name: 'BorrowList',
        component: BorrowList,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/5',
        name: 'ReturnList',
        component: ReturnList,
        meta: { title: "图书馆信息管理系统" },
      },
      {
        path: '/6',
        name: 'BuyBookList',
        component: BuyBookList,
        meta: { title: "图书馆信息管理系统" },
      },


    ]//在此处定义Home页面下的子路由
  },
  {
    path: '/Login',
    name: 'Login',
    component: Login,
    meta: { title: "图书馆信息管理系统" },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    //component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/Register',
    name: 'Register',
    component: Register,
    meta: { title: "图书馆信息管理系统" },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    //component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next();
  if (to.path === '/Register') return next();
  //获取token
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})


export default router
