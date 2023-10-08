import spacy
import csv
import string
sjp = spacy.load("pl_core_news_sm")


def search_sentence(sentence, level_of_details):
    if level_of_details == 1:
         sentence = remove_prepositions(sentence)
    sentence = str(sentence).lower()
    sentence = ''.join([char for char in sentence if char not in string.punctuation]) # remove punctuation characters
    splitted_sentence = []
    for word in sjp(sentence):
        # print(f"Token: {word.text}, Lemma: {word.lemma_}, POS: {word.pos_}")
        splitted_sentence.append(word.lemma_)

    with open('SearchSentence/examples.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None) # skip headers
        results = []
        for row in csv_reader:
            value = str(row).lower()
            try:
                for word in sjp(value):
                    if word.lemma_ in splitted_sentence:
                        # print(f"Token: {word.text}, Lemma: {word.lemma_}, POS: {word.pos_}")
                        results.append(row[0])
                        break # not duplicate rows
            except Exception as error:
                print(error)

    for i in results:
        print(i)

def remove_prepositions(sentence):
    pronouns = [
    "w", "na", "pod", "nad", "przed", "za", "między", "obok", "przy", "między",
    "bez", "po", "do", "przez", "z", "o", "u", "ku", "dzięki", "wobec", "ponad",
    "wśród", "względem", "naprzeciw", "za pomocą", "ku", "wzdłuż", "blisko",
    "dokoła", "wbrew", "zgodnie z", "według", "to"]
    filtered_sentence = ' '.join(word for word in sentence.split() if word not in pronouns)
    return filtered_sentence


if __name__ == "__main__":
    print('Check sentence with prepositions:')
    search_sentence("Jakieś zdanie po polsku.", 0)
    print('Check sentence without prepositions:')
    search_sentence("Jakieś zdanie po polsku.", 1)