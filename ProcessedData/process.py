import json
import time
import mtranslate


def translateTag(valueArray, globalValDict):
    if valueArray:
        translatedValueArray = []
        if type(valueArray) == list:
            for englishVal in valueArray:
                englishVal = englishVal.strip()
                if englishVal in globalValDict:
                    sinhalaGen = globalValDict[englishVal]
                else:
                    sinhalaGen = mtranslate.translate(englishVal, 'si', 'en')
                    globalValDict.update({englishVal: sinhalaGen})
                translatedValueArray.append(sinhalaGen)
            return translatedValueArray, globalValDict
        else:
            englishVal = valueArray.strip()
            if englishVal in globalValDict:
                sinhalaGen = globalValDict[englishVal]
            else:
                sinhalaGen = mtranslate.translate(englishVal, 'si', 'en')
                globalValDict.update({englishVal: sinhalaGen})
            translatedValueArray.append(sinhalaGen)
            return translatedValueArray[0], globalValDict
    else:
        return None, globalValDict


def translate():
    with open('corpus/songs.json', 'r') as t:
        songs = json.loads(t.read())
    with open('corpus/genres.json', 'r') as t:
        genres = json.loads(t.read())
    with open('corpus/artists.json', 'r') as t:
        artists = json.loads(t.read())
    with open('corpus/lyricists.json', 'r') as t:
        lyricists = json.loads(t.read())
    with open('corpus/musics.json', 'r') as t:
        musics = json.loads(t.read())

    for i in range(0, 500):
        if i % 10 == 0:
            time.sleep(15)
        with open('../OriginalData/srcCorpus/s_' + str(i) + '.json', 'r') as f:
            sinhalaSong = {}
            song = json.loads(f.read())

        guitarKey = song.get("guitar_key", None)
        title = song.get("title", None)
        artist = song.get("Artist", None)
        genre = song.get("Genre", None)
        lyricist = song.get("Lyrics", None)
        music = song.get("Music", None)
        lyrics = song.get("song_lyrics", None)
        views = song.get('views', None)

        sinhalaSong.update({"guitar_key": guitarKey})
        sinhalaSong.update({"title": title})
        sinhalaSong.update({"song_lyrics": lyrics})
        sinhalaSong.update({"views": views})

        sinhalaSong.update({"english_lyricst": lyricist})
        sinhalaSong.update({"english_music": music})
        sinhalaSong.update({"english_artist": artist})

        translatedGenre, genres = translateTag(genre, genres)
        if translatedGenre:
            sinhalaSong.update({"Genre": translatedGenre})
        time.sleep(2)
        translatedArtist, artists = translateTag(artist, artists)
        if translatedArtist:
            sinhalaSong.update({"Artist": translatedArtist})
        time.sleep(2)
        translatedLyricist, lyricists = translateTag(lyricist, lyricists)
        if translatedLyricist:
            sinhalaSong.update({"Lyrics": translatedLyricist})
        time.sleep(2)
        translatedMusic, music = translateTag(music, musics)
        if translatedMusic:
            sinhalaSong.update({"Music": translatedMusic})

        songs.append(sinhalaSong)
        with open('corpus/songs.json', 'w') as t:
            t.write(json.dumps(songs))
        with open('corpus/genres.json', 'w') as t:
            t.write(json.dumps(genres))
        with open('corpus/artists.json', 'w') as t:
            t.write(json.dumps(artists))
        with open('corpus/lyricists.json', 'w') as t:
            t.write(json.dumps(lyricists))
        with open('corpus/musics.json', 'w') as t:
            t.write(json.dumps(musics))


if __name__ == "__main__":
    translate()
    pass
