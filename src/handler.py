import urllib
import urlparse
import urllib2

API_KEY = "0chdxJar9tkwkFEAfoyf"

BASE_URL = "http://thesaurus.altervista.org/"

PATH = "thesaurus/v1"
KEY_WORD = "word"

KEY_LANGUAGE = "language"

KEY = 'key'

KEY_OUTPUT = 'output'

OUTPUT_TYPE = 'json'

def build_url(baseurl, path, args_dict):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse.urlparse(baseurl))
    url_parts[2] = path
    url_parts[4] = urllib.urlencode(args_dict)
    return urlparse.urlunparse(url_parts)

def request(word, key, output_type = 'json', language = 'en_US'):
    args_dict = {}
    args_dict[KEY_WORD] = word
    args_dict[KEY] = key
    args_dict[KEY_OUTPUT] = output_type
    args_dict[KEY_LANGUAGE] = language
    url = build_url(BASE_URL, PATH, args_dict)

    f = urllib2.urlopen(url)
    print(f.read().decode('utf-8'))

    json_parser(f)
    return url

request("GABA", API_KEY)

def json_parser(f):
    return null
