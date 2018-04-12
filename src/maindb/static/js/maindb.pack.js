/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 20);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var ajax_fields = {
    props: ['kw'],
    data: function data() {
        return {
            heads: this.kw,
            errors: {},
            row: {}
            //fields_kw:{
            //    heads:this.kw,
            //    errors:{},
            //    row:{}
            //}
        };
    },
    mixins: [mix_fields_data, mix_nice_validator],
    template: '<div>\n    <div style="margin: 5px 1em;">\n        <button type="button" class="btn btn-default" title="\u4FDD\u5B58" @click="save()"><i class="fa fa-save"></i><span>\u4FDD\u5B58</span></button>\n    </div>\n\n    <form class=\'field-panel msg-hide\' id="form">\n\t\t<field  v-for=\'head in heads\' :key="head.name" :head="head" :row=\'row\'></field>\n\t</form></div>'

    // data_getter  回调函数，获取数据,


};

Vue.component('com_ajax_fields', ajax_fields);

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var ajax_table = {
    props: ['kw'], //['heads','row_filters','kw'],
    data: function data() {
        return {
            heads: this.kw.heads,
            row_filters: this.kw.row_filters,

            row_sort: this.kw.row_sort,
            rows: [],
            row_pages: {},
            //search_tip:this.kw.search_tip,

            selected: [],
            del_info: [],

            can_add: this.kw.can_add,
            can_del: this.kw.can_del,
            can_edit: this.kw.can_edit,

            search_args: {}
        };
    },
    mixins: [mix_table_data, mix_v_table_adapter],
    //watch:{
    //    // 排序变换，获取数据
    //    'row_sort.sort_str':function(v){
    //        this.search_args._sort=v
    //        this.get_data()
    //    }
    //},
    template: '<div class="rows-block">\n        <div class=\'flex\' style="min-height: 3em;" v-if="row_filters.length > 0">\n            <com-filter class="flex" :heads="row_filters" :search_args="search_args"\n                        @submit="search()"></com-filter>\n            <div class="flex-grow"></div>\n        </div>\n        <div class="box box-success">\n            <div class="table-wraper">\n                <v-table ref="vtable"\n                         is-horizontal-resize\n                         is-vertical-resize\n                         :title-row-height="30"\n                         :vertical-resize-offset="80"\n                         :row-height="24"\n                         odd-bg-color="#f0f6f8"\n                         column-width-drag\n                         style="width: 100%;"\n                         :columns="columns"\n                         :table-data="rows"\n                         @sort-change="sortChange"\n                         row-hover-color="#eee"\n                         row-click-color="#edf7ff">\n                </v-table>\n            </div>\n            <div style="margin-top: 10px;">\n                <v-pagination @page-change="get_page($event)"\n                              :total="row_pages.total"\n                              size="small"\n                              :page-size="row_pages.perpage"\n                              @page-size-change="on_perpage_change($event)"\n                              :layout="[\'total\', \'prev\', \'pager\', \'next\', \'sizer\', \'jumper\']">\n                </v-pagination>\n            </div>\n        </div>\n    </div>',

    methods: {
        del_item: function del_item() {
            if (this.selected.length == 0) {
                return;
            }
            var del_obj = {};
            for (var j = 0; j < this.selected.length; j++) {
                var pk = this.selected[j];
                for (var i = 0; i < this.rows.length; i++) {
                    if (this.rows[i].pk.toString() == pk) {
                        if (!del_obj[this.rows[i]._class]) {
                            del_obj[this.rows[i]._class] = [];
                        }
                        del_obj[this.rows[i]._class].push(pk);
                    }
                }
            }
            var out_str = '';
            for (var key in del_obj) {
                out_str += key + ':' + del_obj[key].join(':') + ',';
            }
            location = ex.template("{engine_url}/del_rows?rows={rows}&next={next}", { engine_url: engine_url,
                rows: encodeURI(out_str),
                next: encodeURIComponent(location.href) });
        },
        goto_page: function goto_page(page) {
            this.search_args._page = page;
            this.search();
        },
        add_new: function add_new() {
            var url = ex.template('{engine_url}/{page}.edit/?next={next}', {
                engine_url: engine_url,
                page: page_name,
                next: encodeURIComponent(ex.appendSearch(location.pathname, search_args))
            });
            location = url;
        }
    }
};

Vue.component('com_ajax_table', ajax_table);

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Vue.component('com-pop-fields', {
    props: ['row', 'heads', 'ops'],
    mixins: [mix_fields_data, mix_nice_validator],
    methods: {
        on_operat: function on_operat(name) {
            if (name == 'save') {
                this.save();
            }
        },
        before_save: function before_save() {
            eventBus.$emit('sync_data');
            if (this.nice_validator.isValid()) {
                return true;
            } else {
                return false;
            }
        },
        after_save: function after_save(new_row) {
            this.$emit('sub_success', { new_row: new_row, old_row: this.row });
            ex.assign(this.row, new_row);
        },
        del_row: function del_row() {
            var self = this;
            layer.confirm('真的删除吗?', { icon: 3, title: '确认' }, function (index) {
                layer.close(index);
                var ss = layer.load(2);
                var post_data = [{ fun: 'del_rows', rows: [self.row] }];
                $.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    layer.close(ss);
                    self.$emit('del_success', self.row);
                });
            });
        }

    },
    template: '<div class="flex-v" style="margin: 0;height: 100%;">\n    <div>\n        <component v-for="op in ops" :is="op.editor" @operate="on_operat(op.name)" :head="op"></component>\n        <!--<button @click="save()">\u4FDD\u5B58</button>-->\n        <!--<button @click="del_row()" v-if="row.pk">\u5220\u9664</button>-->\n    </div>\n    <div class = "flex-grow" style="overflow: scroll;margin: 0;">\n        <div class="field-panel msg-hide" >\n            <field  v-for="head in heads" :key="head.name" :head="head" :row="row"></field>\n        </div>\n    </div>\n     </div>',
    data: function data() {
        return {
            fields_kw: {
                heads: this.heads,
                row: this.row,
                errors: {}
            }
        };
    }
});

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var label_shower = {
    props: ['row', 'head'],
    template: '<div><span v-if=\'head.readonly\' v-text=\'label\'></span></div>',
    computed: {
        label: function label() {
            return this.row['_' + this.head.name + '_label'];
        }
    }
};

Vue.component('com-field-label-shower', label_shower);

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Vue.component('com-field-op-btn', {
    props: ['head'],
    template: '<button @click="$emit(\'operate\')"><span v-text="head.label"></span></button>'

});

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var mix_fields_data = {
    methods: {
        get_data: function get_data() {
            this.data_getter(this);
        },
        set_errors: function set_errors(errors) {
            ex.each(this.heads, function (head) {
                if (errors[head.name]) {
                    Vue.set(head, 'error', errors[head.name].join(';'));
                } else {
                    Vue.set(head, 'error', null);
                }
            });
        },
        save: function save() {
            var self = this;
            if (!self.before_save()) {
                return;
            }
            //var loader = layer.load(2)
            cfg.show_load();

            var post_data = [{ fun: 'save', row: this.row }];
            var url = ex.appendSearch('/d/ajax', search_args);
            ex.post(url, JSON.stringify(post_data), function (resp) {
                //layer.close(loader)
                if (resp.save.errors) {
                    cfg.hide_load();
                    self.set_errors(resp.save.errors);
                    self.show_error(resp.save.errors);
                } else {
                    cfg.hide_load(2000);
                    //layer.msg('保存成功',{time:2000})
                    self.after_save(resp.save.row);
                    self.set_errors({});
                }
            });
        },
        before_save: function before_save() {
            eventBus.$emit('sync_data');
            return true;
        },
        after_save: function after_save(new_row) {
            ex.assign(this.row, new_row);
        },
        show_error: function show_error(errors) {
            var str = "";
            for (var k in errors) {
                str += k + ':' + errors[k] + '<br>';
            }
            layer.confirm(str, { title: ['错误', 'color:white;background-color:red'] });
        },
        clear: function clear() {
            this.row = {};
            this.set_errors({});
        }

    }
};

window.mix_fields_data = mix_fields_data;

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var nice_validator = {
    mounted: function mounted() {
        var self = this;
        var validator = {};
        ex.each(this.heads, function (head) {
            if (head.required) {
                validator[head.name] = 'required';
            }
        });
        this.nice_validator = $(this.$el).find('.field-panel').validator({
            fields: validator
        });
    }
};

window.mix_nice_validator = nice_validator;

/***/ }),
/* 7 */,
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var mix_v_table_adapter = {

    mounted: function mounted() {
        eventBus.$on('content_resize', this.resize);
    },
    computed: {
        columns: function columns() {
            var self = this;
            var first_col = {
                width: 60,
                titleAlign: 'center',
                columnAlign: 'center',
                type: 'selection'
            };
            var cols = [first_col];
            var converted_heads = ex.map(this.heads, function (head) {
                var col = ex.copy(head);
                var dc = {
                    field: head.name,
                    title: head.label,
                    isResize: true
                };
                if (head.editor) {
                    dc.componentName = head.editor;
                }
                if (ex.isin(head.name, self.row_sort.sortable)) {
                    dc.orderBy = '';
                }
                ex.assign(col, dc);
                if (!col.width) {
                    col.width = 200;
                }
                return col;
            });
            cols = cols.concat(converted_heads);
            return cols;
        }
    },
    methods: {
        resize: function resize() {
            var self = this;
            $(self.$refs.vtable.$el).find('.v-table-rightview').css('width', '100%');
            $(self.$refs.vtable.$el).find('.v-table-header').css('width', '100%');
            $(self.$refs.vtable.$el).find('.v-table-body').css('width', '100%');

            var tmid = setInterval(function () {
                self.$refs.vtable.resize();
            }, 50);
            setTimeout(function () {
                //self.$refs.vtable.resize()
                clearInterval(tmid);
            }, 600);
        },
        on_perpage_change: function on_perpage_change(perpage) {
            this.search_args._perpage = perpage;
            this.search_args._page = 1;
            this.get_data();
        },
        sortChange: function sortChange(params) {
            var self = this;
            ex.each(this.row_sort.sortable, function (name) {
                if (params[name]) {
                    if (params[name] == 'asc') {
                        self.search_args._sort = name;
                    } else {
                        self.search_args._sort = '-' + name;
                    }
                    return 'break';
                }
            });
            this.get_data();
        }
    }
};
window.mix_v_table_adapter = mix_v_table_adapter;

/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var label_shower = {
    props: ['rowData', 'field', 'index'],
    template: '<span v-text="rowData[label]"></span>',
    data: function data() {
        return {
            label: '_' + this.field + '_label'
        };
    }
};

Vue.component('com-table-label-shower', label_shower);

/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var line_text = {
    props: ['rowData', 'field', 'index'],
    template: '<div ><input @change="on_changed()" style="width: 100%" type="text" v-model="rowData[field]"></div>',
    data: function data() {
        return {};
    },
    methods: {
        on_changed: function on_changed() {
            this.$emit('on-custom-comp', { name: 'row-changed', row: this.rowData });
        }
    }
};

Vue.component('com-table-linetext', line_text);

/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var mapper = {
    props: ['rowData', 'field', 'index'],
    template: '<span v-text="show_data"></span>',
    created: function created() {
        // find head from parent table
        var table_par = this.$parent;
        while (true) {
            if (table_par.heads) {
                break;
            }
            table_par = table_par.$parent;
            if (!table_par) {
                break;
            }
        }
        this.table_par = table_par;
    },
    computed: {
        show_data: function show_data() {
            if (this.table_par) {
                var value = this.rowData[this.field];
                var head = ex.findone(this.table_par.heads, { name: this.field });
                var options = head.options;
                return options[value];
            }
        }
    }
};

Vue.component('com-table-mapper', mapper);

/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var picture = {
    props: ['rowData', 'field', 'index'],
    template: '<span>\n        <img @click="open()" :src="rowData[field]" alt="" height="96px" style="cursor: pointer;">\n        </span>',
    methods: {
        open: function open() {
            window.open(this.rowData[this.field]);
        }
    }
};

Vue.component('com-table-picture', picture);

/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var pop_fields = {
    template: '<span v-text="rowData[field].label" @click="edit_me()" class="clickable"></span>',
    props: ['rowData', 'field', 'index'],
    created: function created() {
        // find head from parent table
        var table_par = this.$parent;
        while (true) {
            if (table_par.heads) {
                break;
            }
            table_par = table_par.$parent;
            if (!table_par) {
                break;
            }
        }
        if (table_par) {
            var value = this.rowData[this.field];
            this.head = ex.findone(table_par.heads, { name: this.field });
        }
    },
    methods: {
        edit_me: function edit_me() {
            this.open_layer();
        },
        open_layer: function open_layer() {
            var self = this;
            var id = new Date().getTime();
            var pk = this.rowData[this.field].pk;
            var model_name = this.head.model_name;
            var ops = this.head.ops;
            self.opened_layer_indx = layer.open({
                type: 1,
                area: ['700px', '400px'],
                shadeClose: true, //点击遮罩关闭
                content: '<div id="fields-pop-' + id + '" style="height: 100%;">\n                    <com-pop-fields @del_success="on_del()" @sub_success="on_sub_success($event)"\n                    :row="row" :heads="fields_heads" :ops="ops"></com-pop-fields>\n                </div>'
            });
            //var copy_fields_heads = ex.copy(fields_heads)
            new Vue({
                el: '#fields-pop-' + id,
                data: {
                    row: {},
                    fields_heads: this.head.fields_heads,
                    pk: pk,
                    ops: ops
                },
                mounted: function mounted() {
                    var self = this;
                    cfg.show_load();
                    var post_data = [{ fun: 'get_row', pk: this.pk, model_name: model_name }];
                    ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                        self.row = resp.get_row;
                        cfg.hide_load();
                    });
                },
                methods: {
                    on_sub_success: function on_sub_success(event) {
                        // 将新建的row 插入到表格中
                        var old_row = event.old_row;
                        var new_row = event.new_row;
                        if (!old_row.pk) {
                            self.rows.splice(0, 0, new_row);
                        } else {
                            ex.assign(row, new_row);
                        }
                    },
                    on_del: function on_del() {
                        ex.remove(self.rows, row);
                        layer.close(self.opened_layer_indx);
                    }
                }
            });
        }
    }
};
Vue.component('com-table-pop-fields', pop_fields);

/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


// 无用了。准备删除
var delete_op = {
    props: ['name'],
    template: ' <a class="clickable" @click="delete_op()" :disabled="!enable">\u5220\u9664</a>',
    data: function data() {
        return {
            enable: false
        };
    },
    methods: {
        delete_op: function delete_op() {
            this.$emit('operation', this.name);
        },
        set_enable: function set_enable(yes) {
            this.enable = yes;
        }
    }
};
Vue.component('com-op-delete', delete_op);

/***/ }),
/* 15 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var op_a = {
    props: ['head'],
    template: ' <a class="clickable" @click="operation_call()" :disabled="!enable" v-text="head.label" ></a>',
    data: function data() {
        return {
            enable: true
        };
    },
    methods: {
        operation_call: function operation_call() {
            this.$emit('operation', this.head.name);
        },
        set_enable: function set_enable(yes) {
            this.enable = yes;
        }
    }
};
Vue.component('com-op-a', op_a);

/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(17);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(19)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./fields.scss", function() {
			var newContent = require("!!../../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./fields.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(18)();
// imports


// module
exports.push([module.i, ".msg-hide .field .msg {\n  display: none; }\n\n.field .picture {\n  position: relative; }\n  .field .picture .msg-box {\n    position: absolute;\n    left: 260px; }\n", ""]);

// exports


/***/ }),
/* 18 */
/***/ (function(module, exports) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
module.exports = function() {
	var list = [];

	// return the list of modules as css string
	list.toString = function toString() {
		var result = [];
		for(var i = 0; i < this.length; i++) {
			var item = this[i];
			if(item[2]) {
				result.push("@media " + item[2] + "{" + item[1] + "}");
			} else {
				result.push(item[1]);
			}
		}
		return result.join("");
	};

	// import a list of modules into the list
	list.i = function(modules, mediaQuery) {
		if(typeof modules === "string")
			modules = [[null, modules, ""]];
		var alreadyImportedModules = {};
		for(var i = 0; i < this.length; i++) {
			var id = this[i][0];
			if(typeof id === "number")
				alreadyImportedModules[id] = true;
		}
		for(i = 0; i < modules.length; i++) {
			var item = modules[i];
			// skip already imported module
			// this implementation is not 100% perfect for weird media query combinations
			//  when a module is imported multiple times with different media queries.
			//  I hope this will never occur (Hey this way we have smaller bundles)
			if(typeof item[0] !== "number" || !alreadyImportedModules[item[0]]) {
				if(mediaQuery && !item[2]) {
					item[2] = mediaQuery;
				} else if(mediaQuery) {
					item[2] = "(" + item[2] + ") and (" + mediaQuery + ")";
				}
				list.push(item);
			}
		}
	};
	return list;
};


/***/ }),
/* 19 */
/***/ (function(module, exports) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
var stylesInDom = {},
	memoize = function(fn) {
		var memo;
		return function () {
			if (typeof memo === "undefined") memo = fn.apply(this, arguments);
			return memo;
		};
	},
	isOldIE = memoize(function() {
		return /msie [6-9]\b/.test(self.navigator.userAgent.toLowerCase());
	}),
	getHeadElement = memoize(function () {
		return document.head || document.getElementsByTagName("head")[0];
	}),
	singletonElement = null,
	singletonCounter = 0,
	styleElementsInsertedAtTop = [];

module.exports = function(list, options) {
	if(typeof DEBUG !== "undefined" && DEBUG) {
		if(typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};
	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (typeof options.singleton === "undefined") options.singleton = isOldIE();

	// By default, add <style> tags to the bottom of <head>.
	if (typeof options.insertAt === "undefined") options.insertAt = "bottom";

	var styles = listToStyles(list);
	addStylesToDom(styles, options);

	return function update(newList) {
		var mayRemove = [];
		for(var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];
			domStyle.refs--;
			mayRemove.push(domStyle);
		}
		if(newList) {
			var newStyles = listToStyles(newList);
			addStylesToDom(newStyles, options);
		}
		for(var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];
			if(domStyle.refs === 0) {
				for(var j = 0; j < domStyle.parts.length; j++)
					domStyle.parts[j]();
				delete stylesInDom[domStyle.id];
			}
		}
	};
}

function addStylesToDom(styles, options) {
	for(var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];
		if(domStyle) {
			domStyle.refs++;
			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}
			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];
			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}
			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles(list) {
	var styles = [];
	var newStyles = {};
	for(var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};
		if(!newStyles[id])
			styles.push(newStyles[id] = {id: id, parts: [part]});
		else
			newStyles[id].parts.push(part);
	}
	return styles;
}

function insertStyleElement(options, styleElement) {
	var head = getHeadElement();
	var lastStyleElementInsertedAtTop = styleElementsInsertedAtTop[styleElementsInsertedAtTop.length - 1];
	if (options.insertAt === "top") {
		if(!lastStyleElementInsertedAtTop) {
			head.insertBefore(styleElement, head.firstChild);
		} else if(lastStyleElementInsertedAtTop.nextSibling) {
			head.insertBefore(styleElement, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			head.appendChild(styleElement);
		}
		styleElementsInsertedAtTop.push(styleElement);
	} else if (options.insertAt === "bottom") {
		head.appendChild(styleElement);
	} else {
		throw new Error("Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.");
	}
}

function removeStyleElement(styleElement) {
	styleElement.parentNode.removeChild(styleElement);
	var idx = styleElementsInsertedAtTop.indexOf(styleElement);
	if(idx >= 0) {
		styleElementsInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement(options) {
	var styleElement = document.createElement("style");
	styleElement.type = "text/css";
	insertStyleElement(options, styleElement);
	return styleElement;
}

function createLinkElement(options) {
	var linkElement = document.createElement("link");
	linkElement.rel = "stylesheet";
	insertStyleElement(options, linkElement);
	return linkElement;
}

function addStyle(obj, options) {
	var styleElement, update, remove;

	if (options.singleton) {
		var styleIndex = singletonCounter++;
		styleElement = singletonElement || (singletonElement = createStyleElement(options));
		update = applyToSingletonTag.bind(null, styleElement, styleIndex, false);
		remove = applyToSingletonTag.bind(null, styleElement, styleIndex, true);
	} else if(obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function") {
		styleElement = createLinkElement(options);
		update = updateLink.bind(null, styleElement);
		remove = function() {
			removeStyleElement(styleElement);
			if(styleElement.href)
				URL.revokeObjectURL(styleElement.href);
		};
	} else {
		styleElement = createStyleElement(options);
		update = applyToTag.bind(null, styleElement);
		remove = function() {
			removeStyleElement(styleElement);
		};
	}

	update(obj);

	return function updateStyle(newObj) {
		if(newObj) {
			if(newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap)
				return;
			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;
		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag(styleElement, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (styleElement.styleSheet) {
		styleElement.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = styleElement.childNodes;
		if (childNodes[index]) styleElement.removeChild(childNodes[index]);
		if (childNodes.length) {
			styleElement.insertBefore(cssNode, childNodes[index]);
		} else {
			styleElement.appendChild(cssNode);
		}
	}
}

function applyToTag(styleElement, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		styleElement.setAttribute("media", media)
	}

	if(styleElement.styleSheet) {
		styleElement.styleSheet.cssText = css;
	} else {
		while(styleElement.firstChild) {
			styleElement.removeChild(styleElement.firstChild);
		}
		styleElement.appendChild(document.createTextNode(css));
	}
}

function updateLink(linkElement, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	if(sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = linkElement.href;

	linkElement.href = URL.createObjectURL(blob);

	if(oldSrc)
		URL.revokeObjectURL(oldSrc);
}


/***/ }),
/* 20 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _mix_table_data = __webpack_require__(22);

var mix_table_data = _interopRequireWildcard(_mix_table_data);

var _table_base_opration = __webpack_require__(23);

var mix_table_base_op = _interopRequireWildcard(_table_base_opration);

var _mix_v_table_adapter = __webpack_require__(8);

var mix_v_table_adapter = _interopRequireWildcard(_mix_v_table_adapter);

var _mix_nice_validator = __webpack_require__(6);

var mix_nice_validator = _interopRequireWildcard(_mix_nice_validator);

var _mix_fields_data = __webpack_require__(5);

var mix_fields_data = _interopRequireWildcard(_mix_fields_data);

var _ajax_fields = __webpack_require__(0);

var ajax_fields = _interopRequireWildcard(_ajax_fields);

var _ajax_table = __webpack_require__(1);

var ajax_table = _interopRequireWildcard(_ajax_table);

var _com_pop_fields = __webpack_require__(2);

var com_pop_fields = _interopRequireWildcard(_com_pop_fields);

var _picture = __webpack_require__(12);

var table_picture = _interopRequireWildcard(_picture);

var _label_shower = __webpack_require__(9);

var table_label_shower = _interopRequireWildcard(_label_shower);

var _mapper = __webpack_require__(11);

var table_mapper = _interopRequireWildcard(_mapper);

var _pop_fields = __webpack_require__(13);

var table_pop_fields = _interopRequireWildcard(_pop_fields);

var _linetext = __webpack_require__(10);

var table_linetext = _interopRequireWildcard(_linetext);

var _check_box = __webpack_require__(21);

var table_checkbox = _interopRequireWildcard(_check_box);

var _label_shower2 = __webpack_require__(3);

var field_label_shower = _interopRequireWildcard(_label_shower2);

var _operator_a = __webpack_require__(15);

var op_a = _interopRequireWildcard(_operator_a);

var _delete_op = __webpack_require__(14);

var delete_op = _interopRequireWildcard(_delete_op);

var _btn = __webpack_require__(4);

var btn = _interopRequireWildcard(_btn);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

__webpack_require__(16);

//table mix


// table editor


// table operator


//fields operator

/***/ }),
/* 21 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var check_box = {
    props: ['rowData', 'field', 'index'],
    template: '<div ><input style="width: 100%" @change="on_changed()" type="checkbox" v-model="rowData[field]"></div>',
    data: function data() {
        return {};
    },
    methods: {
        on_changed: function on_changed() {
            this.$emit('on-custom-comp', { name: 'row-changed', row: this.rowData });
        }
    }
};

Vue.component('com-table-checkbox', check_box);

/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var mix_table_data = {
    methods: {
        search: function search() {
            this.search_args._page = 1;
            this.get_data();
        },
        get_data: function get_data() {
            this.data_getter(this);
        },
        get_page: function get_page(page_number) {
            this.search_args._page = page_number;
            this.get_data();
        },
        get_search_args: function get_search_args() {
            return this.search_args;
        },
        data_getter: function data_getter() {
            // 默认的 data_getter
            var self = this;
            //var loader = layer.load(2);
            cfg.show_load();
            $.get(ex.appendSearch(this.search_args), function (resp) {
                self.rows = resp.rows;
                self.row_pages = resp.row_pages;
                cfg.hide_load();
            });
        },
        save_rows: function save_rows(rows) {
            var self = this;
            var post_data = [{ fun: 'save_rows', rows: rows }];
            cfg.show_load();
            ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                ex.each(rows, function (row) {
                    var new_row = ex.findone(resp.save_rows, { pk: row.pk });
                    ex.assign(row, new_row);
                });
                cfg.hide_load(2000);
            });
        },
        clear: function clear() {
            this.rows = [];
            this.row_pages = {};
        },

        del_selected: function del_selected() {
            var self = this;
            layer.confirm('真的删除吗?', { icon: 3, title: '确认' }, function (index) {
                layer.close(index);
                var ss = layer.load(2);
                var post_data = [{ fun: 'del_rows', rows: self.selected }];
                $.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    layer.close(ss);
                    ex.each(self.selected, function (item) {
                        ex.remove(self.rows, item);
                    });
                    self.selected = [];
                    layer.msg('删除成功', { time: 2000 });
                });
            });
        }

        //del_item: function () {
        //    if (this.selected.length == 0) {
        //        return
        //    }
        //    var del_obj = {}
        //    for (var j = 0; j < this.selected.length; j++) {
        //        var pk = this.selected[j]
        //        for (var i = 0; i < this.rows.length; i++) {
        //            if (this.rows[i].pk.toString() == pk) {
        //                if (!del_obj[this.rows[i]._class]) {
        //                    del_obj[this.rows[i]._class] = []
        //                }
        //                del_obj[this.rows[i]._class].push(pk)
        //            }
        //        }
        //    }
        //    var out_str = ''
        //    for (var key in del_obj) {
        //        out_str += (key + ':' + del_obj[key].join(':') + ',')
        //    }
        //    location = ex.template("{engine_url}/del_rows?rows={rows}&next={next}", {
        //        engine_url: engine_url,
        //        rows: encodeURI(out_str),
        //        next: encodeURIComponent(location.href)
        //    })
        //},
        //goto_page: function (page) {
        //    this.search_args._page = page
        //    this.get_data()
        //},
        //add_new: function () {
        //    var url = ex.template('{engine_url}/{page}.edit/?next={next}', {
        //        engine_url: engine_url,
        //        page: page_name,
        //        next: encodeURIComponent(ex.appendSearch(location.pathname, search_args))
        //    })
        //    location = url
        //},
    }
};

window.mix_table_data = mix_table_data;

/***/ }),
/* 23 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var mix_table_base_op = {
    data: function data() {
        return {
            changed_rows: []
        };
    },
    mounted: function mounted() {
        this.$refs.op_save_changed_rows[0].set_enable(false);
        this.$refs.op_delete[0].set_enable(false);
    },
    watch: {
        changed_rows: function changed_rows(v) {
            this.$refs.op_save_changed_rows[0].set_enable(v.length != 0);
        },
        selected: function selected(v) {
            this.$refs.op_delete[0].set_enable(v.length != 0);
        }
    },
    methods: {
        on_operation: function on_operation(operation) {
            if (operation == 'add_new') {
                this.add_new();
            }
            if (operation == 'delete') {
                this.del_selected();
            }
            if (operation == 'save_changed_rows') {
                this.save_rows(this.changed_rows);
                this.changed_rows = [];
            }
        }
    }
};

window.mix_table_base_op = mix_table_base_op;

/***/ })
/******/ ]);