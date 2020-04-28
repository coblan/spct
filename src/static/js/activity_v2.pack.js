/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
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
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
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
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./activity_v2/main.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./activity_v2/scss/shou_cun.scss":
/*!*******************************************************************************************************************************************!*\
  !*** D:/coblan/webcode/node_modules/css-loader!D:/coblan/webcode/node_modules/sass-loader/lib/loader.js!./activity_v2/scss/shou_cun.scss ***!
  \*******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("exports = module.exports = __webpack_require__(/*! ../../../../../../../coblan/webcode/node_modules/css-loader/lib/css-base.js */ \"../../../../../coblan/webcode/node_modules/css-loader/lib/css-base.js\")();\n// imports\n\n\n// module\nexports.push([module.i, \".com-shouchun {\\n  background-color: white;\\n  padding: 0;\\n  margin: 14px 0; }\\n  .com-shouchun table {\\n    width: 100%; }\\n    .com-shouchun table td {\\n      text-align: center; }\\n    .com-shouchun table tr:first-child td {\\n      border-bottom: 1px solid #f2f2f2; }\\n    .com-shouchun table .big-col {\\n      font-size: 110%;\\n      padding: 4px; }\\n    .com-shouchun table .data-col {\\n      color: grey;\\n      font-size: 80%; }\\n    .com-shouchun table .green {\\n      color: #46c8bb; }\\n  .com-shouchun .mybtn-col {\\n    width: 6em;\\n    height: 5em; }\\n    .com-shouchun .mybtn-col .mybtn {\\n      position: relative;\\n      width: 6em;\\n      height: 2.5em;\\n      background-color: #52d39a;\\n      color: white;\\n      border-radius: 2em;\\n      font-size: 90%;\\n      margin: auto; }\\n      .com-shouchun .mybtn-col .mybtn.disabled {\\n        background-color: #aaaaaa; }\\n\", \"\"]);\n\n// exports\n\n\n//# sourceURL=webpack:///./activity_v2/scss/shou_cun.scss?D:/coblan/webcode/node_modules/css-loader!D:/coblan/webcode/node_modules/sass-loader/lib/loader.js");

/***/ }),

/***/ "../../../../../coblan/webcode/node_modules/css-loader/lib/css-base.js":
/*!*****************************************************************!*\
  !*** D:/coblan/webcode/node_modules/css-loader/lib/css-base.js ***!
  \*****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("/*\n\tMIT License http://www.opensource.org/licenses/mit-license.php\n\tAuthor Tobias Koppers @sokra\n*/\n// css base code, injected by the css-loader\nmodule.exports = function() {\n\tvar list = [];\n\n\t// return the list of modules as css string\n\tlist.toString = function toString() {\n\t\tvar result = [];\n\t\tfor(var i = 0; i < this.length; i++) {\n\t\t\tvar item = this[i];\n\t\t\tif(item[2]) {\n\t\t\t\tresult.push(\"@media \" + item[2] + \"{\" + item[1] + \"}\");\n\t\t\t} else {\n\t\t\t\tresult.push(item[1]);\n\t\t\t}\n\t\t}\n\t\treturn result.join(\"\");\n\t};\n\n\t// import a list of modules into the list\n\tlist.i = function(modules, mediaQuery) {\n\t\tif(typeof modules === \"string\")\n\t\t\tmodules = [[null, modules, \"\"]];\n\t\tvar alreadyImportedModules = {};\n\t\tfor(var i = 0; i < this.length; i++) {\n\t\t\tvar id = this[i][0];\n\t\t\tif(typeof id === \"number\")\n\t\t\t\talreadyImportedModules[id] = true;\n\t\t}\n\t\tfor(i = 0; i < modules.length; i++) {\n\t\t\tvar item = modules[i];\n\t\t\t// skip already imported module\n\t\t\t// this implementation is not 100% perfect for weird media query combinations\n\t\t\t//  when a module is imported multiple times with different media queries.\n\t\t\t//  I hope this will never occur (Hey this way we have smaller bundles)\n\t\t\tif(typeof item[0] !== \"number\" || !alreadyImportedModules[item[0]]) {\n\t\t\t\tif(mediaQuery && !item[2]) {\n\t\t\t\t\titem[2] = mediaQuery;\n\t\t\t\t} else if(mediaQuery) {\n\t\t\t\t\titem[2] = \"(\" + item[2] + \") and (\" + mediaQuery + \")\";\n\t\t\t\t}\n\t\t\t\tlist.push(item);\n\t\t\t}\n\t\t}\n\t};\n\treturn list;\n};\n\n\n//# sourceURL=webpack:///D:/coblan/webcode/node_modules/css-loader/lib/css-base.js?");

/***/ }),

/***/ "../../../../../coblan/webcode/node_modules/style-loader/addStyles.js":
/*!****************************************************************!*\
  !*** D:/coblan/webcode/node_modules/style-loader/addStyles.js ***!
  \****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("/*\n\tMIT License http://www.opensource.org/licenses/mit-license.php\n\tAuthor Tobias Koppers @sokra\n*/\nvar stylesInDom = {},\n\tmemoize = function(fn) {\n\t\tvar memo;\n\t\treturn function () {\n\t\t\tif (typeof memo === \"undefined\") memo = fn.apply(this, arguments);\n\t\t\treturn memo;\n\t\t};\n\t},\n\tisOldIE = memoize(function() {\n\t\treturn /msie [6-9]\\b/.test(self.navigator.userAgent.toLowerCase());\n\t}),\n\tgetHeadElement = memoize(function () {\n\t\treturn document.head || document.getElementsByTagName(\"head\")[0];\n\t}),\n\tsingletonElement = null,\n\tsingletonCounter = 0,\n\tstyleElementsInsertedAtTop = [];\n\nmodule.exports = function(list, options) {\n\tif(typeof DEBUG !== \"undefined\" && DEBUG) {\n\t\tif(typeof document !== \"object\") throw new Error(\"The style-loader cannot be used in a non-browser environment\");\n\t}\n\n\toptions = options || {};\n\t// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>\n\t// tags it will allow on a page\n\tif (typeof options.singleton === \"undefined\") options.singleton = isOldIE();\n\n\t// By default, add <style> tags to the bottom of <head>.\n\tif (typeof options.insertAt === \"undefined\") options.insertAt = \"bottom\";\n\n\tvar styles = listToStyles(list);\n\taddStylesToDom(styles, options);\n\n\treturn function update(newList) {\n\t\tvar mayRemove = [];\n\t\tfor(var i = 0; i < styles.length; i++) {\n\t\t\tvar item = styles[i];\n\t\t\tvar domStyle = stylesInDom[item.id];\n\t\t\tdomStyle.refs--;\n\t\t\tmayRemove.push(domStyle);\n\t\t}\n\t\tif(newList) {\n\t\t\tvar newStyles = listToStyles(newList);\n\t\t\taddStylesToDom(newStyles, options);\n\t\t}\n\t\tfor(var i = 0; i < mayRemove.length; i++) {\n\t\t\tvar domStyle = mayRemove[i];\n\t\t\tif(domStyle.refs === 0) {\n\t\t\t\tfor(var j = 0; j < domStyle.parts.length; j++)\n\t\t\t\t\tdomStyle.parts[j]();\n\t\t\t\tdelete stylesInDom[domStyle.id];\n\t\t\t}\n\t\t}\n\t};\n}\n\nfunction addStylesToDom(styles, options) {\n\tfor(var i = 0; i < styles.length; i++) {\n\t\tvar item = styles[i];\n\t\tvar domStyle = stylesInDom[item.id];\n\t\tif(domStyle) {\n\t\t\tdomStyle.refs++;\n\t\t\tfor(var j = 0; j < domStyle.parts.length; j++) {\n\t\t\t\tdomStyle.parts[j](item.parts[j]);\n\t\t\t}\n\t\t\tfor(; j < item.parts.length; j++) {\n\t\t\t\tdomStyle.parts.push(addStyle(item.parts[j], options));\n\t\t\t}\n\t\t} else {\n\t\t\tvar parts = [];\n\t\t\tfor(var j = 0; j < item.parts.length; j++) {\n\t\t\t\tparts.push(addStyle(item.parts[j], options));\n\t\t\t}\n\t\t\tstylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};\n\t\t}\n\t}\n}\n\nfunction listToStyles(list) {\n\tvar styles = [];\n\tvar newStyles = {};\n\tfor(var i = 0; i < list.length; i++) {\n\t\tvar item = list[i];\n\t\tvar id = item[0];\n\t\tvar css = item[1];\n\t\tvar media = item[2];\n\t\tvar sourceMap = item[3];\n\t\tvar part = {css: css, media: media, sourceMap: sourceMap};\n\t\tif(!newStyles[id])\n\t\t\tstyles.push(newStyles[id] = {id: id, parts: [part]});\n\t\telse\n\t\t\tnewStyles[id].parts.push(part);\n\t}\n\treturn styles;\n}\n\nfunction insertStyleElement(options, styleElement) {\n\tvar head = getHeadElement();\n\tvar lastStyleElementInsertedAtTop = styleElementsInsertedAtTop[styleElementsInsertedAtTop.length - 1];\n\tif (options.insertAt === \"top\") {\n\t\tif(!lastStyleElementInsertedAtTop) {\n\t\t\thead.insertBefore(styleElement, head.firstChild);\n\t\t} else if(lastStyleElementInsertedAtTop.nextSibling) {\n\t\t\thead.insertBefore(styleElement, lastStyleElementInsertedAtTop.nextSibling);\n\t\t} else {\n\t\t\thead.appendChild(styleElement);\n\t\t}\n\t\tstyleElementsInsertedAtTop.push(styleElement);\n\t} else if (options.insertAt === \"bottom\") {\n\t\thead.appendChild(styleElement);\n\t} else {\n\t\tthrow new Error(\"Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.\");\n\t}\n}\n\nfunction removeStyleElement(styleElement) {\n\tstyleElement.parentNode.removeChild(styleElement);\n\tvar idx = styleElementsInsertedAtTop.indexOf(styleElement);\n\tif(idx >= 0) {\n\t\tstyleElementsInsertedAtTop.splice(idx, 1);\n\t}\n}\n\nfunction createStyleElement(options) {\n\tvar styleElement = document.createElement(\"style\");\n\tstyleElement.type = \"text/css\";\n\tinsertStyleElement(options, styleElement);\n\treturn styleElement;\n}\n\nfunction createLinkElement(options) {\n\tvar linkElement = document.createElement(\"link\");\n\tlinkElement.rel = \"stylesheet\";\n\tinsertStyleElement(options, linkElement);\n\treturn linkElement;\n}\n\nfunction addStyle(obj, options) {\n\tvar styleElement, update, remove;\n\n\tif (options.singleton) {\n\t\tvar styleIndex = singletonCounter++;\n\t\tstyleElement = singletonElement || (singletonElement = createStyleElement(options));\n\t\tupdate = applyToSingletonTag.bind(null, styleElement, styleIndex, false);\n\t\tremove = applyToSingletonTag.bind(null, styleElement, styleIndex, true);\n\t} else if(obj.sourceMap &&\n\t\ttypeof URL === \"function\" &&\n\t\ttypeof URL.createObjectURL === \"function\" &&\n\t\ttypeof URL.revokeObjectURL === \"function\" &&\n\t\ttypeof Blob === \"function\" &&\n\t\ttypeof btoa === \"function\") {\n\t\tstyleElement = createLinkElement(options);\n\t\tupdate = updateLink.bind(null, styleElement);\n\t\tremove = function() {\n\t\t\tremoveStyleElement(styleElement);\n\t\t\tif(styleElement.href)\n\t\t\t\tURL.revokeObjectURL(styleElement.href);\n\t\t};\n\t} else {\n\t\tstyleElement = createStyleElement(options);\n\t\tupdate = applyToTag.bind(null, styleElement);\n\t\tremove = function() {\n\t\t\tremoveStyleElement(styleElement);\n\t\t};\n\t}\n\n\tupdate(obj);\n\n\treturn function updateStyle(newObj) {\n\t\tif(newObj) {\n\t\t\tif(newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap)\n\t\t\t\treturn;\n\t\t\tupdate(obj = newObj);\n\t\t} else {\n\t\t\tremove();\n\t\t}\n\t};\n}\n\nvar replaceText = (function () {\n\tvar textStore = [];\n\n\treturn function (index, replacement) {\n\t\ttextStore[index] = replacement;\n\t\treturn textStore.filter(Boolean).join('\\n');\n\t};\n})();\n\nfunction applyToSingletonTag(styleElement, index, remove, obj) {\n\tvar css = remove ? \"\" : obj.css;\n\n\tif (styleElement.styleSheet) {\n\t\tstyleElement.styleSheet.cssText = replaceText(index, css);\n\t} else {\n\t\tvar cssNode = document.createTextNode(css);\n\t\tvar childNodes = styleElement.childNodes;\n\t\tif (childNodes[index]) styleElement.removeChild(childNodes[index]);\n\t\tif (childNodes.length) {\n\t\t\tstyleElement.insertBefore(cssNode, childNodes[index]);\n\t\t} else {\n\t\t\tstyleElement.appendChild(cssNode);\n\t\t}\n\t}\n}\n\nfunction applyToTag(styleElement, obj) {\n\tvar css = obj.css;\n\tvar media = obj.media;\n\n\tif(media) {\n\t\tstyleElement.setAttribute(\"media\", media)\n\t}\n\n\tif(styleElement.styleSheet) {\n\t\tstyleElement.styleSheet.cssText = css;\n\t} else {\n\t\twhile(styleElement.firstChild) {\n\t\t\tstyleElement.removeChild(styleElement.firstChild);\n\t\t}\n\t\tstyleElement.appendChild(document.createTextNode(css));\n\t}\n}\n\nfunction updateLink(linkElement, obj) {\n\tvar css = obj.css;\n\tvar sourceMap = obj.sourceMap;\n\n\tif(sourceMap) {\n\t\t// http://stackoverflow.com/a/26603875\n\t\tcss += \"\\n/*# sourceMappingURL=data:application/json;base64,\" + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + \" */\";\n\t}\n\n\tvar blob = new Blob([css], { type: \"text/css\" });\n\n\tvar oldSrc = linkElement.href;\n\n\tlinkElement.href = URL.createObjectURL(blob);\n\n\tif(oldSrc)\n\t\tURL.revokeObjectURL(oldSrc);\n}\n\n\n//# sourceURL=webpack:///D:/coblan/webcode/node_modules/style-loader/addStyles.js?");

/***/ }),

/***/ "./activity_v2/main.js":
/*!*****************************!*\
  !*** ./activity_v2/main.js ***!
  \*****************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _shou_cun_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./shou_cun.js */ \"./activity_v2/shou_cun.js\");\n/* harmony import */ var _shou_cun_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_shou_cun_js__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _network_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./network.js */ \"./activity_v2/network.js\");\n/* harmony import */ var _network_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_network_js__WEBPACK_IMPORTED_MODULE_1__);\n\n\n\n//# sourceURL=webpack:///./activity_v2/main.js?");

/***/ }),

/***/ "./activity_v2/network.js":
/*!********************************!*\
  !*** ./activity_v2/network.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("if (window.jb_app) {// android\n  //cfg.showMsg('具有555window.jb_app对象')\n} else if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.get) {\n  // ios\n  window.jb_app = {\n    get: function get(key, url) {\n      var get_data = {\n        key: key,\n        url: url\n      };\n      window.webkit.messageHandlers.get.postMessage(get_data);\n    },\n    post: function post(key, url, data) {\n      var post_data = {\n        key: key,\n        url: url,\n        data: data\n      };\n      window.webkit.messageHandlers.post.postMessage(post_data);\n    },\n    ios: true\n  };\n} else {\n  //cfg.showMsg('没有window.jb_app对象，创建一个虚拟的')\n  window.jb_app = {\n    get: function get(key, url, mock_data) {\n      var rt_data = mock_data || {\n        data: '顺利GET'\n      };\n      rt_data.key = key;\n      jb_js.dispatch(rt_data);\n    },\n    post: function post(key, url, data, mock_data) {\n      var rt_data = mock_data || {\n        data: '顺利POST'\n      };\n      rt_data.key = key;\n      jb_js.dispatch(rt_data);\n    },\n    fake: true\n  };\n}\n\nvar jb_js = {\n  get: function get(url, callback, mock_data) {\n    //cfg.showMsg('调用333jb_js.get')\n    var fun_key = _uuid();\n\n    jb_js['_fun_' + fun_key] = callback;\n\n    if (window.jb_app.fake) {\n      window.jb_app.get(fun_key, url, mock_data);\n    } else {\n      window.jb_app.get(fun_key, url);\n    } //cfg.showMsg('调用jb.js.get结束')\n\n  },\n  post: function post(url, data, callback, mock_data) {\n    var fun_key = _uuid();\n\n    jb_js['_fun_' + fun_key] = callback;\n\n    if (window.jb_app.fake) {\n      window.jb_app.post(fun_key, url, data, mock_data);\n    } else if (window.jb_app.ios) {\n      window.jb_app.post(fun_key, url, data);\n    } else {\n      window.jb_app.post(fun_key, url, JSON.stringify(data));\n    }\n  },\n  dispatch: function dispatch(resp) {\n    //var resp= JSON.parse(resp_str)\n    //cfg.showMsg('进入dispatch')\n    //cfg.showMsg( JSON.stringify(resp))\n    var key = resp.key;\n    jb_js['_fun_' + key](resp);\n    delete jb_js['_fun_' + key];\n  }\n};\nvar search_args = ex.parseSearch();\n\nif (search_args.client == 'web') {\n  if (search_args.baseurl) {\n    var baseurl = atob(search_args.baseurl);\n  } else {\n    alert('必输传入 baseurl');\n  }\n\n  jb_js = {\n    get: function get(url, callback) {\n      //alert(\"进入web GET请求方式\")\n      //var  baseurl =   'http://appplus.rrystv.com'\n      $.ajax({\n        url: baseurl + url,\n        headers: {\n          Authorization: 'Bearer ' + search_args.token,\n          'x-api-version': '2.2',\n          'x-device': search_args.xdevice ? atob(search_args.xdevice) : ''\n        },\n        type: \"GET\",\n        success: function success(data) {\n          //alert(JSON.stringify(data))\n          callback(data);\n        } //'Content-Type':'application/josn;charset=UTF-8'\n\n      }).fail(function (jqXHR, textStatus) {\n        cfg.hide_load();\n\n        if (jqXHR.status == 401) {\n          cfg.showError('请先登录！');\n        } else {\n          cfg.showError(textStatus);\n        }\n      });\n    },\n    post: function post(url, data, callback) {\n      //alert(\"进入web POST请求方式\")\n      //var baseurl = 'http://appplus.rrystv.com'\n      $.ajax({\n        url: baseurl + url,\n        data: JSON.stringify(data),\n        headers: {\n          Authorization: 'Bearer ' + search_args.token,\n          'x-api-version': '2.0',\n          'x-device': search_args.xdevice ? atob(search_args.xdevice) : '',\n          'Content-Type': 'application/json'\n        },\n        type: \"post\",\n        success: function success(data) {\n          //alert(JSON.stringify(data))\n          callback(data);\n        }\n      }).fail(function (jqXHR, textStatus) {\n        cfg.hide_load();\n\n        if (jqXHR.status == 401) {\n          cfg.showError('请先登录！');\n        } else {\n          cfg.showError(textStatus);\n        }\n      });\n    }\n  };\n}\n\nwindow.jb_js = jb_js;\n\nfunction _uuid() {\n  var d = Date.now();\n\n  if (typeof performance !== 'undefined' && typeof performance.now === 'function') {\n    d += performance.now(); //use high-precision timer if available\n  }\n\n  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {\n    var r = (d + Math.random() * 16) % 16 | 0;\n    d = Math.floor(d / 16);\n    return (c === 'x' ? r : r & 0x3 | 0x8).toString(16);\n  });\n}\n\n//# sourceURL=webpack:///./activity_v2/network.js?");

/***/ }),

/***/ "./activity_v2/scss/shou_cun.scss":
/*!****************************************!*\
  !*** ./activity_v2/scss/shou_cun.scss ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// style-loader: Adds some css to the DOM by adding a <style> tag\n\n// load the styles\nvar content = __webpack_require__(/*! !../../../../../../../coblan/webcode/node_modules/css-loader!../../../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./shou_cun.scss */ \"../../../../../coblan/webcode/node_modules/css-loader/index.js!../../../../../coblan/webcode/node_modules/sass-loader/lib/loader.js!./activity_v2/scss/shou_cun.scss\");\nif(typeof content === 'string') content = [[module.i, content, '']];\n// add the styles to the DOM\nvar update = __webpack_require__(/*! ../../../../../../../coblan/webcode/node_modules/style-loader/addStyles.js */ \"../../../../../coblan/webcode/node_modules/style-loader/addStyles.js\")(content, {});\nif(content.locals) module.exports = content.locals;\n// Hot Module Replacement\nif(false) {}\n\n//# sourceURL=webpack:///./activity_v2/scss/shou_cun.scss?");

/***/ }),

/***/ "./activity_v2/shou_cun.js":
/*!*********************************!*\
  !*** ./activity_v2/shou_cun.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("__webpack_require__(/*! ./scss/shou_cun.scss */ \"./activity_v2/scss/shou_cun.scss\");\n\nVue.component('com-shouchun', {\n  template: \"<div class=\\\"com-shouchun\\\">\\n\\n    <!--<button @click=\\\"update_data()\\\">\\u83B7\\u53D6</button>-->\\n\\n    <table>\\n    <tr v-for=\\\"row in rows\\\">\\n        <td v-for=\\\"head in heads\\\"  :class=\\\"head.scls\\\">\\n            <div   v-if=\\\"row[head.name]\\\" v-text=\\\"head.top_label\\\"></div>\\n            <div v-text=\\\"row[head.name]\\\"></div>\\n        </td>\\n        <td class=\\\"mybtn-col\\\">\\n            <div :class=\\\"['mybtn',{disabled:!row.submitable}]\\\" @click=\\\"submit(row)\\\"><span class=\\\"center-vh\\\" style=\\\"white-space: nowrap\\\" v-text=\\\"action_label(row)\\\"></span></div>\\n        </td>\\n    </tr>\\n    </table>\\n    </div>\",\n  data: function data() {\n    return {\n      heads: [{\n        name: 'label',\n        scls: 'big-col',\n        top_label: ''\n      }, {\n        name: 'chargeTime',\n        scls: 'data-col',\n        top_label: '存款'\n      }, {\n        name: 'amount',\n        scls: 'data-col',\n        top_label: '存入'\n      }, {\n        name: 'bonus',\n        scls: 'data-col green',\n        top_label: '可得红利'\n      }],\n      rows: []\n    };\n  },\n\n  /*\r\n   \"chargeTime\": \"2019-01-09T11:34:28.207Z\",\r\n   \"amount\": 0,\r\n   \"bonus\": 0,\r\n   \"Done\": true\r\n  * */\n  mounted: function mounted() {\n    var self = this; //setTimeout(function(){\n\n    self.update_data(); //},5000)\n  },\n  methods: {\n    action_label: function action_label(row) {\n      var dc = {\n        0: '参加活动',\n        1: '已参加',\n        2: '已发放',\n        3: '已过期'\n      };\n      return dc[row.state];\n    },\n    update_data: function update_data() {\n      //cfg.showMsg('开始更新数据')\n      var mock_data = {\n        data: [{\n          chargeTime: '04-21 22:30',\n          amount: 50,\n          bonus: 50,\n          state: 1\n        }, {\n          chargeTime: '2019-01-22 22:30:30',\n          amount: '100000',\n          bonus: '1239999',\n          state: 0\n        }]\n      };\n      var dec_rows = [{\n        label: '首存',\n        action: '',\n        submitable: false\n      }, {\n        label: '再存',\n        action: '',\n        submitable: false\n      }];\n      var self = this;\n      cfg.show_load();\n      jb_js.get('/activity/charge/list?activityId=' + activity.pk, function (resp) {\n        cfg.hide_load(); //cfg.showMsg('首存数据:'+JSON.stringify(resp))\n\n        self.rows = resp.data;\n        var last_done = true;\n\n        for (var i = 0; i < self.rows.length; i++) {\n          var row = self.rows[i];\n          ex.vueAssign(row, dec_rows[i]);\n          row.Type = i + 1;\n\n          if (row.state != 0) {\n            last_done = true;\n          } else if (last_done) {\n            row.submitable = true;\n            last_done = false;\n          }\n        } //cfg.showMsg('追踪数据:'+JSON.stringify(self.rows))\n\n      }, mock_data);\n    },\n    submit: function submit(row) {\n      if (!row.submitable) {\n        return;\n      }\n\n      var mock_data = {\n        success: 1\n      };\n      var post_data = {\n        ActivityId: activity.pk,\n        Type: row.Type\n      };\n      var self = this;\n      jb_js.post('/activity/charge/do', post_data, function (resp) {\n        if (resp.success) {\n          cfg.showMsg('参加成功！');\n          self.update_data();\n        } else {\n          cfg.showError(resp.error_description);\n        }\n      }, mock_data);\n    }\n  }\n});\n\n//# sourceURL=webpack:///./activity_v2/shou_cun.js?");

/***/ })

/******/ });