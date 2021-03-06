// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import App from './App'
import Routes from './routes'
import AV from 'leancloud-storage'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap-select/dist/css/bootstrap-select.min.css'
import 'bootstrap-select/dist/js/bootstrap-select.min.js'
import axios from 'axios'

import $ from 'jquery'

Vue.prototype.$axios = axios

Vue.config.productionTip = false
Vue.use(VueResource)
Vue.use(VueRouter)
Vue.use(AV)

//自定义指令
/*Vue.directive('rainbow',{
  bind(el,binding,vnode){
    el.style.color = "#"+ Math.random().toString(16).slice(2,8);
  }
})*/
Vue.directive('theme',{
  bind(el,binding,vnode){
    if(binding.value == 'wide') {
      el.style.maxWidth = "1260px";
    }else if(binding.value == 'narrow'){
      el.style.maxWidth = "560px";
    }
    if(binding.arg == 'column'){
      el.style.background = "#6677cc";
      el.style.padding = '20px';
    }
  }
})

//自定义过滤器
//Vue.filter("to-uppercase",function(value){
  //return value.toUpperCase();
//})
Vue.filter("snippet",function(value){
  return value.slice(0,50) + "...";
})

//创建路由
const router = new VueRouter({
  routes: Routes,
  mode:"hash"
})

router.beforeEach((to, from, next) => {
    window.document.title = to.meta.title;
    if(to.path === "/login"){
      next()
    }else if(to.path.substring(0,13)==="/paper_detail"){
      if(sessionStorage.getItem('accessToken')){
        next()
      }else{
        next("/login")
      }
    }else if(to.path.substring(0,9)==="/download"){
      if(sessionStorage.getItem('accessToken')){
        next
      }else{
        next("/login")
      }
    }else if(to.path.substring(0,8) === "/teacher"){
      if(sessionStorage.getItem('accessToken')&&sessionStorage.getItem('identity')=='teacher'){
        next()
      }else{
        next("/login")
      }
    }else{
      if (sessionStorage.getItem('accessToken')&&sessionStorage.getItem('identity')=='student'){
        next()
      } else {
        next("/login")
    }
}
  })

//Leancloud
/*// 存储服务
var AV = require('leancloud-storage');
var { Query, User } = AV;
// 即时通讯服务
var { Realtime, TextMessage } = require('leancloud-realtime');
var AV = require('leancloud-storage/live-query');
*/


/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>',
  router:router
})
