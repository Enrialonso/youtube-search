import requests
import re
import json
from time import sleep

url = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

def build_payload(query_string=None, next_token=None):
    payload = {
        "context": {
            "client": {
                "hl": "es",
                "gl": "ES",
                "geo": "ES",
                "visitorData": "CgtlVmpXYjZMQkRoSSjkyLWABg%3D%3D",
                "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36,gzip(gfe)",
                "clientName": "WEB",
                "clientVersion": "2.20210120.08.00",
                "platform": "DESKTOP"
            }
        },
        "webSearchboxStatsUrl": "/search?oq=game&gs_l=youtube.1.0.0l14.3120.3509.0.5429.4.4.0.0.0.0.147.275.0j2.2.0....0...1ac.1.64.youtube..2.2.274....0.ByG0o0O3p-Y",
    }
    if query_string:
        payload['query'] = query_string

    if next_token:
        payload['continuation'] = next_token

    return json.dumps(payload)

def get_next_token(response):
    try:
        if 'contents' in response:
            return response['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'] \
                ['contents'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

        if 'onResponseReceivedCommands' in response:
            return response['onResponseReceivedCommands'][0]['appendContinuationItemsAction'] \
            ['continuationItems'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

    except Exception:
        print('error')
        return None

def print_title(response_search=None):
    if 'contents' in response:
        res = response_search['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'] \
        ['contents'][0]['itemSectionRenderer']['contents']
    else:
        res = response_search['onResponseReceivedCommands'][0]['appendContinuationItemsAction'] \
            ['continuationItems'][0]['itemSectionRenderer']['contents']

    for item in res:
        if 'videoRenderer' in item:
            print(item['videoRenderer']['title']['runs'][0]['text'])

headers = {
    'cookie': 'endpoint=%7B%22clickTrackingParams%22%3A%22CBcQ7VAiEwi80u7IxbTuAhUJ4dUKHfC4CZk%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fresults%3Fsearch_query%3Dgame%2Bawards%2B2020%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_SEARCH%22%2C%22rootVe%22%3A4724%7D%7D%2C%22searchEndpoint%22%3A%7B%22query%22%3A%22game%20awards%202020%22%7D%7D',
    'Content-Type': 'application/json'
}

payload = build_payload(query_string='laura en america')
index = 1

while True:
    print(index)
    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()

    print_title(response)

    next_token = get_next_token(response)
    if next_token:
        payload = build_payload(next_token=next_token)
        index += 1
    else:
        break
