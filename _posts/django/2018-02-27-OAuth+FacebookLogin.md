---
layout: post
title: "Django OAuth와 Facebook로그인"
categories:
  - Django
tags:
  - Django
---

# Django OAuth, FacebookLogin 01

### OAuth
`OAuth`는 `OpenID`로 개발된 ㅍ준 인증 방식으로, 각종 애플리케이션에서 사용자 인증을 거칠때 활용 될 수 있다.

### 언제 쓰는가?
어떤 사이트에 직접 회원가입을 할 경우도 있지만 페이스북, 카카오톡, 트위터 등의 서드파티 계정으로 회원 가입을 하는 경우도 있다. 그런경우 만약 페이스북 아이디로 해당 사이트에 페이스북 계정 정보를 그냥 넘겨 주게되면 보안상 큰 문제가 된다.

### Facebook OAuth
OAuth란 개념을 이용하면 우리가 페이스북 계정이랑 비밀번호를 로그인하고자 하는 사이트에 알려 주지 않아도 해당 사이트에서 사용자의 페이스북 정보의 일부를 사용 할 수 있다. 

### Login Flow
* 사용자가 애플리케이션 접근하며 페이스북 로그인 요청
* 페이스북에 정보를 요청하게 할 수 있는 URL을 사용자에게 다시 반환
* 사용자가 받은 URL을 가지고 페이스북에 권한 요청
* 페이스북에서 사용자를 거쳐 애플리케이션으로 (Authorizaion code, Redirects user)을 보냄
* 애플리케이션은 해당 코드와 비밀 키 값을 사용하여 페이스북 서버에 엑세스 토큰을 요청함 
* 페이스북 에서 전송받은 코드와 비밀 키 값이 일치 하는지 검사 
* 일치 하면 애플리케이션에 엑세스 토큰을 넘겨줌.

> 사용자가 페이스북 로그인 할때 해당 계정에서 이름, 이메일, 친구 목록을 보려고 한다.
> 그 정보가 엑세스 토큰에 담겨 있는데 사용자가 허가 했으니 해당 토큰으로 서버에 요청을 하면 그 정보를 준다.

### 엑세스 토큰
엑세스 토큰 유형은 사용자 액세스 토큰, 앱 액세스 토큰, 페이지 액세스 토큰, 클라이언트 토큰 등 여러 가지의 토큰이 있다.
* 사용자 액세스 토큰은 일반적으로 사용하는 토큰 유형. 앱에서 사용자 대신 페이스북의 데이터를 읽고 수정 하기 위해 API를 호출 할 때마다 사용자 액세스 토큰이 필요함. 일반적으로 로그인 대화 상자를 통해 얻으며, 사용자가 앱에서 토큰을 확보할 수 있도록 허용 해야 한다.
* 앱 엑세스 토큰은 앱 설정을 수정하고 읽는데 필요함. 오픈 그래프 액션을 게시하는데도 사용할수 있다. 앱과 페이스북 간에 사전 합의된 시크릿을 사용하여 생성한 다음 앱 전체 설정을 변경하는 호출 중에 사용 됨. 서버 간 호출을 통해 앱 액세스 토큰을 얻는다.

### 액세스 토큰 검사
액세스 토큰에 대해서 자동화된 검사를 수행 할 수 있다. 만약 인증 기간이 지나면 자동으로 다시 액세스 토큰을 받을 수 있다.
```
GET graph.facebook.com/degun_token?
    input_token={검사가 필요한 토큰}
    &access_token={앱 개발자의 액세스 토큰 또는 앱 액세스 토큰}
```

### 그래프 API
그래프 API는 페이스북에 있는 정보를 꺼내 올수 있도록 해주는 API. 엑세스 토큰을 사용해서 유저정보, 친구목록, 담벼락에 글쓰기 등의 동작을 할 때 사용 한다. 규모가 큰 API라 사용법이 복잡하다.
`https://developers.facebook.com/tools/explorer/` 에서 해당 앱의 사용자 토큰을 받은다음 테스트 해볼 수 있다.
```
me?fields=id,name,email,gender,link,cover
-----------------------------------------
{
  "id": "",
  "name": "",
  "gender": "",
  ...
}
```

### 로그인 플로우 직접 빌드 시작하기
* `https://developers.facebook.com/apps/`
* 새 앱 추가 하여 아무 이름 입력
* Facebook 로그인 항목 설정
* 웹 선택
* 사이트 URL은 `localhost:8000`
* 그리고 왼쪽 `Facebook로그인` 탭의 설정
* 유효한 OAuth 리디렉션 URI에 `http://localhost:8000/` 입력
* 해당 URL로 요청하면 페이스북 로그인 화면이 뜨거나 혹은 권한 요청창이 팝업
```
<a class="btn-facebook" href="https://www.facebook.com/v2.12/dialog/oauth?client_id=<Facebook App ID>&redirect_uri=http://localhost:8000/facebook-login/">페이스북 로그인</a>
```
* 2018년 3월 18일 현재 `Enforce HTTPS for Web OAuth Login` 옵션 강제 적용으로 `http://`로의 리디렉션 불가.
* 그리고 수신된 코드로 엔드포인트를 사용하여 엑세스 토큰과 교환해야함(엔드포인트: URL의 끝 부분) 해당 호출은 앱 시크릿 코드가 사용되므로 해당 코드가 공개되지 않도록 해야한다.

* 엑세스 토큰을 교환하는 코드를 넣어보자. 코드중 `redirect_uri`는 이전에 요청한 `redirect_uri`와 동일 해야 한다.
```
def facebook_login_view(request):
    # code로 부터 AccessToken 가져오기
    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/facebook-login/',
        'client_secret': settings.FACEBOOK_SECRET_CODE,
        'code': request.GET.get('code'),
    }
    response = requests.get(url, params)
    response_dict = response.json()
    ...
```
* 요청한 값은 JSON 형태로 온다.
```
access_token: 
token_type: 
expires_in: 
```
그리고 가져온 엑세스 토큰으로 유저 정보를 가져 올 수 있다.
```
url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict.get('access_token'),
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
            'first_name',
            'last_name',
        ])
    }
    response = requests.get(url, params)
    response_dict = response.json()
    facebook_id = response_dict.get('id')
    name = response_dict.get('name')
    first_name = response_dict.get('first_name')
    last_name = response_dict.get('last_name')
```
> 받아온 사용자의 ID는 요청한 애플리케이션에 대한 고유한 아이디 값이다. 유저자체의 고유 아이디값은 아니다.
가져온 내용에서 유저ID를 가지고 새로운 유저를 만들거나 가져와서 로그인 시키면 된다.
```
    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    login(request, user)
    return redirect('index')
```
이렇게 하면 페이스북 계정으로 사용자를 만들어 로그인 시켜 줄 수 있다.
그리고 페이스북 유저 인증 과정을 커스텀 백엔드에서`Authenticate`를 이용해 유저를 인증해주는 로직을 따로 만들어 줘야 한다. 

### Customizing authentication
`User`모델이 있는 앱에 `backends.py`를 만든다. 이 파일에 페이스북 유저에 대한 검증후 유저를 만들어 주는 일련의 과정을 코드로 넣는다. 
필수로 `get_user()` 함수를 만들어 주어야 한다.
```
# backends.py
class FacebookBackend:
    def authenticate(self):
        # 페이스북 정보 요청후
        # 유저를 검증후 만들거나 가져옴.
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```
만든 백엔드를 `AUTHENTICATION_BACKENDS`에 추가 해야 한다.
```
# config.settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.FacebookBackend',
]

```
그리고 뷰에서 authenticate만 호출하여 유저를 생성혹은 가져 올수 있다.
```
def facebook_login_view(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    login(request, user)
    return redirect('index')
```