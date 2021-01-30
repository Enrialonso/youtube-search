import json

import requests


class YoutubeSearch:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://www.youtube.com/youtubei/v1/search?key=%s' % self.api_key

    def __build_payload(self, query=None, next_token=None):
        payload = {
            'context': {
                'client': {
                    'hl': 'es',
                    'gl': 'ES',
                    'geo': 'ES',
                    'visitorData': 'CgtlVmpXYjZMQkRoSSjkyLWABg%3D%3D',
                    'userAgent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20210120.08.00',
                    'platform': 'DESKTOP'
                }
            }
        }
        if query:
            payload['query'] = query
        elif next_token:
            payload['continuation'] = next_token
        else:
            raise Exception('Need set query or next_token for make search!')

        return json.dumps(payload)

    def __get_next_token(self, search_response):

        if 'contents' in search_response:
            for item in \
                    search_response['contents']['twoColumnSearchResultsRenderer']['primaryContents'][
                        'sectionListRenderer'][
                        'contents']:
                if 'continuationItemRenderer' in item:
                    return item['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

        elif 'onResponseReceivedCommands' in search_response:
            for item in search_response['onResponseReceivedCommands'][0]['appendContinuationItemsAction'][
                'continuationItems']:
                if 'continuationItemRenderer' in item:
                    return item['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

        return None

    def __get_response(self, search_response):
        list_response = []
        if 'contents' in search_response:
            object = \
                search_response['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'][
                    'contents']
        else:
            object = search_response['onResponseReceivedCommands'][0]['appendContinuationItemsAction'][
                'continuationItems']

        for item in object:
            if 'itemSectionRenderer' in item:
                for i in item['itemSectionRenderer']['contents']:
                    if 'channelRenderer' in i or 'videoRenderer' in i:
                        list_response.append(i)

        return list_response

    def search(self, query=None, next_token=None):
        data = {}
        payload = self.__build_payload(query=query) if query else self.__build_payload(next_token=next_token)
        res = requests.request("POST", self.url, data=payload)
        if res.ok:
            res = res.json()
            data['search_result'] = self.__get_response(res)
            next_token = self.__get_next_token(res)
            data['next_token'] = next_token
            return data
        else:
            raise Exception(f'ERROR: requests error, http error code: {res.status_code}, message: {res.text}')
