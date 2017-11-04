import handler
import pickle
import spacy
import json
from stemming.porter2 import stem
import nltk
nlp = spacy.load('en')
tenK = pickle.load(open('../data/tenK.words', 'rb'))

#Map POS (spaCy form) to api
#PUNCT, PART, SYM, X, INTJ are insignificant pos
POS_MAP = {'ADJ': '(adj)', 'ADV': '(adv)', 'NOUN': '(noun)', 'VERB': '(verb)'}

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
            elif len(tokens) != 0:
                part_token = token(word.lower_, word.pos, word.lemma_)
                combine = (tokens[-1], part_token)
                del tokens[-1]
                tokens.append(combine)
                idx+=1
            else:
                idx+=1
        else:
            param = [word.text, word.pos_, word.lemma_]
            t = token(*param)
            tokens.append(t)
            idx+=1
    return tokens

def get_best_synonym(word_token):
    '''get the returned list of synonyms from a given response'''
    word = word_token.get_word()
    try:
        pos = POS_MAP[word_token.get_pos()]
        json_resp = json.loads(handler.request(word))['response']
    except:
        return word
    synonyms = []
    for w_type in json_resp:
        if w_type['list']['category'] == pos:
            synonyms.extend(w_type['list']['synonyms'].split('|'))
    most_freq = ('', 0)
    for synonym in synonyms:
        score = 0
        syn_tokens = synonym.split()
        synonym_len = len(syn_tokens)
        for syn_token in syn_tokens:
            if syn_token == word:
                synonym_len -= 1
                continue
            syn = stem(syn_token)
            if tenK.get(syn) != None:
                score += tenK[syn]
            else:
                score = 0
                break
        try:
            score = score/float(synonym_len)
        except:
            score = 0
        if score > most_freq[1]:
            most_freq = (synonym, score)
    if most_freq[1] == 0:
        return word
    return most_freq[0]

def eli5(tokens):
    words = []
    for tok in tokens:
        word = None
        if type(tok) == tuple:
            a = tok[0]
            b = tok[1]
            c = None
            if len(tok) == 3:
                c = tok[2]
                word = a.get_word()+b.get_word() + ' ' + c.get_word()
            else:
                word = a.get_word() + b.get_word()
            if not a.get_word() in tenK or (c is not None and not c.get_word() in tenK):
                word = get_best_synonym(token(word, c.get_pos(), tok.lemma_))
        else:
            word = tok.get_word()
            if not word in tenK:
                word = get_best_synonym(tok)
        words.append(word)
    return ' '.join(words)
