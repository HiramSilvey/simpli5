import urllib
import urlparse
import urllib2
import json
from IPython import embed

API_KEY = "0chdxJar9tkwkFEAfoyf"
SM_KEY = "2B269D5CE2"
BASE_URL = "http://thesaurus.altervista.org/"
PATH = "thesaurus/v1"
KEY_WORD = "word"
KEY_LANGUAGE = "language"
KEY = 'key'
KEY_OUTPUT = 'output'
OUTPUT_TYPE = 'json'

WIKI_BASE_URL = "https://en.wikipedia.org/"
PATH = "w/api.php"
wiki_args_dict = {"action": "opensearch", "limit": 1, "format": "json"}
SM_BASE_URL = "http://api.smmry.com/"
SM_API_INPUT_KEY = "sm_api_input"

sm_args_dict = {"SM_API_KEY": SM_KEY }

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
    Send GET request to wiki API which auto complete a search term (e.g. Alzheimer's to Alzheimer's disease)

    args:
        word -- the word (can be incomplete) that is searched
    '''
    word = word.replace(' ', '_')
    wiki_args_dict["search"] = word
    url = _build_url(WIKI_BASE_URL,PATH, wiki_args_dict)
    try:
        f = urllib2.urlopen(url)
        j = json.loads(f.read())
        link_url = j[-1][0].encode('utf-8')
        print link_url
        return link_url
    except urllib2.HTTPError, e:
        print(e.code)
    except urllib2.URLError, e:
        print(e.args)

def smmary_request(paragraph):
    sm_args_dict[SM_API_INPUT_KEY] = paragraph
    url = _build_url(SM_BASE_URL,"", sm_args_dict)
    print url
    try:
        f = urllib2.urlopen(url)
        embed()
    except urllib2.HTTPError, e:
        print(e.code)
    except urllib2.URLError, e:
        print(e.args)


s = "This is a sentence. hahahaha."
smmary_request(s)
