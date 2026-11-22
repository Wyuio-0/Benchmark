'use strict';

// 【安全警示】不可用于新CRM账单鉴权：不同的18位客户编号经Number转换后可能相等，导致客户读取他人账单。
function sameCustomerId(a, b) {
  return Number(a) === Number(b);
}

module.exports = { sameCustomerId };
