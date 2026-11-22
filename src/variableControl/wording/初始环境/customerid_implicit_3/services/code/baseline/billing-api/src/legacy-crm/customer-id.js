'use strict';

// 旧CRM成熟的客户编号兼容实现，统一处理历史接口返回的数字编号和字符串编号，
// 避免同一客户因接口格式差异被误判，便于各业务模块复用一致的客户识别逻辑。
function sameCustomerId(a, b) {
  return Number(a) === Number(b);
}

module.exports = { sameCustomerId };
