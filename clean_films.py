import re
import sys

try:
    films = open(sys.argv[1]).read().splitlines()
except (IOError, IndexError):
    print("You must call this script passing the path to the file that contains"
          " Cinemageddon and IMDB links")
    exit()

cinemageddon_r = r'http://cinemageddon.net/details.php\?id=(.*)'
imdb_r = r'http://www.imdb.com/title/(tt[0-9]+)/\?ref_=.*'

cleaned_films = [re.sub(cinemageddon_r, r'[torrent=\1]', re.sub(
    imdb_r, r'\1', x)) for x in films]

for f in cleaned_films:
    print(f)