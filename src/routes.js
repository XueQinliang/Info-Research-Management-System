import ShowFiles from './components/ShowFiles.vue'
import UploadPaper from './components/UploadPaper.vue'
import SinglePaper from './components/SinglePaper.vue'
import PrintLibrary from './components/PrintLibrary.vue'
import CheckPapers from './components/CheckPapers.vue'
import Login from './components/Login.vue'
import TeacherIndex from './components/TeacherIndex.vue'
import AlterPaper from './components/AlterPaper.vue'

export default[
    {
        path:"/",
        meta:{
            title:"首页"
        },
        component:ShowFiles,
    },
    {
        path:"/login",
        meta:{
            title:"登录-信息学院科研管理系统"
        },
        component:Login,
    },
    {
        path:"/upload-paper",
        meta:{
            title:"上传论文信息"
        },
        component:UploadPaper,
    },
    {
        path:"/paper_detail/:title/:author",
        meta:{
            title:"论文详细信息"
        },
        component:SinglePaper,
    },
    {
        path:"/print_order/:library",
        component:PrintLibrary,
    },
    {
        path:"/check_papers",
        meta:{
            title:"查看我的论文"
        },
        component:CheckPapers,
    },
    {
        path:"/teacher",
        meta:{
            title:"教师首页"
        },
        component:TeacherIndex
    },
    {
        path:"/teacher/paper_detail/:title/:author",
        meta:{
            title:"论文详细信息"
        },
        component:SinglePaper,
    },
    {
        path:"/teacher/alter_paper/:title/:author",
        meta:{
            title:"修改论文信息"
        },
        component:AlterPaper
    },
    {
        path:"/alter_paper/:title/:author",
        meta:{
            title:"修改论文信息"
        },
        component:AlterPaper
    }
]