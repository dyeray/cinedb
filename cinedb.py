from bs4 import BeautifulSoup
import re
import urllib.parse
import urllib.request
import http.cookiejar
from getpass import getpass

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(
    http.cookiejar.CookieJar()))
urllib.request.install_opener(opener)
authentication_url = 'http://cinemageddon.net/takelogin.php'
payload = {'username': input('Write your username: '),
           'password': getpass('Write your password: ')}
data = urllib.parse.urlencode(payload)
binary_data = data.encode('UTF-8')
req = urllib.request.Request(authentication_url, binary_data)
urllib.request.urlopen(req)
torrents_url = (
    'http://cinemageddon.net/browse.php?c1=1&c14=1&c4=1&c15=1&c18=1&c9=1&c17=1&'
    'c8=1&c6=1&c2=1&c3=1&c7=1&c20=1&c13=1&c21=1&c16=1&c12=1&noimdb=1&page=0'
)
page = 0
while input('Do you want to get page %s? (Y/n) ' % page) != 'n':
    html = urllib.request.urlopen(torrents_url + str(page)).read()
    soup = BeautifulSoup(html, 'html5lib')
    featured = soup.find('div', id='k02122')
    featured.extract()
    ingredients = (lambda tag:tag.name == 'a' and
                          tag['href'].startswith('details.php?id=') and
                          not tag.text.isdigit())
    titles = map(lambda x: re.sub(r'\[[^\]]*\]', '', x['title']),
                 soup.findAll(ingredients))
    for t in titles:
        print('http://www.imdb.com/find?q=' + urllib.parse.quote(t) + '&s=tt')
    page += 1