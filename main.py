import requests

url = 'https://radio1.hu/stream/stream.php'
r = requests.get(url)
r.encoding = r.apparent_encoding
resp = r.json()

player = r.json()['player']
tstamp = player[0]['idopont']
artists = [x['artist'] for x in player]
titles = [x['title'] for x in player]
print(artists)
print(titles)
print(tstamp)