---
layout: post
title: "Django User"
categories:
  - Django
tags:
  - Django
---

Django가 기본적으로 사용자 인증 시스템과 함께 제공 된다.
만약 인증 시스템이 필요 없는 애플리케이션을 만들경우 이 기능을 제외 할 수 있다.
Django 인증 시스템은 인증/인가 를 모두 처리 한다.
인증은 사용자가 유효한 사용자 인지 확인하고
인가는 사용자가 수행 할수 있는 권한에 대해 확인한다.
Django는 기본으로 비밀번호 강함 체크, 로그인 시도 막기, 페이스북 로그인 등은 제공하지 않으니 다른 패키지를 사용하여야 한다.

기본 설정에서 Django의 인증 시스템 사용법을 알아 보자
Django에서 인증 프레임워크에 superuser또는 admin staff는 특별한 속성이 설정된 사용자 객체 일뿐 사용자 객체의 클래스는 다르지 않다.
유저 모델 클래스는 단 한개를 사용하고 사용자의 속성은 BooleanField를 하나 넣어서 해당 유저의 속성을 설정한다.
기본적으로 유저가 가져야 하는것은 
* username
* password
* email
* first_name
* last_name
이다 
유저를 만들고 싶다면
```python
from django.contrib.auth.models import User
user = User.objects.create_user('name', 'email', 'password')
user.last_name = 'last_name'
user.save()
```
password가 들어 갈 때  create_user로 통해 들어 가면 특정 해시를 거친 password로 들어 간다. 그냥 create를 하면 password가 row데이터로 들어 가버린다.

또한 set_password 함수를 사용하여 비밀번호를 바꾸면 바꾼 비밀번호를 해시하여 데이터베이스에 넣는다.
```python
user.set_password('new password')
user.save()
```
authenticate를 사용하여 유저를 가져온다.
```python
from django.contrib.auth import authenticate
user = authenticate(username='name', password='password')
if user is not None:
    # 인증 성공
else:
    # 인증 실패
```
기본적으로 사용자 이름 및 암호로 키워드 인수를 받아 자격증명을 가져 온다.
페이스북 로그인이나 다른 로그인 방법으로 인증 백엔드를 등록하면 각 인증 백엔드에 대해 모두 확인하고 특정 백엔드에 자격 증명이 유요한 경우 User객체를 반환한다.

사용자가 인증을 유지 하고 있는지 알아 보는 방법
기본적으로 HTTP요청은 지속적이지 않다. 한번의 request가 가고 response가 오면 해당 연결은 끝이 난다.
하지만 브라우저가 인증을 유지 하는 방법은 session을 사용하여 연결을 유지 하는 것처럼 보이는 것이다.
session은 로그인한 유저가 인증이 되면 특정 키값을 session으로 저장하고 이 키 값을 클라이언트한테 돌려 준다. 클라이언트는 setCookie를 확인하고 받은 데이터가 있으면 자신의 Cookie에 데이터를 저장한다.
그 후 해당 도메인에 접속 할 때 Cookie를 request에 담아서 보낸다. 그러면 서버에서는 받은 데이터 안에 session 키가 있으니 이것을 디비에 검색하여 해당 유저를 찾아서 서버가 인증을 하는 시스템
그리고 request에서 session 값을 검사하는 루틴이 django의 session middleware가 하는 일이다.
```python
if request.user.is_authenticated:
    # 인증 유저
else:
    # 인증 하지 않은 유저
```
session값은 특정 일수가 지나기 전까지는 서버에 유지 된다. 기본적인 SESSION_COOKIE_AGE는 2주일 이다. 만약 2주일안에 한번더 로그인을 하게 되면 2주일이 갱신된다.

그럼 어떻게 session을 기록하느냐 그것은 로그인으로 한다.
login 함수를 사용한다.
```python
from django.contrib.auth import authenticate, login

def view(request):
    username=request.POST['name']
    password=request.POST['passowd']
    user = authenticate(request, username=username, password=password)
    if user is not None:
    	# 이 함수가 실행 될때 DB에 session값을 기록하고
   	# django middle ware가 쿠키를 만든다.
    	# 이후 response받은 브라우저는 setCookie로 값을 전달받아 저장한다.
        login(request, user)
    else:
        ...
```


