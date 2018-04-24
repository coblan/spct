var com_search = {
    props:['head','search_args'],
    template:`<div>
    <input style="max-width: 20em;min-width: 10em;"
             type="text"
             name="_q"
             v-model='search_args._q'
             :placeholder='head.search_tip'
             @keyup.13="$emit('submit')"
             class='form-control input-sm'/>
    </div> `
}
Vue.component('com-search-filter',com_search)