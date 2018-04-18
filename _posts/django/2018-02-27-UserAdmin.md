---
layout: post
title: "Django UserAdmin"
categories:
  - Django
tags:
  - Django
---

# User Admin

만약 `admin`에 `UserAdmin` 을 사용한다면 사용자 정의 User에 추가한 필드는 관리자 페이지에 나오지 않는다. 나오게 하기 위해서 `fieldsets`을 정의 해 주어야 한다.
만약 User에 `nickname`과 `img_profile`를 추가 했다고 한 경우에는

```
# admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class MyUserAdmin(UserAdmin):
    model = User
    # 유저 목록
    list_display = ['username', 'nickname', 'username', 'email']
    
    # 유저 정보 관리 페이지 정보 입력창 추가
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'img_profile',)}),
    )


admin.site.register(User, MyUserAdmin)
```