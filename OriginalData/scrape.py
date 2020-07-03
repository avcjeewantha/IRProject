from bs4 import BeautifulSoup
import requests
import time
import os
import json
import re


def parseHtml(htmlPage):
    links = []
    soup = BeautifulSoup(htmlPage, 'html.parser')
    song_links = soup.find_all("a", {"class": "_blank"})
    for tag in song_links:
        link = tag.get('href')
        links.append(link)
    return links


def processContent(keyValPair):
    if keyValPair:
        keyValPair = keyValPair.get_text()
        splitPair = keyValPair.split(':')
        if len(splitPair) > 1:
            key = splitPair[0]
            val = splitPair[1]
            if ',' in val:
                values = []
                splitVal = val.split(',')
                for value in splitVal:
                    values.append(value)
                return key, values
            else:
                return key, val
        else:
            return None, None
    else:
        return None, None


def parseLyrics(lyrics):
    spaceSet = set([' '])
    processed = ''
    regex = r"([A-z])+|[0-9]|\||-|∆|([.!?\\\/\(\)\+#&])+"
    lyricLines = lyrics.split('\n')
    for line in lyricLines:
        new = re.sub(regex, '', line)
        chars = set(new)
        if not ((chars == spaceSet) or (len(chars) is 0)):
            processed += new + '\n'
    return processed


def parseSong(html_pg):
    soup = BeautifulSoup(html_pg, 'html.parser')
    song = {}
    classList = ["entry-tags", "entry-categories",
                  "entry-author-name", "lyrics", "music"]
    title = soup.find('h1', {"class": "entry-title"}).get_text()
    guitKey = soup.find_all('h3', {'class': None})[0].get_text().split('|')
    views = soup.find('div', {'class': 'tptn_counter'}).get_text().split()[
        1].split('Visits')[0]
    if guitKey and len(guitKey) == 2:
        guitarKey = guitKey[0].split(':')
        if len(guitarKey) == 2:
            guitar_key = guitar_key[1].strip()
            song.update({'guitar_key': guitar_key})
        beat = guitKey[1].split(':')
        if len(beat) == 2:
            beat = beat[1].strip()
            song.update({'beat': beat})
    song.update({'title': title})
    song.update({'views': int(views.replace(',', ''))})
    for class_l in classList:
        content = soup.find_all('span', {"class": class_l})
        if content:
            key, val = processContent(content[0])
            if ((not key is None) and (not val is None)):
                song.update({key: val})
        else:
            pass
    unprocessedLyrics = soup.select('pre')[0].get_text()
    processedLyrics = parseLyrics(unprocessedLyrics)
    song.update({'song_lyrics': processedLyrics})
    print(song)
    print(processedLyrics)
    return song


def getSongList():
    for pageNo in range(1, 11):
        url = 'https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page={}/'.format(
            pageNo)
        print('Scraping the URL : ', url)
        headers = requests.utils.default_headers()
        htmlPage = requests.get(url, headers).text
        linksArray = parseHtml(htmlPage)
        with open('songUrls.csv', 'a') as f:
            for link in linksArray:
                f.write(link + os.linesep)
        time.sleep(10)


def scrapeSongs():
    with open('nextLink.txt', 'r') as f:
        nextIndex = int(f.readlines()[0])
    while nextIndex < 500:
        print('Scraping song', nextIndex)
        with open('songUrls.csv', 'r') as f:
            lines = f.readlines()
        url = lines[int(nextIndex)]
        print(url)
        headers = requests.utils.default_headers()
        res = requests.get(url, headers)
        htmlDoc = res.text
        song = parseSong(htmlDoc)
        with open('srcCorpus/s_' + str(nextIndex)+'.json', 'w+') as f:
            f.write(json.dumps(song))
        nextIndex = nextIndex + 1
        with open('nextLink.txt', 'w') as f:
            f.write(str(nextIndex))
        time.sleep(5)


if __name__ == "__main__":
    getSongList()
    scrapeSongs()
    pass
