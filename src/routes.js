import ShowFiles from './components/ShowFiles.vue'
import UploadPaper from './components/UploadPaper.vue'
import SingleBlog from './components/SingleBlog.vue'
import PrintLibrary from './components/PrintLibrary.vue'
import CheckOrder from './components/CheckOrder.vue'
import Login from './components/Login.vue'

export default[
    {
        path:"/",
        component:ShowFiles,
    },
    {
        path:"/login",
        component:Login,
    },
    {
        path:"/upload-paper",
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
        component:CheckOrder,
    }
]