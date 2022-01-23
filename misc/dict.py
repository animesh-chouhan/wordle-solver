from nltk.corpus import words

words5 = []

for word in words.words():
    if len(word) == 5:
        words5.append(word)

print(words5)
