document.getElementById('extract').addEventListener('click', async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: extractTranscript
  });
});

async function extractTranscript() {
  const videoUrl = window.location.href;

  try {
    const response = await fetch('http://localhost:5000/get_transcript', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: videoUrl })
    });
    const data = await response.json();
    
    // Send the transcript data back to the popup
    chrome.runtime.sendMessage({ transcript: data.transcript });
  } catch (error) {
    chrome.runtime.sendMessage({ error: 'Error fetching transcript: ' + error.message });
  }
}

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.transcript) {
    document.getElementById('transcript').textContent = request.transcript;
  } else if (request.error) {
    document.getElementById('transcript').textContent = request.error;
  }
});
