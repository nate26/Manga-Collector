import json
import requests

types = ["Artbook", "Doujinshi", "Drama CD", "Filipino", "Indonesian",
         "Manga", "Manhwa", "Manhua", "Novel", "OEL", "Thai",
         "Vietnamese", "Malaysian", "Nordic", "French", "Spanish"]

genres = ["Action", "Adult", "Adventure", "Comedy", "Doujinshi", "Drama",
          "Ecchi", "Fantasy", "Gender Bender", "Harem", "Hentai",
          "Historical", "Horror", "Josei", "Lolicon", "Martial Arts",
          "Mature", "Mecha", "Mystery", "Psychological", "Romance",
          "School Life", "Sci-fi", "Seinen", "Shotacon", "Shoujo",
          "Shoujo Ai", "Shounen", "Shounen Ai", "Slice of Life", "Smut",
          "Sports", "Supernatural", "Tragedy", "Yaoi", "Yuri"]

series = {
    "search": "Kaiju No. 8",
    "stype": "title"
}
# resp = requests.post('https://api.mangaupdates.com/v1/series/search', series).json()
resp = requests.get('https://api.mangaupdates.com/v1/series/19101650311').json()
# print(json.dumps(resp))

try:
    with open('./test-details.json', 'w', encoding='UTF-8') as outfile:
        outfile.flush()
        json.dump(resp, outfile, indent=4, separators=(',', ': '))
        outfile.close()
except (FileNotFoundError, TypeError):
    print('Could not save file')
    raise