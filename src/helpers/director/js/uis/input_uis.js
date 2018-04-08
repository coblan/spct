// 这个文件夹里面的所有代码暂时不用了。
// 留下 com-multi-picture 好像是因为 color的feature时，用到了这个组件。
// com_file_uploader 包含了图片上传的所有功能，已经移到了director/inputs目录下
// 自己项目里面，其实可以把uis这个目录删除了。因为uis应该移到direcor(PC)或者f7(手机)目录下去



import {com_multi_picture} from './inputs/multi_picture.js'
import {com_file_uploader,field_file_uploader}  from './inputs/file_uploader.js'

Vue.component('com-multi-picture',com_multi_picture)
