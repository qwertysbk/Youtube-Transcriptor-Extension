chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.transcript || message.error) {
    chrome.runtime.sendMessage(message);
  }
});
