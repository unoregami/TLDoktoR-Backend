import re
import spacy

text = input("Input Text: ")
capitalized = []
split_sentences = []

print()
# Splits sentences based on punctuations [. ! ?]
# split_sentences = re.split(r"[.!?]", text)
# punctuations = re.findall(r"[.!?]", text)   # Extracts all [.!?] punctuations in the sentence
# print(len(split_sentences))
# print(len(punctuations))

# # Puts the punctuations back into the sentences based on index
# for i in range(len(punctuations)):
#     split_sentences[i] += punctuations[i]
# for sentence in split_sentences: print(sentence)

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
split_sentences = [sentence.text for sentence in doc.sents]

for sentence in split_sentences: print(sentence)

print()
# Extracts capitalized word (that is assumed Proper nouns) that is not at the start of the sentence.
for sentence in split_sentences:
    word_index = 0   
    latest_proper_noun_index = -1    # checker if proper noun is adjacent
    for word in sentence.split()[1:]:   # Starts at index 1 onwards
        word_index += 1

        if word[0].isupper():

            word = re.sub(r'^[^\w\'&.-]+', '', word)
            word = re.sub(r'[^\w\'&.-]+$', '', word)

            if word_index - 1 == latest_proper_noun_index:
                capitalized[-1] += f" {word}"
            else:
                capitalized.append(word)
            latest_proper_noun_index = word_index

print(capitalized)
