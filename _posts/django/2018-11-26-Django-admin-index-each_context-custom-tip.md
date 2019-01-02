---
layout: post
title: "Django 관리자 index 페이지 커스텀 트릭"
categories:
  - Django
tags:
  - Django
  - Template
  - Tip
---

# 작성이유
Django 관리자 페이지의 `index`를 커스텀 하고 싶은데 `AdminSite` 를 상속받아 만들지 않고 좀더 간단하게 하고 싶었다.

그래서 `AdminSite`의 메소드를 바꿔 버리는 조금 위험하지만 편한 트릭을 알게되어 적용 해보았다.

# 설명
설명이 따로 없다.

기본 `AdminSite`의 `index` 함수와 `each_context`를 다른 함수로 교체(?) 바꾸어 버리는 방법을 사용

{% raw %}
```python
#project/config_app/admin_site/base.py
import types
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()


def setting_admin_index(context):
    # 인덱스 데이터를 셋팅
    context['total_users'] = User.objects.all().count()


def index(site_object, request, extra_context=None):
    # 인덱스 페이지를 접근 할 때 호출 되는 함수를 재정의
    if not request.user.is_staff:
        return redirect('home')
    else:
        return AdminSite.index(site_object, request, extra_context)


def each_context(site_object, request):
    # context데이터를 가공하여 보냄
    context = AdminSite.each_context(site_object, request)

    # admin인 경우에만 해당 인덱스 페이지를 가져옴
    if request.path == '/admin/':
        setting_admin_index(context)

    return context

# admin.site의 기본 함수를 교체 해버림.
admin.site.index = types.MethodType(index, admin.site)
admin.site.each_context = types.MethodType(each_context, admin.site)
```
{% endraw %}
