function toDo(message) {
  alert(message);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function clearCookies() {
  // 获取所有 cookies
  var cookies = document.cookie.split(";");

  // 循环遍历并清除每一个 cookie
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    var eqPos = cookie.indexOf("=");
    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
  }

  // 清除后的提示
  alert("所有 cookies 已清除！");
}

// 格式化時間為 HH:MM 格式
function formattedTime(date) {
  return `${date.getHours()}:${date.getMinutes().toString().padStart(2, "0")}`;
}

function escapeHtml(unsafe) {
  if (!unsafe) return ""; // 如果輸入為 null 或 undefined，返回空字串
  let safeOutput=DOMPurify.sanitize(unsafe, {ALLOWED_TAGS: ['br', 'b', 'i', 'em', 'strong']});
  // 轉義 HTML 特殊字符
  // let safeOutput = unsafe
  //     .replace(/&/g, "&amp;")
  //     .replace(/</g, "&lt;")
  //     .replace(/>/g, "&gt;")
  //     .replace(/"/g, "&quot;")
  //     .replace(/'/g, "&#039;");

  // // 進一步處理以移除或禁用危險的 URL 協議（如 JavaScript:）
  // safeOutput = safeOutput.replace(/javascript:/gi, "javascript&#58;");

  // // 清理危險的 CSS 代碼（例如 expression、url 使用 JavaScript）
  // safeOutput = safeOutput.replace(/expression\((.*?)\)/gi, ""); // 清除 CSS 表達式
  // safeOutput = safeOutput.replace(/url\((.*?)\)/gi, (match) => {
  //     // 如果 URL 中包含不安全的協議，則移除整個 URL()
  //     if (/javascript:/gi.test(match)) {
  //         return "";
  //     }
  //     return match;
  // });

  return safeOutput;
}
