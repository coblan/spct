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
/******/ 	return __webpack_require__(__webpack_require__.s = 35);
/******/ })
/************************************************************************/
/******/ ({

/***/ 0:
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

/***/ 1:
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

/***/ 28:
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(0)();
// imports


// module
exports.push([module.i, ".com-shouchun {\n  background-color: white;\n  padding: 0;\n  margin: 14px 0; }\n  .com-shouchun table {\n    width: 100%; }\n    .com-shouchun table td {\n      text-align: center; }\n    .com-shouchun table tr:first-child td {\n      border-bottom: 1px solid #f2f2f2; }\n    .com-shouchun table .big-col {\n      font-size: 110%; }\n    .com-shouchun table .data-col {\n      color: grey;\n      font-size: 80%; }\n    .com-shouchun table .green {\n      color: #46c8bb; }\n  .com-shouchun .mybtn-col {\n    width: 6em;\n    height: 5em; }\n    .com-shouchun .mybtn-col .mybtn {\n      position: relative;\n      width: 6em;\n      height: 2.5em;\n      background-color: #52d39a;\n      color: white;\n      border-radius: 2em;\n      font-size: 90%;\n      margin: auto; }\n      .com-shouchun .mybtn-col .mybtn.disabled {\n        background-color: #aaaaaa; }\n", ""]);

// exports


/***/ }),

/***/ 3:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


if (window.jb_app) {
    // android
    //cfg.showMsg('具有555window.jb_app对象')
} else if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.get) {
    // ios
    window.jb_app = {
        get: function get(key, url) {
            var get_data = { key: key, url: url };
            window.webkit.messageHandlers.get.postMessage(get_data);
        },
        post: function post(key, url, data) {
            var post_data = { key: key, url: url, data: data };
            window.webkit.messageHandlers.post.postMessage(post_data);
        },
        ios: true
    };
} else {
    //cfg.showMsg('没有window.jb_app对象，创建一个虚拟的')
    window.jb_app = {
        get: function get(key, url, mock_data) {
            var rt_data = mock_data || { data: '顺利GET' };
            rt_data.key = key;
            jb_js.dispatch(rt_data);
        },
        post: function post(key, url, data, mock_data) {
            var rt_data = mock_data || { data: '顺利POST' };
            rt_data.key = key;
            jb_js.dispatch(rt_data);
        },
        fake: true
    };
}

var jb_js = {
    get: function get(url, callback, mock_data) {
        //cfg.showMsg('调用333jb_js.get')
        var fun_key = _uuid();

        jb_js['_fun_' + fun_key] = callback;
        if (window.jb_app.fake) {
            window.jb_app.get(fun_key, url, mock_data);
        } else {
            window.jb_app.get(fun_key, url);
        }
        //cfg.showMsg('调用jb.js.get结束')
    },
    post: function post(url, data, callback, mock_data) {
        var fun_key = _uuid();

        jb_js['_fun_' + fun_key] = callback;
        if (window.jb_app.fake) {
            window.jb_app.post(fun_key, url, data, mock_data);
        } else if (window.jb_app.ios) {
            window.jb_app.post(fun_key, url, data);
        } else {
            window.jb_app.post(fun_key, url, JSON.stringify(data));
        }
    },
    dispatch: function dispatch(resp) {
        //var resp= JSON.parse(resp_str)
        //cfg.showMsg('进入dispatch')
        //cfg.showMsg( JSON.stringify(resp))
        var key = resp.key;
        jb_js['_fun_' + key](resp);
        delete jb_js['_fun_' + key];
    }
};

window.jb_js = jb_js;

function _uuid() {
    var d = Date.now();
    if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
        d += performance.now(); //use high-precision timer if available
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : r & 0x3 | 0x8).toString(16);
    });
}

/***/ }),

/***/ 32:
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(28);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(1)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./shou_cun.scss", function() {
			var newContent = require("!!../../../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./shou_cun.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),

/***/ 35:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _shou_cun = __webpack_require__(4);

var shou_cun = _interopRequireWildcard(_shou_cun);

var _network = __webpack_require__(3);

var network = _interopRequireWildcard(_network);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

/***/ }),

/***/ 4:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


__webpack_require__(32);

Vue.component('com-shouchun', {
    template: '<div class="com-shouchun">\n\n    <!--<button @click="update_data()">\u83B7\u53D6</button>-->\n\n    <table>\n    <tr v-for="row in rows">\n        <td v-for="head in heads"  :class="head.scls">\n            <div   v-if="row[head.name]" v-text="head.top_label"></div>\n            <div v-text="row[head.name]"></div>\n        </td>\n        <td class="mybtn-col">\n            <div :class="[\'mybtn\',{disabled:!row.submitable}]" @click="submit(row)"><span class="center-vh" style="white-space: nowrap" v-text="action_label(row)"></span></div>\n        </td>\n    </tr>\n    </table>\n    </div>',
    data: function data() {
        return {
            heads: [{ name: 'label', scls: 'big-col', top_label: '' }, { name: 'ChargeTime', scls: 'data-col', top_label: '存款' }, { name: 'Amount', scls: 'data-col', top_label: '存入' }, { name: 'Bonus', scls: 'data-col green', top_label: '可得红利' }],
            rows: []
        };
    },
    /*
     "ChargeTime": "2019-01-09T11:34:28.207Z",
     "Amount": 0,
     "Bonus": 0,
     "Done": true
    * */
    mounted: function mounted() {
        var self = this;
        //setTimeout(function(){
        self.update_data();
        //},5000)
    },
    methods: {
        action_label: function action_label(row) {
            var dc = {
                0: '参加活动',
                1: '已参加',
                2: '已发放'
            };
            return dc[row.State];
        },
        update_data: function update_data() {
            //cfg.showMsg('开始更新数据')
            var mock_data = {
                data: [{ ChargeTime: '04-21 22:30', Amount: 50, Bonus: 50, State: 2 }, { ChargeTime: '2019-01-21 22:30:30', Amount: '100000', Bonus: '1239999', State: 1 }]
            };
            var dec_rows = [{ label: '首存', action: '', submitable: false }, { label: '再存', action: '', submitable: false }];
            var self = this;
            cfg.show_load();
            jb_js.get('/activity/charge/list?activityId=' + activity.pk, function (resp) {
                cfg.hide_load();
                //cfg.showMsg('首存数据:'+JSON.stringify(resp))
                self.rows = resp.data;

                var last_done = true;
                for (var i = 0; i < self.rows.length; i++) {
                    var row = self.rows[i];
                    ex.vueAssign(row, dec_rows[i]);
                    row.Type = i + 1;
                    if (row.State != 0) {
                        last_done = true;
                    } else if (last_done) {
                        row.submitable = true;
                        last_done = false;
                    }
                }
            }, mock_data);
        },
        submit: function submit(row) {
            if (!row.submitable) {
                return;
            }
            var mock_data = { success: 1 };
            var post_data = {
                ActivityId: activity.pk,
                Type: row.Type
            };
            var self = this;
            jb_js.post('/activity/charge/do', post_data, function (resp) {

                if (resp.success) {
                    cfg.showMsg('参加成功！');
                    self.update_data();
                } else {
                    cfg.showError(resp.error_description);
                }
            }, mock_data);
        }
    }
});

/***/ })

/******/ });