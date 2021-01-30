# Youtube search

This repo is a small class son python for make search on youtube.

### Dependencies:

for use the class you need an api key form the browser, if you have a chrome, follow this steps to find the API-KEY

1. Open de browser and go to youtube web.
2. Open de the developers toll and go to de network tab.
3. On the tab network filter the requests only `XHR`.
4. Make a Search on the yuotybe search input form and press enter.
5. Find the url similar to this: https://www.youtube.com/youtubei/v1/search?key=**AIzaSyAO_FJ2S_Y9_11qcW8**
6. And copy the api key, on the url example the api key is: **AIzaSyAO_FJ2S_Y9_11qcW8**

For install dependencies use this command:

```bash
pip install -r requirements.txt
```

Exmaple usage:

```python

from youtube_search import YoutubeSearch

API_KEY = 'AIzaSyAO_......Y9_11qcW8'

api = YoutubeSearch(api_key=API_KEY)

response = api.search(query='search')

print(response)

```

Response output: you can see full example on data.json 

```json
{
   "search_result":[
      {
         "videoRenderer":{
            "videoId":"c6D8v6DhKc4",
            "thumbnail":{
               "thumbnails":[
                  {
                     "url":"https://i.ytimg.com/vi/c6D8v6DhKc4/hqdefault.jpg?sqp=-oaymwEjCOADEI4CSFryq4qpe1A",
                     "width":480,
                     "height":270
                  }
               ]
            },
            "title":{
               "runs":[
                  {
                     "text":"Sech - Relación (Video Oficial)"
                  }
               ],
              ...
   ],
   "next_token":"EokDEgZzZWFyY2ga....GIHg6BgiC3NlYXJjaC1mZWVk"
}
```
 If the response search have `next_token` you can make another requests and paginate de result of the search.