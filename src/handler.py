import urllib
import urlparse
import urllib2
import json

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

def get_synonyms(response):
    '''get the returned list of synonyms from a given response'''
    synonyms_str = json.loads(response)['response'][0]['list']['synonyms']
    synonyms = synonyms_str.split('|')
    return synonyms

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

print get_synonyms(request("dog"))

