import urllib
import urlparse
import urllib2
import json
import sys
sys.path.append('../data/')
import tenK.words as tenK

API_KEY = "0chdxJar9tkwkFEAfoyf"
BASE_URL = "http://thesaurus.altervista.org/"
PATH = "thesaurus/v1"
KEY_WORD = "word"
KEY_LANGUAGE = "language"
KEY = 'key'
KEY_OUTPUT = 'output'
OUTPUT_TYPE = 'json'

#Map POS (spaCy form) to api
#PUNCT, PART, SYM, X, INTJ are insignificant pos
POS_MAP = {'VERB': '(verb)', 'ADJ': '(adj)', 'ADV': '(adv)', 'NOUN': '(noun)'}

def get_best_synonym(word_token):
    '''get the returned list of synonyms from a given response'''
    try:
        pos = POS_MAP[word_token.get_pos()]
        json_resp = json.loads(request(word_token.get_word()))['response']
    except:
        return word_token.get_word()
    synonyms = []
    for w_type in json_resp if w_type['list']['category'] == pos:
        synonyms.extend(w_type['list']['synonyms'].split('|'))
    most_freq = ('', 0)
    for synonym in synonyms:
        if tenK.get(synonym) != None:
            if tenK[synonym][1] > most_freq[1]:
                most_freq = tenK[synonym]
    return most_freq[0]

def _build_url(baseurl, path, args_dict):
    '''return a list in the structure of urlparse.ParseResult

    args:
        baseurl -- the base url to use
        path -- the path off of the base url
        args_dict -- the key, value pairs of the keywords and parameters supplied
    '''
    url_parts = list(urlparse.urlparse(baseurl))
    url_parts[2] = path
    url_parts[4] = urllib.urlencode(args_dict)
    return urlparse.urlunparse(url_parts)

def request(word, key=API_KEY, output_type = 'json', language = 'en_US'):
    '''send a request to the thesaurus API

    args:
        word -- the word to lookup in the thesaurus
        key -- the API key
        output_type -- the format of the response data
        language -- the language used
    '''
    args_dict = {}
    args_dict[KEY_WORD] = word
    args_dict[KEY] = key
    args_dict[KEY_OUTPUT] = output_type
    args_dict[KEY_LANGUAGE] = language
    url = _build_url(BASE_URL, PATH, args_dict)

    response = urllib2.urlopen(url).next()
    return response

