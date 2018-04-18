---
layout: post
title: "Django YouTube API"
categories:
  - Django
tags:
  - Django
---

# 0227 django YouTube Api 

`https://console.developers.google.com/?hl=ko`로 접속하여 새 프로젝트를 생성
좋은 이름으로 프로젝트를 만드는데, **프로젝트ID**는 유일 값 이어야 한다. 수정을 눌러서 유일값으로 만들어 주자.
대시 보드에 `+API 및 서비스 사용 설정`으로 들어가서 검색창에 `youtube` 검색.
그리고 `YouTube Data API v3`들어가서 사용 설정 해주기.
사용자 인증 정보 만들기 접속. 구성설정 웹 서버, 공개 데이터 설정후 `어떤 사용자 인증 정보가 필요한가요?` 클릭. 완료!
이후 인증 정보의 API키 의 키를 복사 하여 장고의 `settings.py`에 넣자
```
# settings.py
YOUTUBE_API_KEY = <YouTube API Key>
```
그리고 `requests`를 이용하여 요청을 날려서 데이터를 받아온다.
```
import requests
def youtube(request):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'maxResults': '10',
        'q': 민아,
    }
    response = requests.get(url, params)
    response_dict = response.json()

    context = {
        'youtube_items': response_dict['items']
    }
    return render(request, 'youtube.html', context)
```
