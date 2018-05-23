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
/******/ 	return __webpack_require__(__webpack_require__.s = 11);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var activity_logic = {
    mounted: function mounted() {
        var self = this;
        ex.assign(this.op_funs, {
            update_activity_file: function update_activity_file() {
                cfg.show_load();
                var post_data = [{ fun: 'update_activity_file' }];
                ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                    if (resp.update_activity_file.status == 'success') {
                        cfg.hide_load(500);
                    } else {
                        cfg.warning(resp);
                        cfg.hide_load();
                    }
                });
            }
        });
    }
};

window.activity_logic = activity_logic;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
var field_file_uploader = exports.field_file_uploader = {
    props: ['row', 'head'],
    template: '<div><com-file-uploader-tmp v-model="row[head.name]" :config="head.config" :readonly="head.readonly"></com-file-uploader-tmp></div>',
    computed: {
        url: function url() {
            return this.row[this.head.name];
        }
    },
    watch: {
        url: function url(v) {
            var mt = /([^\?]+)\?([^\?]+)/.exec(v);
            if (mt) {
                var args = ex.parseSearch(mt[2]);
                if (args.version_code) {
                    this.row.versionid = args.version_code;
                }
                if (args.version_name) {
                    this.row.versionname = args.version_name;
                }
                if (args.size) {
                    this.row.size = args.size;
                }
                if (args.md5) {
                    this.row.md5 = args.md5;
                }

                this.row[this.head.name] = mt[1];
            }
        }
    }
};

Vue.component('com-field-app-pkg-uploader', field_file_uploader);

var app_pkg = {
    mounted: function mounted() {
        this.updateReadonly();
    },
    watch: {
        'row.terminal': function rowTerminal() {
            this.updateReadonly();
        }
    },
    methods: {
        updateReadonly: function updateReadonly() {
            var self = this;
            ex.each(self.heads, function (head) {
                if (ex.isin(head.name, ['versionid', 'versionname'])) {
                    // 2 == android
                    if (self.row.terminal == 2) {
                        head.readonly = true;
                    } else {
                        head.readonly = false;
                    }
                }
            });
        }
    }
};
window.app_pkg = app_pkg;

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var banner_logic = {
    mounted: function mounted() {
        var self = this;
        ex.assign(this.op_funs, {
            online: function online() {
                self.set_banner_state(1);
            },
            offline: function offline() {
                self.set_banner_state(0);
            }
        });
    },

    methods: {
        set_banner_state: function set_banner_state(state) {
            var self = this;
            var post_data = [{ fun: 'set_banner_status', rows: this.selected, status: state }];
            cfg.show_load();
            ex.post('/d/ajax/' + app, JSON.stringify(post_data), function (resp) {
                cfg.hide_load(2000);
                ex.each(self.selected, function (item) {
                    item.status = state;
                });
            });
        }
    }
};

window.banner_logic = banner_logic;

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


__webpack_require__(10);

var com_tab_special_bet_value = {
    props: ['tab_head', 'par_row'],
    data: function data() {
        return {
            match_opened: true,
            oddstype: [],
            specialbetvalue: [],

            ops: this.tab_head.ops
        };
    },
    mixins: [mix_fields_data],
    template: '<div class="com_tab_special_bet_value">\n    <span class="oprations">\n            <component style="padding: 0.5em;" v-for="op in ops" :is="op.editor" :ref="\'op_\'+op.fun" :head="op" @operation="on_operation(op)"></component>\n    </span>\n    <div style="text-align: center;">\n        <span v-text="par_row.matchdate"></span>/\n        <span v-text="par_row.matchid"></span>/\n        <span v-text="par_row.team1zh"></span>\n        <span>VS</span>\n        <span v-text="par_row.team2zh"></span>\n\n    </div>\n    <div>\n           <div class="box">\n\n                <el-switch\n                      v-model="match_opened"\n                      active-color="#13ce66"\n                      inactive-color="#ff4949">\n                </el-switch>\n                <span>\u6574\u573A\u6BD4\u8D5B</span>\n            </div>\n            <div class="box">\n                <div v-for="odtp in normed_oddstype">\n                    <el-switch\n                          v-model="odtp.opened"\n                          active-color="#13ce66"\n                          inactive-color="#ff4949">\n                    </el-switch>\n                    <span v-text="odtp.name"></span>\n                     <!--<span v-text="odtp.oddstypeid"></span>-->\n                      <!--<span v-text="odtp.oddstypegroup"></span>-->\n                </div>\n            </div>\n            <div class="box">\n                <div v-for="spbet in normed_specailbetvalue">\n                    <el-switch\n                          v-model="spbet.opened"\n                          active-color="#13ce66"\n                          inactive-color="#ff4949">\n                    </el-switch>\n                    <span v-text="spbet.name"></span>\n                    <!--<span v-text="spbet.specialbetvalue"></span>-->\n                     <!--<span v-text="spbet.oddsid"></span>-->\n                </div>\n            </div>\n    </div>\n\n    </div>',
    mounted: function mounted() {
        this.getRowData();

        var self = this;
        ex.assign(this.op_funs, {
            refresh: function refresh() {
                self.getRowData();
            }
        });
    },
    computed: {
        normed_oddstype: function normed_oddstype() {
            if (!this.match_opened) {
                return [];
            } else {
                return ex.sortOrder(this.oddstype, 'name');
            }
        },
        normed_specailbetvalue: function normed_specailbetvalue() {
            if (!this.match_opened) {
                return [];
            }
            var self = this;
            var ss = ex.filter(this.specialbetvalue, function (bet) {
                var oddtyps = ex.findone(self.oddstype, { oddstypegroup: bet.oddstypegroup });
                return oddtyps.opened;
            });

            return ex.sortOrder(ss, 'name');
        }
    },
    methods: {
        save: function save() {
            var post_data = [{ fun: 'save_special_bet_value',
                matchid: this.par_row.matchid,
                match_opened: this.match_opened,
                oddstype: this.oddstype,
                specialbetvalue: this.specialbetvalue
            }];
            cfg.show_load();
            ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                if (resp.save_special_bet_value.status == 'success') {
                    cfg.hide_load(500);
                } else {
                    cfg.showMsg('error');
                }
            });
        },
        on_show: function on_show() {},
        getRowData: function getRowData() {
            var self = this;
            var post_data = [{ fun: 'update_special_bet_value', matchid: this.par_row.matchid }];
            cfg.show_load();
            ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                self.match_opened = resp.update_special_bet_value.match_opened;
                self.oddstype = resp.update_special_bet_value.oddstype, self.specialbetvalue = resp.update_special_bet_value.specialbetvalue, cfg.hide_load();
            });
        }
    }
};
Vue.component('com-tab-special-bet-value', com_tab_special_bet_value);

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var help_logic = {

    mounted: function mounted() {

        var self = this;
        ex.assign(this.op_funs, {
            update_help_file: function update_help_file() {
                cfg.show_load();
                var post_data = [{ fun: 'update_help_file' }];
                ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                    if (resp.update_help_file.status == 'success') {
                        cfg.hide_load(500);
                    } else {
                        cfg.warning(resp);
                        cfg.hide_load();
                    }
                });
            }
        });
    },

    computed: {
        row_count: function row_count() {
            return this.rows.length;
        }
    },
    watch: {
        row_count: function row_count(v) {
            var post_data = [{ fun: 'get_help_options' }];
            ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                var mtype_filter = ex.findone(row_filters, { name: 'mtype' });
                mtype_filter.options = resp.get_help_options;
            });
        }
    }
};
window.help_logic = help_logic;

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var match_logic = {
    mounted: function mounted() {
        var self = this;
        ex.assign(this.op_funs, {
            close_match: function close_match(kws) {
                if (self.selected.length != 1) {
                    cfg.showMsg('请选择一条记录');
                    return;
                }
                var crt_row = self.selected[0];
                if (crt_row.statuscode == 100) {
                    cfg.showMsg('比赛状态已经为结束，不需要手动结束！');
                    return;
                }

                var index = layer.confirm('结束比赛?', function (index) {
                    layer.close(index);
                    crt_row.statuscode = 100;
                    var post_data = [{ fun: 'save_row', row: crt_row }];
                    cfg.show_load();
                    ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {

                        if (resp.save_row.errors) {
                            cfg.warning(JSON.stringify(resp.save_row.errors));
                        } else {
                            cfg.hide_load(2000);
                        }
                    });
                });
            },
            manual_end_money: function manual_end_money(kws) {
                if (self.selected.length != 1) {
                    cfg.showMsg('请选择一条记录');
                    return;
                }

                var crt_row = self.selected[0];
                //if(crt_row.statuscode !=100){
                //    cfg.showMsg('请先结束比赛')
                //    return
                //}

                var mt = /(\d+):(\d+)/.exec(crt_row.matchscore);
                if (mt) {
                    var home_score = mt[1];
                    var away_score = mt[2];
                } else {
                    var home_score = 0;
                    var away_score = 0;
                }

                var row = {
                    matchid: crt_row.matchid,
                    _matchid_label: crt_row._matchid_label,
                    home_score: home_score,
                    away_score: away_score
                    //statuscode:crt_row.statuscode
                };
                pop_fields_layer(row, kws.fields_ctx, function (e) {
                    alert(e.new_row);
                });
            },
            jie_suan_pai_cai: function jie_suan_pai_cai(kws) {
                if (self.selected.length != 1) {
                    cfg.showMsg('请选择一条记录');
                    return;
                }
            },
            recommendate: function recommendate(kws) {
                if (self.selected.length == 0) {
                    cfg.showMsg('请选择一些记录');
                    return;
                }
                ex.each(self.selected, function (row) {
                    row.isrecommend = true;
                });
                var post_data = [{ fun: 'save_rows', rows: self.selected }];
                cfg.show_load();
                ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    cfg.hide_load(2000);
                });
            },
            un_recommendate: function un_recommendate(kws) {
                if (self.selected.length == 0) {
                    cfg.showMsg('请选择一些记录');
                    return;
                }
                ex.each(self.selected, function (row) {
                    row.isrecommend = false;
                });
                var post_data = [{ fun: 'save_rows', rows: self.selected }];
                cfg.show_load();
                ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    cfg.hide_load(2000);
                });
            },

            livebet: function livebet(kws) {
                if (self.selected.length == 0) {
                    cfg.showMsg('请选择一些记录');
                    return;
                }
                ex.each(self.selected, function (row) {
                    row.livebet = true;
                });
                var post_data = [{ fun: 'save_rows', rows: self.selected }];
                cfg.show_load();
                ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    cfg.hide_load(2000);
                });
            },
            un_livebet: function un_livebet(kws) {
                if (self.selected.length == 0) {
                    cfg.showMsg('请选择一些记录');
                    return;
                }
                ex.each(self.selected, function (row) {
                    row.livebet = false;
                });
                var post_data = [{ fun: 'save_rows', rows: self.selected }];
                cfg.show_load();
                ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    cfg.hide_load(2000);
                });
            }
        });
    },
    computed: {
        only_one_selected: function only_one_selected() {
            return this.selected.length == 1;
        },
        status_is_not_100: function status_is_not_100() {
            if (this.selected.length == 1) {
                var row = this.selected[0];
                if (row.statuscode != 100) {
                    return true;
                }
            }
            return false;
        }
    }
};

var produce_match_outcome = {
    mounted: function mounted() {
        var self = this;
        ex.assign(this.op_funs, {
            produce_match_outcome: function produce_match_outcome(kws) {

                var index = layer.confirm('确认手动结算?', function (index) {
                    layer.close(index);

                    var post_data = [{ fun: 'produce_match_outcome', row: self.row }];
                    cfg.show_load();
                    ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                        cfg.hide_load();
                        cfg.showMsg(resp.produce_match_outcome.Message);
                    });
                });
            }
        });
    }
};

window.match_logic = match_logic;
window.produce_match_outcome = produce_match_outcome;

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var notice_logic = {

    mounted: function mounted() {

        var self = this;
        ex.assign(this.op_funs, {
            update_notice_file: function update_notice_file() {
                cfg.show_load();
                var post_data = [{ fun: 'update_notice_file' }];
                ex.post('/d/ajax/maindb', JSON.stringify(post_data), function (resp) {
                    if (resp.update_notice_file.status == 'success') {
                        cfg.hide_load(500);
                    } else {
                        cfg.warning(resp);
                        cfg.hide_load();
                    }
                });
            }
        });
    }

    //computed:{
    //    row_count:function(){
    //        return this.rows.length
    //    }
    //},
    //watch:{
    //    row_count:function(v){
    //        var post_data=[{fun:'get_help_options'}]
    //        ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
    //            var mtype_filter = ex.findone(row_filters,{name:'mtype'})
    //            mtype_filter.options = resp.get_help_options
    //        })
    //    }
    //},
};
window.notice_logic = notice_logic;

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(8)();
// imports


// module
exports.push([module.i, ".com_tab_special_bet_value .box {\n  width: 250px;\n  height: 400px;\n  padding: 1em;\n  border: 1px solid black;\n  float: left;\n  margin-right: 1em;\n  position: relative;\n  overflow: auto; }\n", ""]);

// exports


/***/ }),
/* 8 */
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
/* 9 */
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
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(7);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(9)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./com_tab_special_bet_value.scss", function() {
			var newContent = require("!!../../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./com_tab_special_bet_value.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _match = __webpack_require__(5);

var match = _interopRequireWildcard(_match);

var _app_pkg = __webpack_require__(1);

var app_pkg = _interopRequireWildcard(_app_pkg);

var _help = __webpack_require__(4);

var help_logic = _interopRequireWildcard(_help);

var _notice = __webpack_require__(6);

var notice_logic = _interopRequireWildcard(_notice);

var _activity = __webpack_require__(0);

var activity_logic = _interopRequireWildcard(_activity);

var _banner = __webpack_require__(2);

var banner_logic = _interopRequireWildcard(_banner);

var _com_tab_special_bet_value = __webpack_require__(3);

var com_tab_special_bet_value = _interopRequireWildcard(_com_tab_special_bet_value);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

/***/ })
/******/ ]);