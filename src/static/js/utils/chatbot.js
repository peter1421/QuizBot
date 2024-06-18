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
  return `${card.rarity}<br><strong>提示：</strong>${card.fortune}`;
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
  const chatMessageClass =
    side === "assistant"
      ? " chat-message btn btn-outline-primary mt-2"
      : "chat-message";
  const chatUser = setUser(imgSrc, time);
  messageText = escapeHtml(messageText);
  let sendMessageText = messageText;
  let voiceText = "";
  let chatContent = "";
  if (messageText) {
    if (side === "assistant") {
      sendMessageText += "🔉";
    }
    chatContent += setMessage(sendMessageText);
  }
  if (imagesUrl) {
    chatContent += setImage(imagesUrl);
  }
  return `
      <div class="chat${sideClass}">
        ${chatUser}
        <div class="chat-detail">
            <div class="${chatMessageClass}" onclick="speak('${messageText}')">
                ${chatContent}
          </div>
        </div>
      </div>`;
}
function speak(text, lang = "zh-TW") {
  // 創建一個新的 SpeechSynthesisUtterance 實例
  var utterance = new SpeechSynthesisUtterance(text);

  // 選擇語音。這裡使用函數參數指定的語言
  var voices = window.speechSynthesis.getVoices();
  utterance.voice = voices.find((voice) => voice.lang === lang);

  // 如果沒有找到指定語言的語音，可以選擇第一個可用的語音
  if (!utterance.voice) {
    utterance.voice = voices[0];
  }

  // 設置其他屬性，如語速和音調
  utterance.rate = 2; // 語速，範圍從0.1至10，預設為1
  utterance.pitch = 1; // 音調，範圍從0至2，預設為1

  // 將utterance傳給speechSynthesis介面
  window.speechSynthesis.speak(utterance);
}
