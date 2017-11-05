import worker
import pickle
import spacy
import json
from stemming.porter2 import stem
import nltk
import os
nlp = spacy.load('en')
tenK = pickle.load(open(os.path.dirname(__file__) + '/data/tenK.words', 'rb'))

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

    def set_word(self, word):
        self.word = word

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_lemma(self):
        return self.lemma_

    def get_tag(self):
        return self.tag_

def tokenize(sentence):
    '''
    Parse sentense and identify the pos and lemma_ of each word.
    Return a tuple (e.g. Alzheimer's disease) when there's a PART pos.
    '''
    doc = nlp(unicode(sentence))
    tokens = []
    for word in doc:
        curr_token = token(word.orth_, word.pos_, word.lemma_, word.tag_)
        if (word.pos_ == 'PART' or (word.tag_ == 'RB' and "'" in word.orth_) or (word.pos_ == 'VERB' and "'" in word.orth_)) and len(tokens) != 0:
            tokens[-1].set_word(tokens[-1].get_word() + word.orth_)
            continue
        elif (word.pos_ == 'NOUN' or word.pos_ == 'PROPN') and (len(tokens) != 0 and _isNounGroup(tokens[-1])):
            tokens[-1].set_word(tokens[-1].get_word() + ' ' + word.orth_)
            tokens[-1].set_pos(word.pos_)
            continue
        elif (word.pos_ == 'ADJ' and not word.tag_ == 'PRP$') and (len(tokens) != 0 and (tokens[-1].get_pos() == 'NOUN' or tokens[-1].get_pos() == 'PROPN')):
            tokens[-1].set_word(tokens[-1].get_word() + ' ' + word.orth_)
            continue
        tokens.append(curr_token)
    #for tok in tokens:
    #    print tok.get_word() + ' ' + tok.get_pos()
    return tokens

def _isNounGroup(token):
    '''
    NounGroup includes NOUN, PROPN, ADJ
    '''
    if type(token) == tuple:
        token = token[-1]
    pos = token.get_pos()
    return pos == 'NOUN' or pos == 'PROPN' or (pos == 'ADJ' and not token.get_tag() == 'PRP$')

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

SPECIAL = set(['PART', 'SYM', 'PUNCT', 'SPACE'])
def simpli5(paragraph):
    tokens = tokenize(paragraph)
    result = ''
    for i, tok in enumerate(tokens):
        text = tok.get_word()
        pos = tok.get_pos()
        words = text.split(' ')
        common = True
        for word in words:
            if not stem(word).lower() in tenK and (pos != 'VERB' or "'" not in word):
                common = False
                break
        if not common and pos not in SPECIAL:
            synonym = get_best_synonym(tok)
            wiki_link = worker.wiki_request(text)
            if wiki_link != None:
                text = '[' + text + '](' + wiki_link + ')'
            if synonym != text:
                text = synonym + ' (' + text + ')'
        if i != 0 and pos not in SPECIAL:
            result += ' '
        result += text
    return result
