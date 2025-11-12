chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "summarizeText",
    title: "TLDoktoR: Summarize this text",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info) => {
  // Fetch to summarize text and length
  async function to_summarize(text) {
    try {
      const response = await fetch('http://127.0.0.1:8000/to-summarize', {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: text,
          length: 2
        })
      });

      if (!response.ok) {
        const error = await response.json();
        console.error('Error:', error);
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();

      console.log("Received data from server:", data);
      
      return data.summary;

    } catch (error) {
      console.error("Failed to fetch summary:", error);
      return "Error occured while generating summary. Please check console."
    }
  }

  function openSummaryWindow(summaryText) {
    // Calculate center position for popup
    const width = 1000;
    const height = 800;

    chrome.windows.create({
      url: 'output.html',
      type: "popup",
      width,
      height,
    });
  }

  if (info.menuItemId === "summarizeText") {
    const selectedText = info.selectionText;

    if (!selectedText) {
      alert("No text selected!");
      return;
    }

    const summary = await to_summarize(selectedText)
    
      await chrome.storage.local.set({ summaryToShow: summary });
      await openSummaryWindow();
  }
});