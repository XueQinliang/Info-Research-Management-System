<template>
  <div id="app">
    <!--<add-blog></add-blog>-->
    <!--<show-blogs></show-blogs>-->
    <blog-header></blog-header>
    <router-view></router-view>
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
  }
}
</script>

<style>

</style>
