# Sinhala Song Lyrics Search Engine

This repository contains the source code for a sinhala songs search engine built using ElasticSearch 7.7.1 and Python 3.7.6.

## Quickstart

These instructions will get you a copy of the project up and running on your local machine.

* Clone the [repository] (https://github.com/avcjeewantha/IRProject.git )
* Start [ElasticSeacrh](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-windows-x86_64.zip) on the port 9200 - Navigate to the ElasticSeacrhdirectory and run the following command in command prompt.

```
./bin/elasticsearch
```

* Navigate in to the project folder and run the following command in command prompt

```
python back-end.py
```

* Visit http://localhost:5000
* Enter the search query

## Structure of the Data

* Title(In Sinhala, In English)
* Artist (In Sinhala, In English)
* Genre (In Sinhala, In English)
* Lyricist (In Sinhala, In nglish)
* Composer (In Sinhala, In English)
* Guitar key (In English)
* Number of views (Number)
* Song lyrics (In Sinhala)

The dataset for the project was scraped from the website [Sinhala Song Book] (https://sinhalasongbook.com/ ).

## Techniques used

### Indexing

* Rule based text mining is used to understand and extract data from the user entered query string.

* ICU_Tokenizer’ which is a standard tokenizer and which has better support for Asian languages to tokenize text into the words.

* Elastic search ‘edge_ngram’ filter was used to generate n-grams. ###MultiSearch with Rule Base classification Rule-based text mining is used to understand and extract data from the user entered query string.

### Rule Based Classification

A rule based classification has been used to classify the user search queries into different types of searches.

### Boosting

Each field of a search is boosted by a certain value based on the keywords present in the search phrase.

## Functionalities

* Bilingual support (both Sinhala and English queries)

```
eg: sunil ආරියරත්න රචිත,  sunil ariyarathna, සුනිල් ආරියරත්න
```

* Faceted Queries (The search engine supports seacrhing by any field that the query string contains any tokens related to a specific data field such as artist, writer or music)

```
eg: එඩ්වඩ් ජයකොඩි ගයන, සුනිල් ආරියරත්න රචිත, ක්ලැසික්, Key: D minor
```

* Range Queries (Search Engine can identify ranges given in the search query and sort by view count)

```
eg: සුනිල් ආරියරත්න රචිත හොදම සංගීත 10,  එඩ්වඩ් ජයකොඩි රචිත හොදම 3
```

![Range](/images/Range.png)

## Authors

* **[Chamoda Jeewantha](https://github.com/avcjeewantha )**


