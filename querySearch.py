from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json
import re
import os
import sysRequest

client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'song-index1'

# ---------------------------------------------------------------------------------------
# At the first time you run the system, uncomment following section.


def createIndex():
    settings = {
        "settings": {
            "index": {
                "number_of_shards": "1",
                "number_of_replicas": "1"
            },
            "analysis": {
                "analyzer": {
                    "sinhala-analyzer": {
                        "type": "custom",
                        "tokenizer": "icu_tokenizer",
                        "filter": ["edge_ngram_custom_filter"]
                    }
                },
                "filter": {
                    "edge_ngram_custom_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 50,
                        "side": "front"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                    "analyzer": "sinhala-analyzer",
                    "search_analyzer": "standard"
                },
                "lyrics": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                    "analyzer": "sinhala-analyzer",
                    "search_analyzer": "standard"
                },
                "artist": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                    "analyzer": "sinhala-analyzer",
                    "search_analyzer": "standard"
                },
                "music": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                    "analyzer": "sinhala-analyzer",
                    "search_analyzer": "standard"
                },
                "genre": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                    "analyzer": "sinhala-analyzer",
                    "search_analyzer": "standard"
                },
                "english_artist": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                },
                "english_lyricist": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                },
                "english_music": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                },
                "guitar_key": {
                    "type": "text",
                    "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                    },
                },
                "views": {
                    "type": "long",
                }
            }
        }
    }
    result = client.indices.create(index=INDEX, body=settings)
    print(result)

def readAllSongs():
    selfPath = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(selfPath, 'ProcessedData')
    file2 = os.path.join(file1, 'corpus')
    filef = os.path.join(file2, 'songs.json')
    with open(filef, 'r') as f:
        allSongs = json.loads(f.read())
        responseList = [i for n, i in enumerate(
            allSongs) if i not in allSongs[n + 1:]]
        return responseList


def cleanLyrics(lyrics):
    if lyrics:
        cleanedLyricsList = []
        lines = lyrics.split('\n')
        for index, line in enumerate(lines):
            lineStripped = re.sub('\s+', ' ', line)
            linePuncStripped = re.sub('[.!?\\-]', '', lineStripped)
            cleanedLyricsList.append(linePuncStripped)
        last = len(cleanedLyricsList)
        final_list = []
        for index, line in enumerate(cleanedLyricsList):
            if line == '' or line == ' ':
                if index != last-1 and (cleanedLyricsList[index+1] == ' ' or cleanedLyricsList[index+1] == ''):
                    pass
                else:
                    final_list.append(line)
            else:
                final_list.append(line)
        cleanedLyrics = '\n'.join(final_list)
        return cleanedLyrics
    else:
        return None


def genData(song_array):
    for song in song_array:
        guitarKey = song.get("guitar_key", None)  # English
        englishLyricist = song.get("english_lyricst", None)
        englishMusic = song.get("english_music", None)
        englishArtist = song.get("english_artist", None)
        title = song.get("title", None)  # Bilingual
        artist = song.get("Artist", None)  # Sinhala
        genre = song.get("Genre", None)
        lyricist = song.get("Lyrics", None)
        music = song.get("Music", None)
        lyrics = cleanLyrics(song.get("song_lyrics", None))
        views = song.get('views', None)  # Numbers
        yield {
            "_index": "song-index1",
            "_source": {
                "guitar_key": guitarKey,
                "title": title,
                "artist": artist,
                "genre": genre,
                "lyrics": lyricist,
                "music": music,
                "english_lyricist": englishLyricist,
                "english_music": englishMusic,
                "english_artist": englishArtist,
                "views": views,
                "song_lyrics": lyrics
            },
        }


# createIndex()
# allSongs = readAllSongs()
# helpers.bulk(client, genData(allSongs))

# -------------------------------------------------------------------------------------------


def getAllGenre():
    selfPath = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(selfPath, 'ProcessedData')
    file2 = os.path.join(file1, 'corpus')
    filef = os.path.join(file2, 'genres.json')
    with open(filef, 'r') as t:
        allGenres = json.loads(t.read())
        return allGenres.keys(), allGenres.values()


def getAllArtists():
    selfPath = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(selfPath, 'ProcessedData')
    file2 = os.path.join(file1, 'corpus')
    filef = os.path.join(file2, 'artists.json')
    with open(filef, 'r') as t:
        allArtists = json.loads(t.read())
        return allArtists.keys(), allArtists.values()


def getAllLyrics():
    selfPath = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(selfPath, 'ProcessedData')
    file2 = os.path.join(file1, 'corpus')
    filef = os.path.join(file2, 'lyricists.json')
    with open(filef, 'r') as t:
        allLyricists = json.loads(t.read())
        return allLyricists.keys(), allLyricists.values()


def getAllMusic():
    selfPath = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(selfPath, 'ProcessedData')
    file2 = os.path.join(file1, 'corpus')
    filef = os.path.join(file2, 'musics.json')
    with open(filef, 'r') as t:
        allMusic = json.loads(t.read())
        return allMusic.keys(), allMusic.values()


englishGenres, sinhalaGenres = getAllGenre()
englishArtists, sinhalaArtists = getAllArtists()
englishLyrics, sinhalaLyrics = getAllLyrics()
englishMusic, sinhalaMusic = getAllMusic()

synonymLyrics = ['ලියන්නා', 'ලියන', 'රචිත', 'ලියපු',
                 'ලියව්‌ව', 'රචනා', 'රචක', 'ලියන්', 'ගත්කරු', 'රචකයා']
synonymEngLyrics = ['wrote', 'songwriter', 'lyricist', 'write']
synonymArtist = ['ගායනා', 'ගැයු', 'ගයන', 'ගායකයා', 'ගයනවා']
synonymEngArtist = ['sing', 'artist', 'singer', 'sung']
synonymMusic = ['සංගීත']
synonymEngMusic = ['composer', 'music', 'composed']
synonymPopularity = ['හොඳම', 'ජනප්‍රිය',
                     'ප්‍රචලිත', 'ප්‍රසිද්ධ', 'හොදම', 'ජනප්‍රියම']
synonymKey = ['Minor', 'Major', 'minor', 'major']
synonymGenre = ['පොප්', 'දේවානුභාවයෙන්', 'රන්', 'පැරණි', 'රන්වන්', 'පොප්', 'කණ්ඩායම්',
                'යුගල', 'අලුත්', 'නව', 'පැරණි', 'පොප්ස්', 'කැලිප්සෝ', 'සම්භාව්ය', 'වත්මන්', 'චිත්‍රපට']

allLists = [None, None, sinhalaGenres, englishArtists, sinhalaArtists,
            englishLyrics, sinhalaLyrics, englishMusic, sinhalaMusic]

synonymList = [None, None, synonymGenre, synonymEngArtist, synonymArtist,
               synonymEngLyrics, synonymLyrics, synonymEngMusic, synonymMusic]

# ----------------------------------------------------------------------------------------------------


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def boost(boost_array):  # views is not taken for search
    term1 = "title^{}".format(boost_array[1])
    term2 = "genre^{}".format(boost_array[2])
    term3 = "english_artist^{}".format(boost_array[3])
    term4 = "artist^{}".format(boost_array[4])
    term5 = "english_lyricist^{}".format(boost_array[5])
    term6 = "lyrics^{}".format(boost_array[6])
    term7 = "english_music^{}".format(boost_array[7])
    term8 = "music^{}".format(boost_array[8])
    term9 = "song_lyrics^{}".format(boost_array[9])
    term10 = "guitar_key^{}".format(boost_array[10])
    return [term1, term2, term3, term4, term5, term6, term7, term8, term9, term10]


def search(phrase):
    # flag order, 0 - number, 1 - title, 2 - sin_gen, 3 - eng_art, 4 - sin_art, 5 - eng_lyr, 6 - sin_lyr, 7 - eng_mus, 8 - sin_mus, 9 - song_lyrics, 10 - guitar_key
    flags = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    num = 0
    if isEnglish(phrase):  # If term is in english,boost guitar key
        flags[3] = 2
        flags[5] = 2
        flags[7] = 2
        flags[10] = 3
        print('Boosting for english language')
    else:
        flags[2] = 3
        flags[4] = 3
        flags[6] = 3
        flags[8] = 3
        flags[9] = 3
        print('Boosting for sinhala language')
    tokens = phrase.split()

    for word in tokens:  # Identify numbers
        print(word)
        if word.isdigit():
            flags[0] = 1
            num = int(word)
            print('Identified sort number', num)
        for i in range(2, 9):  # Check whether a value from any list is present
            if word in allLists[i]:
                print('Boosting field', i, 'for', word, 'in all list')
                flags[i] = 5
        for i in range(2, 9):  # Check whether token matches any synonyms
            if word in synonymList[i]:
                print('Boosting field', i, 'for', word, 'in synonym list')
                flags[i] = 5
        if word in synonymKey:
            print('Boosting guitar key')
            flags[10] = 5
        if word in synonymPopularity:
            print('Start sort by views')
            if flags[0] == 0:
                flags[0] = 1
                num = 500

    for i in range(2, 9):  # Check whether full phrase is in any list
        if phrase in allLists[i]:
            print('Boosting field', i, 'for', phrase, 'in all list')
            flags[i] = 5
    if len(tokens) > 5:  # If there are more than 5 words,boost lyrics
        print('Boosting song lyrics for tokens > 5')
        flags[9] = 5
    fields = boost(flags)
    print(fields)
    if flags[0] == 0:  # If the query contain a number call sort query
        reqBody = sysRequest.aggMultiMatchQuery(phrase, fields)
        print('Making Faceted Query')
    else:
        reqBody = sysRequest.aggMultiMatchAndSortQuery(phrase, num, fields)
        print('Making Range Query')
    res = client.search(index=INDEX, body=reqBody)
    return res
