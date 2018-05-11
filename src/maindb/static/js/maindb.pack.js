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
/******/ 	return __webpack_require__(__webpack_require__.s = 4);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
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
/* 1 */
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
/* 2 */
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
/* 3 */
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
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _match = __webpack_require__(2);

var match = _interopRequireWildcard(_match);

var _app_pkg = __webpack_require__(0);

var app_pkg = _interopRequireWildcard(_app_pkg);

var _help = __webpack_require__(1);

var help_logic = _interopRequireWildcard(_help);

var _notice = __webpack_require__(3);

var notice_logic = _interopRequireWildcard(_notice);

var _activity = __webpack_require__(5);

var activity_logic = _interopRequireWildcard(_activity);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

/***/ }),
/* 5 */
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

/***/ })
/******/ ]);