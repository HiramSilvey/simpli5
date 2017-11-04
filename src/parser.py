import spacy

nlp = spacy.load('en')

class token:
    def __init__(self, word, pos, lemma_):
        self.word = word
        self.pos = pos
        self.lemma_ = lemma_

    def get_word(self):
        return self.word

    def get_pos(self):
        return self.pos

    def get_lemma(self):
        return self.lemma_


def parse(sentence):
    '''
    Parse sentense and identify the pos and lemma_ of each word.
    '''
    doc = nlp(sentence.decode('utf-8'))
    tokens = []
    for word in doc:
        param = [word.text, word.pos, word.lemma_]
        t = token(*param)
        tokens.append(t)
    return
