import re

text = input("Input Text: ")
capitalized = []
split_sentences = []

print()
# Splits sentences based on punctuations [. ! ?]
# for i in text.split("."):
#     split_sentences.append(i + ".")
split_sentences = re.split(r"[.!?]", text)
punctuations = re.findall(r"[.!?]", text)   # Extracts all [.!?] punctuations in the sentence
print(len(split_sentences))
print(len(punctuations))

# Puts the punctuations back into the sentences based on index
for i in range(len(punctuations)):
    split_sentences[i] += punctuations[i]
print(split_sentences)

# Extracts capitalized word (that is assumed Proper nouns) that is not at the start of the sentence.
for sentence in split_sentences:
    for word in sentence.split()[1:]:   # Starts at index 1 onwards
        if word[0].isupper():
            capitalized.append(word)

print(capitalized)
