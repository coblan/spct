/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.l = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };

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

/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};

/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 1);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
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

                    crt_row.statuscode = 100;
                    var post_data = [{ fun: 'save_row', row: crt_row }];
                    cfg.show_load();
                    ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                        layer.close(index);
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
                var row = {
                    matchid: '123',
                    home_score: '123',
                    away_score: '213',
                    statuscode: crt_row.statuscode
                };
                pop_fields_layer(row, kws.heads, kws.ops, function (kws) {
                    alert(kws.new_row);
                });
            },
            jie_suan_pai_cai: function jie_suan_pai_cai(kws) {
                if (self.selected.length != 1) {
                    cfg.showMsg('请选择一条记录');
                    return;
                }
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

window.match_logic = match_logic;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _match = __webpack_require__(0);

var match = _interopRequireWildcard(_match);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

/***/ })
/******/ ]);