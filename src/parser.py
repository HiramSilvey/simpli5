import pickle
import spacy
from stemming.porter2 import stem
import nltk
nlp = spacy.load('en')

#Map POS (spaCy form) to api
#PUNCT, PART, SYM, X, INTJ are insignificant pos
POS_MAP = {'PUNCT': -1, 'PART': -1, 'SYM': -1, 'X': -1, 'INTJ': -1, 'ADJ': '(adj)', 'ADV': '(adv)', 'NOUN': '(noun)'}

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


def tokenize(sentence):
    '''
    Parse sentense and identify the pos and lemma_ of each word.
    Return a tuple (e.g. Alzheimer's disease) when there's a PART pos.
    '''
    doc = nlp(sentence.decode('utf-8'))
    tokens = []
    idx = 0
    while idx < len(doc):
        word = doc[idx]
        if word.pos_ == 'PART':
            if len(tokens) != 0 and idx + 1 < len(doc) and doc[idx+1].pos_ == 'NOUN':
                part_token = token(word.lower_, word.pos, word.lemma_)
                noun_token = token(doc[idx+1].lower_, doc[idx+1].pos, doc[idx+1].lemma_)
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

def get_best_synonym(word_token):
    '''get the returned list of synonyms from a given response'''
    try:
        pos = POS_MAP[word_token.get_pos()]
        json_resp = json.loads(request(word_token.get_word()))['response']
    except:
        return word_token.get_word()
    synonyms = []
    for w_type in json_resp:
        if w_type['list']['category'] == pos:
            synonyms.extend(w_type['list']['synonyms'].split('|'))
    most_freq = ('', 0)
    tenK = pickle.load(open('../data/tenK.words', 'rb'))
    print(synonyms)
    for synonym in synonyms:
        score = 0
        for syn_token in synonym.split():
            syn = stem(syn_token)
            if tenK.get(syn) != None:
                score += tenK[syn]
            else:
                score = 0
                break
        score = score/float(len(synonym))
        if score > most_freq[1]:
            most_freq = (synonym, score)
    return most_freq[0]

def eli5(tokens):
    words = []
    for tok in tokens:
        word = None
        if type(tok) == tuple:
            a = tok[0]
            b = tok[1]
            c = tok[2]
            word = ' '.join(a.get_word()+b.get_word(), c.get_word())
            if not a.get_word() in tenK or not c.get_word() in tenK:
                word = get_best_synonym(token(word, c.get_pos(), word.lemma_))
        else:
            word = tok.get_word()
            if not word in tenK:
                word = get_best_synonym(tok)
        words.append(word)
    return ' '.join(words)
tokenize("My grandmother developed Alzheimer's disease.")
