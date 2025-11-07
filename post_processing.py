import re
import spacy


# AS SPLIT SENTENCES. Extracts capitalized word that is not at the start of the sentence. RETURNS LIST
def extract_cap_split(split_sentences):
    capitalized = []
    
    for sentence in split_sentences:
        word_index = 0   
        for word in sentence.split()[1:]:   # Starts at index 1 onwards
            word_index += 1
            word = re.sub(r'[\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]', '', word)
            if word == "":
                break

            if word[0].isupper():
                word = re.sub(r'^[^\w\'&.-]+', '', word)
                word = re.sub(r'[^\w\'&.-]+$', '', word)

                capitalized.append(word)

    return capitalized

# AS A STRING. Extracts capitalized word that is not at the start of the sentence. RETURNS DICTIONARY
def extract_cap_text(text):
    capitalized = {}
    isFirst = True

    for word in text.split():
        if isFirst:
            isFirst = False
            continue
        word = re.sub(r'^[^\w]+', '', word)     # removes punctuaions at start
        word = re.sub(r'[^\w]+$', '', word)     # removes punctuations at end
        if word == "":
            continue

        if word[0].isupper():
            if word in capitalized:
                capitalized[word] += 1
            else:
                capitalized[word] = 1

    return capitalized

# Post-processing
def post_process(text:str, capitalized_dictionary:dict, nlp):
    text = re.sub(r' \.', '.', text)        # periods
    text = re.sub(r' \!', '!', text)        # exclamation
    text = re.sub(r' \?', '?', text)        # question
    text = re.sub(r' \(', '(', text)        # left parenthesis
    text = re.sub(r' \)', ')', text)        # right parenthesis
    text = re.sub(r'\s*,\s*', ', ', text)   # commas

    doc = nlp(text)
    out = ""

    # Uppercase first word's letter
    for sent in doc.sents:
        ph = sent.text.lstrip()
        out += " " + ph[0].upper() + ph[1:]
    out = out.lstrip()

    capitalized_words = list(capitalized_dictionary.keys())
    for word in capitalized_words:
        word_lower = word.lower()
        count = capitalized_dictionary[word]
        out = re.sub(word_lower, word, out, count=count)

    return out

if __name__ == "__main__":
    text = input("Input Text: ")
    split_sentences = []
    print()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    split_sentences = [sentence.text for sentence in doc.sents]
    batch = 2

    test_capitalized_dictionary = {}
    for i in range(0, len(split_sentences), batch):
        to_be_translated = ""
        capitalized_dictionary = {}

        # Preparing sentences to be translated
        for sentence in split_sentences[i:i+batch]: 
            to_be_translated += " " + sentence      # concat to be translated sentences

            ph = extract_cap_text(sentence)         # extract capitalized per sentence
            capitalized_dictionary = capitalized_dictionary | ph    # store to main dictionary
            
        to_be_translated = to_be_translated.lstrip()

        print("TO BE TRANSLATED")
        print(to_be_translated.lower())
        print()
        print("EXTRACTED CAPITAL WORDS")
        print(capitalized_dictionary)
        print()

        test_capitalized_dictionary = test_capitalized_dictionary | capitalized_dictionary


    text_sample = """
    Nang sumigaw si emily, wait! - nag-freeze ang lahat. may hawak siyang kakaibang sobre na may nakasulat na "top secret #42". Sa loob nito ay may note na ganito: "Meet me @ 7:00 p.m.; bring $100,000 (cash only)!" confused, mumble Dr. Miles, "Is this some kind of joke?" - pero ang mga coordinates na <40.7128N, 74.0060W> ay mukhang totoo. Bigla na lang bumibita ang kanyang telepono: Error 404 - Access Denied . nag-type siya ng sudo unlock_all at pinindot ang enter tapos on-screen ay lumitaw ang mga symbols: [isang kakaibang bagay]. "Oh hindi"... sabay sabi niya, "nagbabalik na naman". At sa malayo ay may bumangga na munting beep - click! - pagkatapos ay tahimik...
    """
    print("LOWER TEST TEXT SAMPLE")
    print(text_sample)
    print()

    print("EXTRACTED CAPITALIZED WORDS")
    print(test_capitalized_dictionary)
    print()

    text_sample = post_process(text_sample, test_capitalized_dictionary, nlp)

    print("POST-PROCESSED")
    print(text_sample)

    # ---------------------------------------------------------------

    # capitalized = extract_cap_split(split_sentences)
    # print("As split sentences")
    # print(capitalized)


    # # test to original text
    # text = text.lower()
    # print("Lowercased sample text:")
    # print(text)

    # for word in capitalized:
    #     ph = word.lower()
    #     text = re.sub(ph, word, text)

    # text = 

    # print("Truecased text:")
    # print(text)