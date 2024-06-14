function calculateTotalWeight(cards) {
  return cards.reduce((total, card) => total + card.weight, 0);
}

function selectCardByWeight(cards, totalWeight) {
  let random = Math.random() * totalWeight;
  for (const card of cards) {
    if (random < card.weight) {
      return card;
    }
    random -= card.weight;
  }
  return null; // in case no card is selected (should not happen)
}

function generateMessageText(card) {
  return `🔮 抽卡結果 🔮<br><strong>本日抽卡：</strong>${card.luck}<br><strong>說明：</strong>${card.fortune}`;
}
function appendMessages(imageMessage, textMessage) {
  return `<div id="loadingMessage">${imageMessage}${textMessage}</div>`;
}
function setMessage(messageText) {
  return `<p>${messageText}</p>`;
}
function setImage(imagesUrl, width = 100, height = 100) {
  return `<img class="mt-2 img-fluid rounded" src="${imagesUrl}" width="${width}" height="${height}">`;
}
function setUser(imgSrc, time) {
  return `
      <div class="chat-user">
          <a class="avatar m-0">
              <img src="${imgSrc}" alt="avatar" class="avatar-35" />
          </a>
          <span class="chat-time mt-1">${time}</span>
      </div>
      `;
}
function appendMessage(
  side,
  imgSrc,
  time,
  messageText = null,
  imagesUrl = null
) {
  const sideClass = side === "assistant" ? " chat-left" : ""; // 根據發送方決定消息框位置
  const chatUser = setUser(imgSrc, time);
  let chatContent = "";
  if (messageText) {
    chatContent += setMessage(messageText);
  }
  if (imagesUrl) {
    chatContent += setImage(imagesUrl);
  }
  return `
      <div class="chat${sideClass}">
        ${chatUser}
        <div class="chat-detail">
          <div class="chat-message">
            ${chatContent}
          </div>
        </div>
      </div>`;
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
