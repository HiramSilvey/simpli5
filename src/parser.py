import worker
import pickle
import spacy
import json
from stemming.porter2 import stem
import nltk
nlp = spacy.load('en')
tenK = pickle.load(open('../data/tenK.words', 'rb'))

#Map POS (spaCy form) to api
#PUNCT, PART, SYM, X, INTJ are insignificant pos
POS_MAP = {'ADJ': '(adj)', 'PROPN': '(noun)',  'ADV': '(adv)', 'NOUN': '(noun)', 'VERB': '(verb)'}

class token:
    def __init__(self, word, pos, lemma_, tag_):
        self.word = word
        self.pos = pos
        self.lemma_ = lemma_
        self.tag_ = tag_

    def get_word(self):
        return self.word

    def get_pos(self):
        return self.pos

    def get_lemma(self):
        return self.lemma_

    def get_tag(self):
        return self.tag_

def tokenize(sentence):
    '''
    Parse sentense and identify the pos and lemma_ of each word.
    Return a tuple (e.g. Alzheimer's disease) when there's a PART pos.
    '''
    doc = nlp(sentence.decode('utf-8'))
    tokens = []
    for word in doc:
        curr_token = token(word, word.pos_, word.lemma_, word.tag_)
        if word.pos_ == 'NOUN' or word.pos_ == 'PROPN' or word.pos_ == 'PART' or (word.pos_ == 'ADJ' and not word.tag_ == 'PRP$'):
            if len(tokens) == 0 or not _isNounGroup(tokens[-1]):
                tokens.append(curr_token)
            else:
                tokens[-1] =  tokens[-1] + (curr_token,) if type(tokens[-1]) == tuple else (tokens[-1], curr_token)
        else:
            tokens.append(curr_token)
    return tokens

def _isNounGroup(token):
    '''
    NounGroup includes PART, NOUN, PROPN, ADJ
    '''
    if type(token) == tuple:
        token = token[-1]
    pos = token.get_pos()
    return pos == 'PART' or pos == 'NOUN' or pos == 'PROPN' or (pos == 'ADJ' and not token.get_tag() == 'PRP$')

def get_best_synonym(word_token):
    '''get the returned list of synonyms from a given response'''
    word = word_token.get_word()
    try:
        pos = POS_MAP[word_token.get_pos()]
        json_resp = json.loads(worker.request(word))['response']
    except:
        return word
    synonyms = []
    for w_type in json_resp:
        if w_type['list']['category'] == pos:
            synonyms.extend(w_type['list']['synonyms'].split('|'))
    most_freq = ('', 0)
    print synonyms
    for synonym in synonyms:
        score = 0
        syn_tokens = synonym.split()
        synonym_len = len(syn_tokens)
        for syn_token in syn_tokens:
            syn_token = syn_token.lower()
            if syn_token == word.lower():
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

def smmrize(paragraph):
    f = worker.smmry_request(paragraph)
    s =  f.read()
    j = json.loads(s)
    try:
        return j["sm_api_content"]
    except:
        return paragraph

def simpli5(paragraph):
    tokens = tokenize(paragraph)
    words = []
    for tok in tokens:
        word = ""
        if type(tok) == tuple:
            simple = True
            for t in tok:
                if t.get_pos() == 'PART':
                    word = word.rstrip(' ')
                word += t.get_word()
                word += ' '
                if not t.get_word() in tenK:
                    simple = False
            word = word.rstrip(' ')
            if tok[-1].get_pos() == 'PART':
                curr_token = token(word, tok[-2].get_pos(), word, tok[-2].get_tag())
            else:
                curr_token = token(word, tok[-1].get_pos(), word, tok[-1].get_tag())
            if not simple:
                word = get_best_synonym(curr_token)
        else:
            word = tok.get_word()
            if not word in tenK:
                word = get_best_synonym(tok)
        words.append(word)
    result =' '.join(words)
    return result.replace(' .', '.').replace(' ,', ',')
