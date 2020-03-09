from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import scraper
import nltk
from nltk.corpus import stopwords
from urllib.parse import urlparse
from urllib.parse import urljoin



def normalize_url(url):
    if url.__contains__('#'):
        url = url[:url.index('#')]

    if url.__contains__('?reply'):
        url = url[:url.index('?reply')]

    if url.__contains__('?event'):
        url = url[:url.index('?event')]

    if url.__contains__('archive.ics.uci.edu/'):
        url = url[:url.index('archive.ics.uci.edu/')]

    if re.match(r".*/$", url):
        url = url[:-1]

    return url


# Code Source https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
def html_to_text(document):
    soup = BeautifulSoup(document, 'html.parser', )
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style'
    ]

    # count = 0
    for t in text:
        if t.parent.name not in blacklist and not isinstance(t, Comment):
            # if count<1:

            # if t[0] == '<':
            #     print(t.parent.name, '||', t)

            # if isinstance(t, Comment):
            #     print(t.parent.name, '||', t)

            # print(t)
            # print(t.parent.name, '||', t)

            # if t.parent.name != 'style':
            #     print(t.parent.name,'||',t)

            output += '{} '.format(t)

    return output


def get_link(document, base):
    all_links = []
    soup = BeautifulSoup(document, 'html.parser')
    for link in soup.find_all('a'):
        curr_link = link.get('href')
        curr_link = urljoin(base, curr_link)
        if scraper.is_valid(curr_link) and curr_link is not None:
            curr_link = normalize_url(curr_link)
            all_links.append(curr_link)

    return all_links


def get_subdomain(url):
    my_domain = urlparse(url)
    subdomain = '{uri.scheme}://{uri.netloc}/'.format(uri=my_domain)
    subdomain = subdomain[subdomain.index('//') + 2:]
    subdomain = normalize_url(subdomain)
    return subdomain
