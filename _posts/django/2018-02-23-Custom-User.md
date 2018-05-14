---
layout: post
title: "Django Custom User"
categories:
  - Django
tags:
  - Django
---

## Custom User 기초

Django의 초기에는 `User`정보를 `usename, password, email, fristname, lastname` 만 있었다.
그런데 기존 유저의 객체를 바꾸는게 불가능 했기 때문에 `User`정보를 추가 할 때 `One To One` 필드로 유저 프로필을 만들어 기존 유저 모델과 연결했다. 하지만 사용하기 불편하여 유저 모델 확장 기능이 추가 됨.

`Authentication backends`는 사용자 모델에 저장되는 이름과 비밀번호를 쓰지 않는 다른 서비스에 대한 인증이 필요 할때 확장 가능한 시스템을 제공함.

우리는 기본 사용자 모델을 확장 하거나 완전히 사용자 **기본 모델을 대체** 하여 사용할 수 있다.

사용자 기본 모델을 확장하거나 대체하는 방식은 각각 두가지 방법이 존재 한다.

### 기본 유저 모델을 확장하고 싶을때의 방법
프록시 모델 사용
* 사용자 모델의 테이블 대한 변경 사항 없이 순수한 동작(python method)만 추가 하여 쓰는 경우.
One To One 필드 사용
* 사용자 모델과 `One To One`으로 연결 되는 모델을 만들어서 연결 하여 추가 필드를 사용.

### 기본 유저 모델을 대체하고 싶을때의 방법
기본적으로 제공하는 유저 모델을 베이스로 하는 방법
* 기본적으로 장고가 제공하는 모델을 기반으로 씀.
유저 모델을 완전히 새로 직접 정의 하는 방법
* 장고가 제공하는 유저 모델의 최소한의 기능 즉 뼈대만 가지고 있는 모델을 씀.
> 외부 인증 라이브러리들을 쓸때 기본적으로 장고의 기본 유저 모델을 기반으로 라이브러리들을 만들기 때문에 사용자 지정 모델을 완전히 대체 할 경우 라이브러리 사용에 문제가 생길 수가 있다.

장고에 내장된 유저 모델이 항상 좋은것은 아닌다. 만약 사용자 이름 대신 이메일을 식별 토큰으로 사용 할 수도 있다. 이런 경우 새로운 유저 모델을 정의 한다.(장고가 제공해주는 모델을 상속받아 정의)
```python
AUTH_USER_MODEL = `myapp.MyUser`
```

**새로운 프로젝트를 시작할 경우 기본 사용자 모델로도 충분하지만 기본적으로 사용자 지정 모델을 설정 하는것이 좋다. 확장이 용이 하여 필요에 따라 사용자에 대한 정의를 추가 할수 있기 때문이다.**
이유는 미래에 기본 사용자 모델을 사용하다가 필드를 추가할 경우 그것을 장고가 마이그레이션을 해주는 것이 불가능하기 때문이다. 많은 데이터들을 직접 수정해야 한다. 
**그래서 프로젝트를 만들고 제일 처음 하는일이 사용자 지정 유저 모델을 만드는 것이 좋다**

기본 장고 유저 모델인 `User`는 `AbstractUser`를 상속 받는다. 우리는 이 `User`모델을 기본 모델로 사용한다. 그래서 `AbstracUser`을 우리가 상속받아 사용자 지정 유저 모델을 만들면 된다.

새로 정의한 유저 모델을 쓰기 위해서는 `get_user_model()`이라는 함수를 사용해야 한다.
```python
User = get_user_model()
User.objects.filter(pk=1).delete()
```
만약 모델에서 사용자 지정 유저모델을 사용할 경우 (ForeignKey로 연결 한다든지) `settings.AUTH_USER_MODEL`을 사용해야 한다.
```python
from django.conf import settings
from django.db import models

class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
     )
```

사용자 지정 유저 모델 만드는 방법
```python
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.
```
주의 할것은 `admin`에 유저를 등록 할 경우 `User`만 사용해서 할 경우에 관리자 페이지에서 유저를 하나 생성하면 비밀번호에 대한 해시키가 제공되지 않아 로그인이 안되는 일이 생긴다. 그래서 해당 관리자 계정 페이지에 `UserAdmin`에 대한 속성까지 제공하여 등록 해야 한다.
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

form .models import User

# admin.site.register(User) [x]
admin.site.register(User, UserAdmin)
```

만약 사용자 지정유저모델에 닉네임을 추가 하고 관리자 페이지에서 해당 닉네임을 입력하고 싶은 경우 그리고 관리자 페이지의 유저 목록에서 닉네임을 보고 싶은 경우 어떻게 해야 할까.
```python
# members.admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['nickname', 'username', 'email']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname',)}),
    )


admin.site.register(User, MyUserAdmin)
```
`list_display`로 유저 목록에 대한 정보를 정할수 있고,
`fieldsets`으로 기본 유저 모델의 필드와 별명 필드에 대한 `form`을 유저 생성시 볼 수 있다.

