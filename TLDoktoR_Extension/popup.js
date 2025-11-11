window.addEventListener('DOMContentLoaded', () => {
  const inputText = document.getElementById('inputText');
  const youtubeUrl = document.getElementById('youtubeUrl');
  const summarizeBtn = document.getElementById('summarizeBtn');
  const fetchYoutubeBtn = document.getElementById('fetchYoutubeBtn');
  const summarizeYoutubeBtn = document.getElementById('summarizeYoutubeBtn');
  const youtubeControls = document.getElementById('youtubeControls');
  const rangeSliderContainer = document.getElementById('rangeSliderContainer');
  
  // Summary Length Slider Elements
  const lengthSlider = document.getElementById('lengthSlider');
  const lengthDisplay = document.getElementById('lengthDisplay');
  const lengthSliderFill = document.getElementById('lengthSliderFill');
  
  // Double Range Slider Elements
  const minSlider = document.getElementById('minSlider');
  const maxSlider = document.getElementById('maxSlider');
  const minValue = document.getElementById('minValue');
  const maxValue = document.getElementById('maxValue');
  const sliderRange = document.getElementById('sliderRange');
  
  // Time Input Elements
  const startTimeInput = document.getElementById('startTimeInput');
  const endTimeInput = document.getElementById('endTimeInput');

  // Placeholder variables
  let currentSummary = "🧠 Placeholder summary text for testing UI features.";
  const availableLanguages = ["Taglish", "Filipino", "Japanese", "Korean", "Spanish", "German", "French"];
  
  const lengthOptions = ['Short', 'Medium', 'Long'];
  let selectedLength = 'Short';

  // === Helper Functions ===
  async function print_to_console(summaryText) {
    const response = await fetch('http://127.0.0.1:8000/print', {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({value: summaryText})
    });
    return response.json()
  }

  function openSummaryWindow(summaryText) {
    const encoded = encodeURIComponent(summaryText);
  
    // Calculate center position for popup
    const width = 1000;
    const height = 800;
    const left = Math.round((screen.availWidth - width) / 2);
    const top = Math.round((screen.availHeight - height) / 2);

    chrome.windows.create({
      url: `output.html?summary=${encoded}`,
      type: "popup",
      width,
      height,
      left,
      top
    });
  }

  // Convert seconds to mm:ss format
  function secondsToTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  // Convert mm:ss to seconds
  function timeToSeconds(timeStr) {
    const parts = timeStr.split(':');
    if (parts.length !== 2) return null;
    
    const mins = parseInt(parts[0]);
    const secs = parseInt(parts[1]);
    
    if (isNaN(mins) || isNaN(secs) || secs >= 60 || secs < 0) return null;
    
    return mins * 60 + secs;
  }

  // === Summary Length Slider Logic ===
  function updateLengthSlider() {
    const value = parseInt(lengthSlider.value);
    selectedLength = lengthOptions[value];

    // Update fill bar (0 = 0%, 1 = 50%, 2 = 100%)
    const percent = value * 50;
    lengthSliderFill.style.width = percent + '%';

    // Remove active state from all labels
    document.getElementById('labelShort').classList.remove('active');
    document.getElementById('labelMedium').classList.remove('active');
    document.getElementById('labelLong').classList.remove('active');

    // Add active state to selected label
    if (value === 0) document.getElementById('labelShort').classList.add('active');
    if (value === 1) document.getElementById('labelMedium').classList.add('active');
    if (value === 2) document.getElementById('labelLong').classList.add('active');
  }
lengthSlider.addEventListener('input', updateLengthSlider);
updateLengthSlider();

  function updateSlider() {
    minVal = parseInt(minSlider.value);
    maxVal = parseInt(maxSlider.value);

    // Prevent sliders from crossing
    if (minVal >= maxVal) {
      minSlider.value = maxVal - 1;
      minVal = maxVal - 1;
    }

    if (maxVal <= minVal) {
      maxSlider.value = minVal + 1;
      maxVal = minVal + 1;
    }

    // Update display values in mm:ss format
    minValue.textContent = secondsToTime(minVal);
    maxValue.textContent = secondsToTime(maxVal);
    
    // Update input fields
    startTimeInput.value = secondsToTime(minVal);
    endTimeInput.value = secondsToTime(maxVal);

    // Update visual range bar
    const percent1 = (minVal / minSlider.max) * 100;
    const percent2 = (maxVal / maxSlider.max) * 100;
    
    sliderRange.style.left = percent1 + '%';
    sliderRange.style.width = (percent2 - percent1) + '%';
  }

  minSlider.addEventListener('input', updateSlider);
  maxSlider.addEventListener('input', updateSlider);

  // === Time Input Fields Logic ===
  startTimeInput.addEventListener('change', () => {
    const seconds = timeToSeconds(startTimeInput.value);
    
    if (seconds !== null && seconds >= 0 && seconds < maxVal) {
      minSlider.value = seconds;
      minVal = seconds;
      updateSlider();
    } else {
      // Reset to current value if invalid
      startTimeInput.value = secondsToTime(minVal);
      alert('⚠️ Invalid start time. Use format mm:ss (e.g., 1:30)');
    }
  });

  endTimeInput.addEventListener('change', () => {
    const seconds = timeToSeconds(endTimeInput.value);
    
    if (seconds !== null && seconds > minVal && seconds <= parseInt(maxSlider.max)) {
      maxSlider.value = seconds;
      maxVal = seconds;
      updateSlider();
    } else {
      // Reset to current value if invalid
      endTimeInput.value = secondsToTime(maxVal);
      alert('⚠️ Invalid end time. Use format mm:ss (e.g., 5:00)');
    }
  });

  // Initialize slider
  updateSlider();

  // === Summarize Text Placeholder ===
  summarizeBtn.addEventListener('click', () => {
    const text = inputText.value.trim();
    if (!text) {
      alert("⚠️ Please enter text to summarize.");
      return;
    }

    const fakeSummary = `

Ang matter ay anumang may mass at sumasakop sa space, ibig sabihin ay may volume. Ito ang "stuff" na gawa ng universe mula sa hangin na inaagos natin hanggang sa lupa na ating tinatahak at binubuo ng mga fundamental particles tulad ng atoms at molecules .Ang pinaka-karaniwang estado ng bagay ay solid, liquid, at gas, bagaman may iba pang mga estado tulad ng plasma

`;
    // openSummaryWindow(fakeSummary);
    print_to_console(fakeSummary)
  });

  // === Fetch YouTube Placeholder ===
fetchYoutubeBtn.addEventListener('click', () => {
  const url = youtubeUrl.value.trim();
  if (!url) {
    alert("⚠️ Please paste a YouTube URL first.");
    return;
  }

  // Simulate fetching process
  fetchYoutubeBtn.textContent = "Fetching...";
  fetchYoutubeBtn.disabled = true;

  setTimeout(() => {
    fetchYoutubeBtn.textContent = "Fetched ✓";
    rangeSliderContainer.classList.add('show');
    youtubeControls.style.display = "flex";
    updateSlider();

    // After 1 second, revert back to Fetch
    setTimeout(() => {
      fetchYoutubeBtn.textContent = "Fetch";
      fetchYoutubeBtn.disabled = false;
    }, 3000);
  }, 800);
});

  // === Summarize YouTube Placeholder ===
  summarizeYoutubeBtn.addEventListener('click', () => {
    if (youtubeControls.style.display !== "flex") {
      alert("⚠️ Fetch video first.");
      return;
    }

    const fakeSummary = `🎥 Placeholder ${selectedLength.toLowerCase()} summary for YouTube video from ${secondsToTime(minVal)} to ${secondsToTime(maxVal)}.`;
    openSummaryWindow(fakeSummary);
  });
});