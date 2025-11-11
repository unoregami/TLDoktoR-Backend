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
  const summary = data.summaryToShow || "No summary text was found.";
  summaryText.value = summary;

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
  "Egyptian",
  "Esperanto",
  "Estonian",
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
  "Luxembourgish",
  "Luo",
  "Magahi",
  "Maithili",
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
  "Swahili",
  "Swati",
  "Swedish",
  "Tamil",
  "Tamasheq",
  "Tatar",
  "Tajik",
  "Taglish",
  "Ta'izzi Adeni",
  "Telugu",
  "Thai",
  "Tibetan",
  "Tigrinya",
  "Tok Pisin",
  "Tosk Albanian",
  "Tumbuka",
  "Tunisian",
  "Turkish",
  "Turkmen",
  "Twi",
  "Uyghur",
  "Ukrainian",
  "Urdu",
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

  translateBtn.addEventListener("click", async () => {
    const text = summaryText.value;
    const selected = dropdownLabel.textContent;
    const original = summaryText.value;
    summaryText.value = `🌐 [Translated to ${selected}] ${summary}`;

    // Fetch text and language to backend
    to_translate(text, selected)
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


  let ttsActive = false;
  ttsBtn.addEventListener("click", () => {
    if (ttsActive) {
      speechSynthesis.cancel();
      ttsActive = false;
      ttsBtn.classList.remove("tts-active");
    } else {
      const utterance = new SpeechSynthesisUtterance(summaryText.value);
      utterance.lang = "en-US";
      speechSynthesis.speak(utterance);
      ttsActive = true;
      ttsBtn.classList.add("tts-active");
      utterance.onend = () => {
        ttsActive = false;
        ttsBtn.classList.remove("tts-active");
      };
    }
  });
});
