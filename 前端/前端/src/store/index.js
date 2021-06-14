import Vue from 'vue'
import Vuex from 'vuex'//用于多页面数据同步

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    count: 0,
    isLogin: false,
  },
  mutations: {
    increment(state) {
      state.count++;
    },
    login(state) {
      state.isLogin = true;
    },
    logout(state) {
      state.isLogin = false;
    },
  },
  getters: {
  },
  actions: {
  },
  modules: {
  }
})
