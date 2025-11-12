from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gtts_t2s
import post_processing as pp
import torch
import spacy
from spacy.lang.tl import Tagalog
import time
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from multiprocessing import Process, Semaphore


# English to Taglish translation
def toTaglish(text, taglish_tokenizer, taglish_model):
    inputs = taglish_tokenizer(text, return_tensors="pt").to(taglish_model.device)

    generated_tokens = taglish_model.generate(
        **inputs,
        forced_bos_token_id=taglish_tokenizer.convert_tokens_to_ids("tgl_Latn"),
        max_length=360
    )
    translation = taglish_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return translation

# Taglish translation multiprocessing (deprecated)
def toTaglish_multiprocessing(text, taglish_tokenizer, taglish_model, semaphore):
    semaphore.acquire()
    inputs = taglish_tokenizer(text, return_tensors="pt").to(taglish_model.device)

    generated_tokens = taglish_model.generate(
        **inputs,
        forced_bos_token_id=taglish_tokenizer.convert_tokens_to_ids("tgl_Latn"),
        max_length=360
    )
    translation = taglish_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    print(translation, end=" ")
    semaphore.release()

# NLLB model
def translate(text, target, NLLB_tokenizer, NLLB_model):
    inputs = NLLB_tokenizer(text, return_tensors="pt").to(NLLB_model.device)

    generated_tokens = NLLB_model.generate(
        **inputs,
        forced_bos_token_id=NLLB_tokenizer.convert_tokens_to_ids(target),
        max_length=360
    )
    translation = NLLB_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return translation

# Translate using multiprocessing (deprecated)
def translate_multiprocessing(text, target, NLLB_tokenizer, NLLB_model, semaphore):
    semaphore.acquire()
    inputs = NLLB_tokenizer(text, return_tensors="pt").to(NLLB_model.device)

    generated_tokens = NLLB_model.generate(
        **inputs,
        forced_bos_token_id=NLLB_tokenizer.convert_tokens_to_ids(target),
        max_length=360
    )
    translation = NLLB_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    print(translation, end=" ")
    semaphore.release()

# Split sentence based on punctuation (deprecated)
def separate_sentences(text):
    split_sentence = []
    ph = ""
    for sentence in text.split(";"):
        sentence = sentence.strip()
        sentence += ";"
        # print(sentence)
        if sentence == ";":
            continue
        ph += sentence

    text = ""
    for sentence in ph.split("?"):
        sentence = sentence.strip()
        sentence += "?"
        # print(sentence)
        if sentence == "?":
            continue
        text += sentence

    ph = ""
    for sentence in text.split("!"):
        sentence = sentence.strip()
        sentence += "!"
        # print(sentence)
        if sentence == "!":
            continue
        ph += sentence

    for sentence in ph.split("."):
        sentence = sentence.strip()
        sentence += "."
        # print(sentence)
        if sentence == ".":
            continue
        split_sentence.append(sentence)

    split_sentence.pop()  # removes the last index (occurs when last sentence ends in a punctuation)

    return split_sentence

# Translate to all NLLB languages
def translate_all():
    text = input("Text: ")
    doc = nlp(text)
    languages = list(nllb_token.keys())

    split_sentences = [sent.text for sent in doc.sents] #separate_sentences(text)
    for lang in languages:
        nllb_target = nllb_token.get(lang) # NLLB target token

        start = time.perf_counter()
        out = ""
        batch = 2
        for i in range(0, len(split_sentences), batch):
            to_be_translated = split_sentences[i]       # Gets first sentence per batch
            for sentence in split_sentences[i+1:i+batch]: to_be_translated += f" {sentence}"    # Preparing sentences to be translated
            out += translate(to_be_translated, nllb_target)

        print(f"{lang}:", out)
        end = time.perf_counter()
        print(f"Time: {end - start:.2f}")
        print()

# Main
def translate_main(text, to, nlp, nlp_tgl, gtts_token, nllb_token, taglish_tokenizer, taglish_model, NLLB_tokenizer, NLLB_model):
    doc = nlp(text)
    split_sentences = [sent.text for sent in doc.sents] #separate_sentences(text)

    start = time.perf_counter()
    if to == "taglish":
        gtts_target = "tl"

        # Batch Processing
        start = time.perf_counter()
        
        out = ""
        batch = 2
        capitalized_dictionary = {}
        for i in range(0, len(split_sentences), batch):
            to_be_translated = ""
            
            # Preparing sentences to be translated
            for sentence in split_sentences[i:i+batch]: 
                to_be_translated += " " + sentence      # concat to be translated sentences
                
                ph = pp.extract_cap_text(sentence, capitalized_dictionary)         # extract capitalized per sentence
                capitalized_dictionary = capitalized_dictionary | ph    # store to main dictionary
            to_be_translated = to_be_translated.lstrip()

            out += " " + toTaglish(to_be_translated, taglish_tokenizer, taglish_model)
        
        # Post Processing
        # print(capitalized_dictionary)
        # print()
        out = pp.post_process(out, capitalized_dictionary, nlp_tgl)

        print(out)
        end = time.perf_counter()
        print(f"Time: {end - start:.2f}")
    else:
        nllb_target = nllb_token.get(to) # NLLB target token
        gtts_target = gtts_token.get(to) # gtts target token
        if gtts_target == None:# edge case for lang with no tts (Sanskrit, Santali, Shan, Uyghur, Yiddish are conlang (Constructed Language))
            match to:
                case "malagasy" | "swati" | "xhosa" | "zulu" | "tsonga":
                    gtts_target = "af"
                case "tigrinya":
                    gtts_target = "am"
                case "central_atlas_tamazight" | "bambara" | "wolof" | "egyptian" | "fulfulde" | "kabyle" | "mesopotamian" | "moroccan" | "najdi" | "north_levantine" | "south_levantine" | "ta'izzi-adeni" | "tamasheq" | "tunisian":
                    gtts_target = "ar"
                case "assamese" | "meitei":
                    gtts_target = "bn"
                case "yiddish":
                    gtts_target = "de"
                case "armenian" | "georgian":
                    gtts_target = "el"
                case "ayacucho_quechua" | "central_aymara" | "papiamento" | "guarani" | "asturian":
                    gtts_target = "es"
                case "occitan" | "mossi":
                    gtts_target = "fr"
                case "bhojpuri" | "maithili" | "awadhi" | "santali" | "chhattisgarhi" | "eastern_punjabi" | "magahi":
                    gtts_target = "hi"
                case "minangkabau" | "balinese" | "acehnese" | "banjar" | "buginese":
                    gtts_target = "id"
                case "sicilian" | "friulian" | "ligurian" | "lombard" | "venetian" | "maltese" | "sardinian":
                    gtts_target = "it"
                case "latgalian":
                    gtts_target = "lt"
                case "shan" | "jingpho":
                    gtts_target = "my"
                case "limburgish" | "luxembourgish":
                    gtts_target = "nl"
                case "faroese" | "bokmal" | "nynorsk":
                    gtts_target = "no"
                case "belarusian" | "kazakh" | "kyrgyz" | "tatar" | "bashkir" | "mongolian" | "crimean_tatar" | "halh_mongolian":
                    gtts_target = "ru"
                case "slovenian":
                    gtts_target = "sk"
                case "macedonian":
                    gtts_target = "sr"
                case "somali" | "tswana" | "shona" | "lingala" | "nyanja" | "rundi" | "bemba" | "tumbuka" | "luo" | "chokwe" | "kamba" | "kikongo" | "kikuyu" | "kimbundu" | "kinyarwanda":
                    gtts_target = "sw"
                case "fon" | "ewe" | "kanuri" | "oromo" | "sango" | "yoruba" | "dyula" | "ganda" | "southwestern_dinka" | "nuer" | "igbo" | "akan" | "haitian_creole" | "kabiye":
                    gtts_target = "ha"
                case "mizo" | "sanskrit":
                    gtts_target = "hi"
                case "silesian":
                    gtts_target = "pl"
                case "kabuverdianu":
                    gtts_target = "pt"
                case "odia":
                    gtts_target = "ta"
                case "lao" | "dzongkha" | "tibetan":
                    gtts_target = "th"
                case "ilocano" | "cebuano" | "pangasinan" | "waray":
                    gtts_target = "tl"
                case "north_azerbaijani" | "south_azerbaijani" | "turkmen" | "uyghur" | "uzbek":
                    gtts_target = "tr"
                case "sindhi" | "pashto" | "persian" | "dari" | "central_kurdish" | "tajik" | "kashmiri":
                    gtts_target = "ur"
                case "halh_mongolian" | "yue_chinese":
                    gtts_target = "zh-CN"
                case _:
                    gtts_target = "en"

        # Batch Processing
        start = time.perf_counter()
        out = ""
        batch = 2
        for i in range(0, len(split_sentences), batch):
            to_be_translated = ""
            for sentence in split_sentences[i:i+batch]: to_be_translated += " " + sentence    # Preparing sentences to be translated
            to_be_translated = to_be_translated.lstrip()
            out += translate(to_be_translated, nllb_target, NLLB_tokenizer, NLLB_model)

        print(out)
        end = time.perf_counter()
        print(f"Time: {end - start:.2f}")

    return out, gtts_target

# NLLB LANGUAGE TOKENS
nllb_token = {
        "acehnese": "ace_Latn",
        "afrikaans": "afr_Latn",
        "akan": "aka_Latn",
        "amharic": "amh_Ethi",
        "arabic": "arb_Arab",
        "armenian": "hye_Armn",
        "assamese": "asm_Beng",
        "asturian": "ast_Latn",
        "awadhi": "awa_Deva",
        "ayacucho_quechua": "quy_Latn",
        "balinese": "ban_Latn",
        "bambara": "bam_Latn",
        "banjar": "bjn_Latn",
        "bashkir": "bak_Cyrl",
        "basque": "eus_Latn",
        "belarusian": "bel_Cyrl",
        "bemba": "bem_Latn",
        "bengali": "ben_Beng",
        "bhojpuri": "bho_Deva",
        "bokmal": "nob_Latn",
        "bosnian": "bos_Latn",
        "buginese": "bug_Latn",
        "bulgarian": "bul_Cyrl",
        "burmese": "mya_Mymr",
        "catalan": "cat_Latn",
        "cebuano": "ceb_Latn",
        "central_atlas_tamazight": "tzm_Tfng",
        "central_aymara": "ayr_Latn",
        "central_kurdish": "ckb_Arab",
        "chhattisgarhi": "hne_Deva",
        "chinese_simplified": "zho_Hans",
        "chinese_traditional": "zho_Hant",
        "chokwe": "cjk_Latn",
        "crimean_tatar": "crh_Latn",
        "croatian": "hrv_Latn", 
        "czech": "ces_Latn",
        "danish": "dan_Latn",
        "dari": "prs_Arab",
        "dutch": "nld_Latn",
        "dyula": "dyu_Latn",
        "dzongkha": "dzo_Tibt",
        "eastern_punjabi": "pan_Guru",
        "egyptian": "arz_Arab",
        "english": "eng_Latn",
        "esperanto": "epo_Latn",
        "estonian": "est_Latn",
        "ewe": "ewe_Latn",
        "faroese": "fao_Latn",
        "fijian": "fij_Latn",
        "filipino": "tgl_Latn",
        "finnish": "fin_Latn",
        "fon": "fon_Latn",
        "french": "fra_Latn",
        "friulian": "fur_Latn",
        "fulfulde": "fuv_Latn",
        "galician": "glg_Latn",
        "ganda": "lug_Latn",
        "georgian": "kat_Geor",
        "german": "deu_Latn",
        "greek": "ell_Grek",
        "guarani": "grn_Latn",
        "gujarati": "guj_Gujr",
        "haitian_creole": "hat_Latn",
        "halh_mongolian": "khk_Cyrl",
        "hausa": "hau_Latn",
        "hebrew": "heb_Hebr",
        "hindi": "hin_Deva",
        "hungarian": "hun_Latn",
        "icelandic": "isl_Latn",
        "igbo": "ibo_Latn",
        "ilocano": "ilo_Latn",
        "indonesian": "ind_Latn",
        "irish": "gle_Latn",
        "italian": "ita_Latn",
        "japanese": "jpn_Jpan",
        "javanese": "jav_Latn",
        "jingpho": "kac_Latn",
        "kabiye": "kbp_Latn",
        "kabuverdianu": "kea_Latn",
        "kabyle": "kab_Latn",
        "kamba": "kam_Latn",
        "kannada": "kan_Knda",
        "kanuri": "knc_Latn",
        "kashmiri": "knc_Arab",
        "kazakh": "kaz_Cyrl",
        "khmer": "khm_Khmr",
        "kikongo": "kon_Latn",
        "kikuyu": "kik_Latn",
        "kimbundu": "kmb_Latn",
        "kinyarwanda": "kin_Latn",
        "korean": "kor_Hang",
        "kyrgyz": "kir_Cyrl",
        "lao": "lao_Laoo",
        "latgalian": "ltg_Latn",
        "latvian": "lvs_Latn",
        "ligurian": "lij_Latn",
        "limburgish": "lim_Latn",
        "lingala": "lin_Latn",
        "lithuanian": "lit_Latn",
        "lombard": "lmo_Latn",
        "luo": "luo_Latn",
        "luxembourgish": "ltg_Latn",
        "macedonian": "mkd_Cyrl",
        "magahi": "mag_Deva",
        "maithili": "mai_Deva",
        "malagasy": "plt_Latn",
        "malay": "zsm_Latn",
        "malayalam": "mal_Mlym",
        "maltese": "mlt_Latn",
        "maori": "mri_Latn",
        "marathi": "mar_Deva",
        "meitei": "mni_Beng",
        "mesopotamian": "acm_Arab",
        "minangkabau": "min_Latn",
        "mizo": "lus_Latn",
        "mongolian": "khk_Cyrl",
        "moroccan": "ary_Arab",
        "mossi": "mos_Latn",
        "najdi": "ars_Arab",
        "nepali": "npi_Deva",
        "north_azerbaijani": "azj_Latn",
        "north_levantine": "apc_Arab",
        "northern_kurdish": "kmr_Latn",
        "northern_sotho": "nso_Latn",
        "nuer": "nus_Latn",
        "nyanja": "nya_Latn",
        "nynorsk": "nno_Latn",
        "occitan": "oci_Latn",
        "odia": "ory_Orya",
        "oromo": "gaz_Latn",
        "pangasinan": "pag_Latn",
        "papiamento": "pap_Latn",
        "pashto": "pbt_Arab",
        "persian": "pes_Arab",
        "polish": "pol_Latn",
        "portuguese": "por_Latn",
        "romanian": "ron_Latn",
        "rundi": "run_Latn",
        "russian": "rus_Cyrl",
        "samoan": "smo_Latn",
        "sango": "sag_Latn",
        "sanskrit": "san_Deva",
        "santali": "sat_Beng",
        "sardinian": "srd_Latn",
        "scottish_gaelic": "gla_Latn",
        "serbian": "srp_Cyrl",
        "shan": "shn_Mymr",
        "shona": "sna_Latn",
        "sicilian": "scn_Latn",
        "silesian": "szl_Latn",
        "sindhi": "snd_Arab",
        "sinhala": "sin_Sinh",
        "slovak": "slk_Latn",
        "slovenian": "slv_Latn",
        "somali": "som_Latn",
        "south_azerbaijani": "azb_Arab",
        "south_levantine": "ajp_Arab",
        "southern_sotho": "sot_Latn",
        "southwestern_dinka": "dik_Latn",
        "spanish": "spa_Latn",
        "sundanese": "sun_Latn",
        "swahili": "swh_Latn",
        "swati": "ssw_Latn",
        "swedish": "swe_Latn",
        "ta'izzi-adeni": "acq_Arab",
        "tajik": "tgk_Cyrl",
        "tamasheq": "taq_Tfng",
        "tamil": "tam_Taml",
        "tatar": "tat_Cyrl",
        "telugu": "tel_Telu",
        "thai": "tha_Thai",
        "tibetan": "bod_Tibt",
        "tigrinya": "tir_Ethi",
        "tok_pisin": "tpi_Latn",
        "tosk_albanian": "als_Latn",
        "tsonga": "tso_Latn",
        "tswana": "tsn_Latn",
        "tumbuka": "tum_Latn",
        "tunisian": "aeb_Arab",
        "turkish": "tur_Latn",
        "turkmen": "tuk_Latn",
        "twi": "twi_Latn",
        "ukrainian": "ukr_Cyrl",
        "urdu": "urd_Arab",
        "uyghur": "uig_Arab",
        "uzbek": "uzn_Latn",
        "venetian": "vec_Latn",
        "vietnamese": "vie_Latn",
        "waray": "war_Latn",
        "welsh": "cym_Latn",
        "wolof": "wol_Latn",
        "xhosa": "xho_Latn",
        "yiddish": "ydd_Hebr",
        "yoruba": "yor_Latn",
        "yue_chinese": "yue_Hant",
        "zulu": "zul_Latn"
    }

if __name__ == "__main__":
    # Time startup
    start = time.perf_counter()

    # for sentence splitting
    nlp = spacy.load("en_core_web_sm")

    # Tagalog spacy nlp
    nlp_tgl = Tagalog()
    nlp_tgl.add_pipe('sentencizer')

    # gtts language tokens
    gtts_token = gtts_t2s.langs

    langs_list = list(nllb_token.keys())
    langs_list.append('taglish')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Taglish model
    taglish_model_name = "touno/english_to_taglish_8483_v2"
    taglish_tokenizer = AutoTokenizer.from_pretrained(taglish_model_name)
    taglish_model = AutoModelForSeq2SeqLM.from_pretrained(taglish_model_name).to(device)

    # NLLB model
    NLLB_model_name = "facebook/nllb-200-distilled-1.3B"
    NLLB_tokenizer = AutoTokenizer.from_pretrained(NLLB_model_name)
    NLLB_model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_model_name).to(device)

    print(f"Startup time: {time.perf_counter() - start:.2f}")

    while True:
        text = input("Input Text: ")
        to = input("to Language (refer to list): ").lower()
        while to not in langs_list:
            print("LANGUAGE NOT AVAILABLE")
            to = input("to Language (refer to list): ").lower()
        doVoice = input("Enable voice?: ").lower()

        out, gtts_target = translate_main(text, to, nlp, nlp_tgl, gtts_token, nllb_token, taglish_tokenizer, taglish_model, NLLB_tokenizer, NLLB_model)

        # Text-to-Speech
        if doVoice == "y" or doVoice == "yes":
            gtts_t2s.speech_text(out, "translation.mp3", gtts_target)