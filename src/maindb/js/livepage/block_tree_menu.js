require('./styl/block_tree_menu.styl')

var report_block_tree_menu = {
    props:['ctx'],
    basename:'block-tree',
    template:`<div class="report-block-tree-menu">

    <div v-for="action in ctx.menu" class="block-btn" @click="next_level(action)">
        <span v-text="action.label"></span>
    </div>
    </div>`,
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    methods:{
        next_level(action){
            this.$root.open_live(window[action.open_editor] ,action.open_ctx,action.label)
        }
    }
}

Vue.component('com-live-block-tree-menu',report_block_tree_menu)
window.livepage_report_block_tree_menu