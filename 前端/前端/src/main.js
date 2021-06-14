import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import './assets/CSS/Global.css'//导入全局样式表

import global from "./components/Global.js";
import qs from 'qs'      //引入qs

Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.prototype.$http = axios//将http定义为全局变量，将axios挂载到http上
axios.defaults.baseURL = ' http://127.0.0.1:8000'    //通过这种方式向服务器发出获取数据的请求
Vue.prototype.$qs = qs

Vue.prototype.global = global//用于传递登录用户信息

//接下来通过axios请求拦截器添加token，保证拥有获取数据的权限
// （ token就是比如向浏览器验证过一次密码了，验证正确了，就会给一个token令牌，路由器页面跳转的时候，查看有没有token令牌就行，就不用了再反复验证密码了）
axios.interceptors.request.use(config => {//获取了请求拦截器对象
  console.log(config)
  config.headers.HTTP2_HEADER_AUTHORIZATION = window.sessionStorage.getItem('token');
  return config;
})//这里的config就是请求对象

new Vue({
  router,
  store,
  render: h => h(App)//箭头函数，括号内为参数，箭头指向返回值
}).$mount('#app')

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})
