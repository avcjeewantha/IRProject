import json

#fields=['title', 'song_lyrics']


def aggMultiMatchAndSortQuery(query, sortNum, fields, operator='or'):
    query = {
        "size": sortNum,
        "sort": [
            {"views": {"order": "desc"}},
        ],
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    query = json.dumps(query)
    return query

#fields=['title', 'song_lyrics']


def aggMultiMatchQuery(query, fields, operator='or'):
    query = {
        "size": 500,
        "explain": True,
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    query = json.dumps(query)
    return query
