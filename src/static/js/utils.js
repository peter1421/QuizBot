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

function speak(text) {
  // 創建一個新的 SpeechSynthesisUtterance 實例
  var utterance = new SpeechSynthesisUtterance(text);

  // 選擇語音。這是可選的，也可以留空使用系統預設語音
  var voices = window.speechSynthesis.getVoices();
  utterance.voice = voices.filter(function (voice) {
    return voice.lang === "zh-TW";
  })[0]; // 選擇特定語言的語音，這裡以繁體中文為例

  // 設置其他屬性，如語速和音調
  utterance.rate = 1; // 語速，範圍從0.1至10，預設為1
  utterance.pitch = 1; // 音調，範圍從0至2，預設為1

  // 將utterance傳給speechSynthesis介面
  window.speechSynthesis.speak(utterance);
}
