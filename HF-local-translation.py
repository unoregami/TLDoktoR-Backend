from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np
from tqdm.auto import tqdm
import time
from multiprocessing import Process, Semaphore


# English to Taglish translation
def toTaglish(text):
    inputs = taglish_tokenizer(text, return_tensors="pt").to(taglish_model.device)

    generated_tokens = taglish_model.generate(
        **inputs,
        forced_bos_token_id=taglish_tokenizer.convert_tokens_to_ids("tgl_Latn"),
        max_length=360
    )
    translation = taglish_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return translation

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
def translate(text, target):
    inputs = NLLB_tokenizer(text, return_tensors="pt").to(NLLB_model.device)

    generated_tokens = NLLB_model.generate(
        **inputs,
        forced_bos_token_id=NLLB_tokenizer.convert_tokens_to_ids(target),
        max_length=360
    )
    translation = NLLB_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return translation

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


# split sentence based on punctuation
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


if __name__ == "__main__":
    # NLLB LANGUAGE TOKENS
    nllb_token = {
        "acehnese": "ace_Latn",
        "afrikaans": "afr_Latn",
        "albanian": "als_Latn",
        "amharic": "amh_Ethi",
        "arabic": "arb_Arab",
        "armenian": "hye_Armn",
        "assamese": "asm_Beng",
        "awadhi": "awa_Deva",
        "ayacucho_quechua": "quy_Latn",
        "azerbaijani_(north)": "azj_Latn",
        "azerbaijani_(south)": "azb_Arab",
        "balinese": "ban_Latn",
        "bambara": "bam_Latn",
        "bashkir": "bak_Cyrl",
        "basque": "eus_Latn",
        "belarusian": "bel_Cyrl",
        "bemba": "bem_Latn",
        "bengali": "ben_Beng",
        "bhojpuri": "bho_Deva",
        "bosnian": "bos_Latn",
        "bulgarian": "bul_Cyrl",
        "burmese": "mya_Mymr",
        "catalan": "cat_Latn",
        "cebuano": "ceb_Latn",
        "central_aymara": "ayr_Latn",
        "central_kurdish": "ckb_Arab",
        "chinese_simplified": "zho_Hans",
        "chinese_traditional": "zho_Hant",
        "crimean_tatar": "crh_Latn",
        "croatian": "hrv_Latn",
        "czech": "ces_Latn",
        "danish": "dan_Latn",
        "dari": "prs_Arab",
        "dinka_sw": "dik_Latn",
        "dutch": "nld_Latn",
        "dyula": "dyu_Latn",
        "dzongkha": "dzo_Tibt",
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
        "galician": "glg_Latn",
        "ganda": "lug_Latn",
        "georgian": "kat_Geor",
        "german": "deu_Latn",
        "greek": "ell_Grek",
        "guarani": "grn_Latn",
        "gujarati": "guj_Gujr",
        "hausa": "hau_Latn",
        "hebre": "heb_Hebr",
        "hind": "hin_Deva",
        "hungarian": "hun_Latn",
        "icelandic": "isl_Latn",
        "igbo": "ibo_Latn",
        "ilocano": "ilo_Latn",
        "indonesia": "ind_Latn",
        "irish": "gle_Latn",
        "italian": "ita_Latn",
        "japanese": "jpn_Jpan",
        "javanes": "jav_Latn",
        "jingpho": "kac_Latn",
        "kannad": "kan_Knda",
        "kanuri": "knc_Latn",
        "kazakh": "kaz_Cyrl",
        "khmer": "khm_Khmr",
        "korean": "kor_Hang",
        "kurdish_north": "kmr_Latn",
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
        "maithili": "mai_Deva",
        "malagasy": "plt_Latn",
        "malay": "zsm_Latn",
        "malayalam": "mal_Mlym",
        "maltese": "mlt_Latn",
        "marathi": "mar_Deva",
        "minangkabau": "min_Latn",
        "mizo": "lus_Latn",
        "mongolian": "khk_Cyrl",
        "nepali": "npi_Deva",
        "nuer": "nus_Latn",
        "nyanja": "nya_Latn",
        "occitan": "oci_Latn",
        "odia": "ory_Orya",
        "oromo": "gaz_Latn",
        "panganisan": "pag_Latn",
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
        "spanish": "spa_Latn",
        "sundanese": "sun_Latn",
        "swahili": "swh_Latn",
        "swati": "ssw_Latn",
        "swedish": "swe_Latn",
        "tajik": "tgk_Cyrl",
        "tamazight": "tzm_Tfng",
        "tamil": "tam_Taml",
        "tatar": "tat_Cyrl",
        "telugu": "tel_Telu",
        "thai": "tha_Thai",
        "tibetan": "bod_Tibt",
        "tigrinya": "tir_Ethi",
        "tok_pisin": "tpi_Latn",
        "tsonga": "tso_Latn",
        "tswana": "tsn_Latn",
        "tumbuka": "tum_Latn",
        "turkish": "tur_Latn",
        "turkmen": "tuk_Latn",
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
        "zulu": "zul_Latn"
    }
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Taglish model
    taglish_model_name = "touno/touno_english_to_taglish"
    taglish_tokenizer = AutoTokenizer.from_pretrained(taglish_model_name)
    taglish_model = AutoModelForSeq2SeqLM.from_pretrained(taglish_model_name).to(device)

    # NLLB model
    NLLB_model_name = "facebook/nllb-200-distilled-1.3B"
    NLLB_tokenizer = AutoTokenizer.from_pretrained(NLLB_model_name)
    NLLB_model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_model_name).to(device)

    
    text = input("Input Text: ")
    to = input("to Language (refer to list): ").lower()
    split_sentences = separate_sentences(text)

    if to == "taglish":
        # No Multiprocessing
        start = time.perf_counter()
        for sentence in split_sentences:
            print(toTaglish(sentence), end=" ")
        end = time.perf_counter()
        print(f"\nTime 1: {end - start:.2f}")

        # With Multiprocessing
        start = time.perf_counter()
        processes = []
        semaphore = Semaphore(4)
        for sentence in split_sentences:
            processes.append(Process(target=toTaglish_multiprocessing, args=(sentence, taglish_tokenizer, taglish_model, semaphore)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    
        end = time.perf_counter()
        print(f"\nTime 2: {end - start:.2f}")
    else:
        target = nllb_token.get(to)
        # No Multiprocessing
        start = time.perf_counter()
        for sentence in split_sentences:
            print(translate(sentence, target), end=" ")
        end = time.perf_counter()
        print(f"\nTime 1: {end - start:.2f}")

        # With Multiprocessing
        start = time.perf_counter()
        processes = []
        semaphore = Semaphore(4)
        for sentence in split_sentences:
            processes.append(Process(target=translate_multiprocessing, args=(sentence, target, NLLB_tokenizer, NLLB_model, semaphore)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    
        end = time.perf_counter()
        print(f"\nTime 2: {end - start:.2f}")
