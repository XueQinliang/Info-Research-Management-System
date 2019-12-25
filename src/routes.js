import ShowFiles from './components/ShowFiles.vue'
import UploadPaper from './components/UploadPaper.vue'
import SingleBlog from './components/SingleBlog.vue'
import PrintLibrary from './components/PrintLibrary.vue'
import CheckOrder from './components/CheckOrder.vue'
import Login from './components/Login.vue'

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
        path:"/blog_detail/:id",
        component:SingleBlog,
    },
    {
        path:"/print_order/:library",
        component:PrintLibrary,
    },
    {
        path:"/check_order",
        meta:{
            title:"查看我的论文"
        },
        component:CheckOrder,
    }
]