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

WIKI_BASE_URL = "https://en.wikipedia.org/wiki/"


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

def wiki_request(word):
    '''
    Send GET request to wiki
    '''
    word = word.replace(' ', '_')
    word = word.replace("'", "%27")

    url = _build_url(WIKI_BASE_URL,word, {})
    print url
    return url
wiki_request("Alzheimer's disease")

