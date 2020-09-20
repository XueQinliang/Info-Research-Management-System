<template>
  <div id="app">
      <!--<add-blog></add-blog>-->
      <!--<show-blogs></show-blogs>-->
      <blog-header v-if="isshow"></blog-header>
      <blog-header-t v-if="isshow_t"></blog-header-t>
      <router-view></router-view>
  </div>
</template>

<script>
import UploadPaper from './components/UploadPaper'
import ShowFiles from './components/ShowFiles'
import BlogHeader from './components/BlogHeader'
import PrintLibrary from './components/PrintLibrary'
import CheckPapers from './components/CheckPapers'
import Login from './components/Login'
import TeacherIndex from './components/TeacherIndex'
import BlogHeaderT from './components/BlogHeaderT'
import AlterPaper from './components/AlterPaper'
import ImportSid from './components/ImportSid'


export default {
  name: 'App',
  components: {
    UploadPaper,ShowFiles,BlogHeader,PrintLibrary,CheckPapers,Login,TeacherIndex,BlogHeaderT,AlterPaper,ImportSid
  },
  data(){
    return{
      isshow:true,
      isshow_t:true
    }
  },
  updated(){
    console.log(this.$route.path)
    if(this.$route.path ==='/login'){
      this.isshow = false
      this.isshow_t = false
    }else if(this.$route.path.substring(0,8)==='/teacher'){
      this.isshow = false
      this.isshow_t = true
    }else{
      this.isshow = true
      this.isshow_t = false
    }
  },
  created(){
    console.log(this.$route.path)
    if(this.$route.path ==='/login'){
      this.isshow = false
      this.isshow_t = false
    }else if(this.$route.path.substring(0,8)==='/teacher'){
      this.isshow = false
      this.isshow_t = true
    }else{
      this.isshow = true
      this.isshow_t = false
    }
  },
  methods:{
    // showheader(bool){
    //   console.log(this.$route.path)
    //   this.isshow = bool
    // }
  }
}
</script>

<style>

</style>
