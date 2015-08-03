from bs4 import BeautifulSoup
import re
import urllib.parse
import urllib.request
import http.cookiejar
from getpass import getpass

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(
    http.cookiejar.CookieJar()))
authentication_url = 'http://cinemageddon.net/takelogin.php'
payload = {'username': input('Write your username: '),
           'password': getpass('Write your password: ')}
data = urllib.parse.urlencode(payload)
binary_data = data.encode('UTF-8')
req = urllib.request.Request(authentication_url, binary_data)
opener.open(req)
torrents_url = (
    'http://cinemageddon.net/browse.php?c1=1&c14=1&c4=1&c15=1&c18=1&c9=1&c17=1&'
    'c8=1&c6=1&c2=1&c3=1&c7=1&c20=1&c13=1&c21=1&c16=1&c12=1&noimdb=1&page=0'
)
page = 0
while input('Do you want to get page %s? (Y/n) ' % page) != 'n':
    torrent_url = torrents_url + str(page)
    html = opener.open(torrent_url).read()
    print(torrent_url)
    soup = BeautifulSoup(html, 'html5lib')
    featured = soup.find('div', id='k02122')
    featured.extract()
    ingredients = (lambda t: t.name == 'a' and
                             t['href'].startswith('details.php?id=') and
                             not t.text.isdigit())
    titles = map(lambda x: re.sub(r'\[[^\]]*\]', '', x['title']),
                 soup.findAll(ingredients))
    for t in titles:
        imdb_url = ('http://www.imdb.com/find?q=' + urllib.parse.quote(t) +
                    '&s=tt')
        imdb_soup = BeautifulSoup(
            urllib.request.urlopen(imdb_url).read(), 'html5lib')
        no_result = imdb_soup.find(lambda t: t.name == 'div' and
                                             'class' in t.attrs and
                                             'findNoResults' in t['class'])
        if not no_result:
            print(imdb_url)
    page += 1