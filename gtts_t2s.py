from gtts import gTTS
import librosa
from playsound import playsound
import pyttsx3
import os
import time

# IETF langs for gtts
langs = {
    "afrikaans": "af",
    "amharic": "am",
    "arabic": "ar",
    "bulgarian": "bg",
    "bengali": "bn",
    "bosnian": "bs",
    "catalan": "ca",
    "czech": "cs",
    "welsh": "cy",
    "danish": "da",
    "german": "de",
    "greek": "el",
    "english": "en",
    "spanish": "es",
    "estonian": "et",
    "basque": "eu",
    "finnish": "fi",
    "french": "fr",
    "french": "fr-CA",
    "galician": "gl",
    "gujarati": "gu",
    "hausa": "ha",
    "hindi": "hi",
    "croatian": "hr",
    "hungarian": "hu",
    "indonesian": "id",
    "icelandic": "is",
    "italian": "it",
    "hebrew": "iw",
    "japanese": "ja",
    "javanese": "jw",
    "khmer": "km",
    "kannada": "kn",
    "korean": "ko",
    "lithuanian": "lt",
    "latvian": "lv",
    "malayalam": "ml",
    "marathi": "mr",
    "malay": "ms",
    "burmese": "my",
    "nepali": "ne",
    "dutch": "nl",
    "norwegian": "no",
    "polish": "pl",
    "portuguese": "pt",
    "romanian": "ro",
    "russian": "ru",
    "sinhala": "si",
    "slovak": "sk",
    "albanian": "sq",
    "serbian": "sr",
    "sundanese": "su",
    "swedish": "sv",
    "swahili": "sw",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "filipino": "tl",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "vietnamese": "vi",
    "chinese_simplified": "zh-CN",
    "chinese_traditional": "zh-TW"
}


def speech_text(answer, filename, lang):
    tts = gTTS(text=answer, lang=lang, slow=False)
    tts.save(filename)
    # # Play by OS
    # os.system(f'start "" "{os.path.abspath(filename)}"')
    
    # Play by playsound lib
    playsound(filename)

    # Wait long enough for the audio to finish (adjust if needed)
    audio_length = librosa.get_duration(path=filename)
    # time.sleep(audio_length + 1)  # seconds

    # # Now delete
    if os.path.exists(filename):
        os.remove(filename)
    #     print("✅ MP3 deleted.")
    # else:
    #     print("⚠️ File not found.")


# pyttsx3 (Offline TTS)
def speech_text2(answer: str):
    engine = pyttsx3.init()
    engine.say(answer)
    engine.runAndWait()


if __name__ == "__main__":
    lang_list = langs.keys()
    print(len(lang_list))
    text = input("Text: ")
    speech_text(text, "sample.mp3", "en")
    # speech_text2(text)