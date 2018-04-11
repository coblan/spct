import {old} from './old.js'
import {network} from './network.js'
import {urlparse} from './urlparse.js'
import {collection} from  './collection.js'
import * as path from './patch.js'
import {cookie} from './cookie.js'
var ex={
    assign:function (dst,src) {
        for(var key in src){
            dst[key]=src[key]
        }
    },
}

ex.assign(ex,old)
ex.assign(ex,network)
ex.assign(ex,urlparse)
ex.assign(ex,collection)
ex.assign(ex,cookie)

window.ex = ex
