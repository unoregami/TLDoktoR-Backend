chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "summarizeText",
    title: "TLDoktoR: Summarize this text",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "summarizeText") {
    const selectedText = info.selectionText;

    if (!selectedText) {
      alert("No text selected!");
      return;
    }

    // Placeholder summary for testing
    const summary = "Ang matter ay anumang may mass at sumasakop sa space, ibig sabihin ay may volume. Ito ang stuf na gawa ng universe mula sa hangin na inaagos natin hanggang sa lupa na ating tinatahak at binubuo ng mga fundamental particles tulad ng atoms at molecules .Ang pinaka-karaniwang estado ng bagay ay solid, liquid, at gas, bagaman may iba pang mga estado tulad ng plasma";

    // Open summary-output.html with the summary as a query param
    const url = chrome.runtime.getURL("output.html") + `?summary=${encodeURIComponent(summary)}`;

    chrome.windows.create({
      url,
      type: "popup",
      width: 1000,
      height: 800
    });

    try {
      const response = await fetch('http://127.0.0.1:8000/summarize_text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: selectedText, summary_type: 'medium' })
      });

      const data = await response.json();

      if (!response.ok) {
        alert("API error: " + (data.error || "Unknown error"));
        return;
      }

      const summary = data.summary;

      const url = chrome.runtime.getURL("summary-output.html") + `?summary=${encodeURIComponent(summary)}`;

      chrome.windows.create({
        url,
        type: "popup",
        width: 400,
        height: 600
      });

    } catch (error) {
      alert("Failed to connect to summarization API.");
    }
  }
});