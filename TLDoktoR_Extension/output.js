window.addEventListener('DOMContentLoaded', async () => {
  const summaryText = document.getElementById('summaryText');
  const translateBtn = document.getElementById('translateBtn');
  const ttsBtn = document.getElementById('ttsBtn');
  const copyBtn = document.getElementById('copyBtn');
  const dropdown = document.getElementById('languageDropdown');
  const dropdownToggle = document.getElementById('dropdownToggle');
  const dropdownLabel = document.getElementById('dropdownLabel');
  const languageSearch = document.getElementById('languageSearch');
  const languageList = document.getElementById('languageList');

  console.log("Output window loaded. Attempting to retrieve summary from storage...");
  const data = await chrome.storage.local.get('summaryToShow');
  const summaryObject = data.summaryToShow || "No summary text was found.";
  const summaryTextContent = (typeof summaryObject === 'object' && summaryObject.summary) ? summaryObject.summary : summaryObject;

  summaryText.value = summaryTextContent;

  await chrome.storage.local.remove('summaryToShow');
  console.log("Summary loaded and storage has been cleared");

  const languages = [
    "Taglish",
    "Filipino",
    "English",
    "Acehnese",
    "Afrikaans",
    "Akan",
    "Amharic",
    "Arabic",
    "Armenian",
    "Assamese",
    "Asturian",
    "Awadhi",
    "Ayacucho Quechua",
    "Balinese",
    "Bambara",
    "Banjar",
    "Bashkir",
    "Basque",
    "Belarusian",
    "Bemba",
    "Bengali",
    "Bhojpuri",
    "Bokmal",
    "Bosnian",
    "Bulgarian",
    "Buginese",
    "Burmese",
    "Catalan",
    "Cebuano",
    "Central Atlas Tamazight",
    "Central Aymara",
    "Central Kurdish",
    "Chhattisgarhi",
    "Chinese Simplified",
    "Chinese Traditional",
    "Chokwe",
    "Crimean Tatar",
    "Croatian",
    "Czech",
    "Danish",
    "Dari",
    "Dutch",
    "Dyula",
    "Dzongkha",
    "Eastern Punjabi",
    "Egyptian",
    "Esperanto",
    "Estonian",
    "Ewe",
    "Faroese",
    "Fijian",
    "Finnish",
    "Fon",
    "French",
    "Friulian",
    "Fulfulde",
    "Galician",
    "Ganda",
    "Georgian",
    "German",
    "Greek",
    "Guarani",
    "Gujarati",
    "Haitian Creole",
    "Halh Mongolian",
    "Hausa",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Igbo",
    "Ilocano",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Javanese",
    "Jingpho",
    "Kabyle",
    "Kabuverdianu",
    "Kabiye",
    "Kamba",
    "Kannada",
    "Kanuri",
    "Kashmiri",
    "Kazakh",
    "Khmer",
    "Kikongo",
    "Kikuyu",
    "Kimbundu",
    "Kinyarwanda",
    "Korean",
    "Kyrgyz",
    "Lao",
    "Latgalian",
    "Latvian",
    "Ligurian",
    "Limburgish",
    "Lingala",
    "Lithuanian",
    "Lombard",
    "Luo",
    "Luxembourgish",
    "Macedonian",
    "Magahi",
    "Maithili",
    "Malagasy",
    "Malay",
    "Malayalam",
    "Maltese",
    "Maori",
    "Marathi",
    "Meitei",
    "Mesopotamian",
    "Minangkabau",
    "Mizo",
    "Mongolian",
    "Moroccan",
    "Mossi",
    "Najdi",
    "Nepali",
    "North Azerbaijani",
    "North Levantine",
    "Northern Kurdish",
    "Northern Sotho",
    "Nuer",
    "Nyanja",
    "Nynorsk",
    "Occitan",
    "Odia",
    "Oromo",
    "Pangasinan",
    "Papiamento",
    "Pashto",
    "Persian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Rundi",
    "Russian",
    "Samoan",
    "Sango",
    "Sanskrit",
    "Santali",
    "Sardinian",
    "Scottish Gaelic",
    "Serbian",
    "Shan",
    "Shona",
    "Sicilian",
    "Silesian",
    "Sindhi",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "South Azerbaijani",
    "South Levantine",
    "Southern Sotho",
    "Southwestern Dinka",
    "Spanish",
    "Sundanese",
    "Swahili",
    "Swati",
    "Swedish",
    "Ta'izzi Adeni",
    "Tajik",
    "Tamasheq",
    "Tamil",
    "Tatar",
    "Telugu",
    "Thai",
    "Tibetan",
    "Tigrinya",
    "Tok Pisin",
    "Tosk Albanian",
    "Tsonga",
    "Tswana",
    "Tumbuka",
    "Tunisian",
    "Turkish",
    "Turkmen",
    "Twi",
    "Ukrainian",
    "Urdu",
    "Uyghur",
    "Uzbek",
    "Venetian",
    "Vietnamese",
    "Waray",
    "Welsh",
    "Wolof",
    "Xhosa",
    "Yiddish",
    "Yoruba",
    "Yue Chinese",
    "Zulu"

];
  const original = summaryText.value;

  // Translation function
  async function to_translate(text, lang) {
    const response = await fetch('http://127.0.0.1:8000/to-translate', {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text,
        lang: lang
      })
    });
    return response.json()
  }

  // Audio buffer
  async function playAudioBuffer(buffer) {
    if (audioContext.state === 'suspended') {
      audioContext.resume();
    }

    const source = audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(audioContext.destination);

    currentAudioSource = source;

    source.onended = () => {
      currentAudioSource = null;
      ttsBtn.innerHTML = '<span class="material-symbols-outlined">volume_mute</span>';
    };

    source.start(0);
    ttsBtn.innerHTML = '<span class="material-symbols-outlined">brand_awareness</span>';
  }

  function renderLanguages(list) {
    languageList.innerHTML = "";
    list.forEach(lang => {
      const li = document.createElement("li");
      li.textContent = lang;
      li.addEventListener("click", () => {
        dropdownLabel.textContent = lang;
        dropdown.classList.remove("open");
      });
      languageList.appendChild(li);
    });
  }

  renderLanguages(languages);

  dropdownToggle.addEventListener("click", () => {
    dropdown.classList.toggle("open");
    languageSearch.value = "";
    renderLanguages(languages);
  });

  languageSearch.addEventListener("input", () => {
    const query = languageSearch.value.toLowerCase();
    const filtered = languages.filter(l => l.toLowerCase().includes(query));
    renderLanguages(filtered);
  });

  // Close dropdown when clicking outside
document.addEventListener("click", (event) => {
  if (
    !dropdown.contains(event.target) && // click is outside the dropdown
    !dropdownToggle.contains(event.target) // and not the toggle button
  ) {
    dropdown.classList.remove("open"); // close it
  }
});

  let currentLanguageCode = 'en'; // Global lang code variable
  translateBtn.addEventListener("click", async () => {
    const text = original;
    const selected = dropdownLabel.textContent;
    
    
    translateBtn.textContent = "Translating...";
    translateBtn.disabled = true;
    dropdownToggle.disabled = true;
    setTimeout( async () => {
      // Fetch text and language to backend
      const translated = await to_translate(text, selected);

      summaryText.value = translated.text;
      currentLanguageCode = translated.gtts_target;
      dropdownLabel.textContent = `${selected} (Original)`;

      setTimeout(() => {
        translateBtn.textContent = "Translate";
        translateBtn.disabled = false;
        dropdownToggle.disabled = false;
      }, 3000);
    }, 800);
    
  });

  copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(summaryText.value).then(() => {
      const toast = document.getElementById("copyToast");
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 1500);
    });
  });




  //copyBtn.addEventListener("click", () => {
   // navigator.clipboard.writeText(summaryText.value).then(() => {
      // optional: console.log or a toast instead of changing button text
   //   console.log("Copied to clipboard!");
   //   copyBtn.classList.add('show');
  //  }).catch(err => {
    //  console.error("Failed to copy: ", err);
   // });
  //});


  let audioContext = null;
  let currentAudioSource = null;
  let currentAudioBuffer = null;
  let cachedText = null;

  ttsBtn.addEventListener("click", async () => {
    if (currentAudioSource) {
      console.log("Stopping TTS.");
      currentAudioSource.stop();
      return
    }
    
    const textToSpeech = summaryText.value
    if (!textToSpeech.trim()) {
      console.log("Text empty, not playing speech.");
      return;
    }

    if (cachedText === textToSpeech && currentAudioBuffer) {
      console.log("Playing audio from cache.");
      playAudioBuffer(currentAudioBuffer);
      return;
    }

    console.log("Fetching new audio from server.");
    const selectedLanguage = currentLanguageCode;

    const formData = new URLSearchParams();
    formData.append('text', textToSpeech);
    formData.append('lang', selectedLanguage);

    ttsBtn.innerHTML = '<span class="material-symbols-outlined">cycle</span>';

    await fetch('http://127.0.0.1:8000/play-speech', {
      method: "POST",
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.arrayBuffer();
      })
      .then(arrayBuffer => {
        if (!audioContext) {
          audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        audioContext.decodeAudioData(arrayBuffer, (buffer) => {
          currentAudioBuffer = buffer;
          cachedText = textToSpeech;

          playAudioBuffer(currentAudioBuffer);
        });
      })
      .catch(error => {
        console.error('Error fetching or playing audio:', error);
        currentAudioSource = null;
        currentAudioBuffer = null;
        cachedText = null;
        ttsBtn.innerHTML = '<span class="material-symbols-outlined">volume_mute</span>';
    }); 
    
    ttsBtn.innerHTML = '<span class="material-symbols-outlined">volume_mute</span>';
  });
});
