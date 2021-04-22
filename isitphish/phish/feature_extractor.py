import re
from urllib.parse import urlparse, urlsplit
import tldextract 

HINTS = ['site', 'content', 'admin', 'includes', 'include', 'login', 'wp', 'css', 'images', 'alibaba', 'js',
         'themes', 'view', 'myaccount', 'dropbox', 'signin', 'plugins']

## Function to get domain
def get_domain(url):
    output = urlparse(url)
    return output.hostname, tldextract.extract(url).domain, output.path, tldextract.extract(url).suffix

## Function to extract raw words
def raw_words_extractor(domain, subdomain, path):
    words_domain = re.split("\.|\?|\=|\@|\&|\%|\:|\_|\-|\/", domain.lower())
    words_subdomain = re.split("\.|\?|\=|\@|\&|\%|\:|\_|\-|\/", subdomain.lower())
    words_path = re.split("\.|\?|\=|\@|\&|\%|\:|\_|\-|\/", path.lower())
    raw_words = words_domain + words_path + words_subdomain
    words_host = words_domain + words_subdomain
    raw_words = list(filter(None, raw_words))
    return raw_words, list(filter(None, words_host)), list(filter(None, words_path))

def get_subdomain(url):
    return tldextract.extract(url).subdomain

def count_www(raw_words):
    count = 0
    for word in raw_words:
        if not word.find('www') == -1:
            count +=1
    return count

def feature_extractor(url):
    hostname, domain_name, path, tld = get_domain(url)
    subdomain = get_subdomain(url)
    raw_words, raw_words_host, raw_words_path = raw_words_extractor(domain_name, subdomain, path) 

    features = []
    features.append(len(url))
    features.append(len(hostname))
    features.append(1) if re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
                                    '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'
                                    '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'
                                    '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
                                    '[0-9a-fA-F]{7}', url) else features.append(0)
    features.append(url.count('.'))
    features.append(url.count('?'))
    features.append(url.count('='))
    features.append(url.count('/'))
    features.append(count_www(raw_words))
    features.append(len(re.sub("[^[0-9]", "", url)) / len(url))
    features.append(len(re.sub("[^[0-9]", "", hostname)) / len(hostname)) #ratio digits hostname
    features.append(1) if subdomain.count(tld) else features.append(0) #tld_in_subdomain
    features.append(1) if re.findall(r"https?://[^\-]+-[^\-]+/", url) else features.append(0) #prefix_suffix
    features.append(len(raw_words)) #len of raw words
    features.append(0 if len(raw_words_host) == 0 else min(len(word) for word in raw_words_host)) #shortest raw word host
    features.append(0 if len(raw_words) == 0 else max(len(word) for word in raw_words)) #longest raw word
    features.append(0 if len(raw_words_path) == 0 else max(len(word) for word in raw_words_path)) #longest raw word path
    features.append(0 if len(raw_words_host) == 0 else sum(len(word) for word in raw_words_host) / len(raw_words_host)) #average
    features.append(0 if len(raw_words_path) == 0 else sum(len(word) for word in raw_words_path) / len(raw_words_path)) #average
    features.append(sum(path.lower().count(hint) for hint in HINTS)) #phish hints
    return features