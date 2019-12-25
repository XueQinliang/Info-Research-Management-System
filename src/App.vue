<template>
  <div id="app">
    <!--<add-blog></add-blog>-->
    <!--<show-blogs></show-blogs>-->
    <blog-header v-if="isshow"></blog-header>
    <router-view @header='showheader'></router-view>
  </div>
</template>

<script>
import UploadPaper from './components/UploadPaper'
import ShowFiles from './components/ShowFiles'
import BlogHeader from './components/BlogHeader'
import PrintLibrary from './components/PrintLibrary'
import CheckOrder from './components/CheckOrder'
import Login from './components/Login'

export default {
  name: 'App',
  components: {
    UploadPaper,ShowFiles,BlogHeader,PrintLibrary,CheckOrder,Login
  },
  data(){
    return{
      isshow:true,
    }
  },
  methods:{
    showheader(bool){
      this.isshow = bool
    }
  }
}
</script>

<style>

</style>
