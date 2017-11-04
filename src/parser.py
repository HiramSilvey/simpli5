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
    Return a tuple (e.g. Alzheimer's disease) when there's a PART pos.
    '''
    doc = nlp(sentence.decode('utf-8'))
    tokens = []
    idx = 0
    while idx < len(doc):
        word = doc[idx]
        print word.pos_
        if word.pos_ == 'PART':
            if len(tokens) != 0 and idx + 1 < len(doc) and doc[idx+1].pos_ == 'NOUN':
                part_token = token(word, word.pos, word.lemma_)
                noun_token = token(doc[idx+1], doc[idx+1].pos, doc[idx+1].lemma_)
                combine = (tokens[-1], part_token, noun_token)
                del tokens[-1]
                tokens.append(combine)
                idx+=2
        else:
            param = [word.text, word.pos_, word.lemma_]
            t = token(*param)
            tokens.append(t)
            idx+=1
    return tokens

'''
parse("My grandmother developed Alzheimer's disease.")
'''
