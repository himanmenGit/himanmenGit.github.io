---
layout: post
title: "자기자신과 슈퍼유저만 접근 가능한 뷰를 위한 Mixin"
categories:
  - Django
tags:
  - Django
  - Django
  - Mixin
---


어떤 뷰를 접근할 경우 로그인 하지 않았을 경우나
로그인 했지만 슈퍼유저나 자기자신이 아닐 경우에 접근을 제한하는 Mixin을 만들어 봄

더 좋은 방법이 있을 것 같은데 떠오르지 않음..

`LoginRequiredMixin`을 상속받아 로그인을 강제함
그리고 로그인이 통과되면 현재 유저가 슈퍼유저인지 자기자신인지 판단하여 진행

`common_mixin.py`
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status

class SelfSuperUserRequiredMixin(LoginRequiredMixin):
    """
    로그인 유저가 아니면 로그인 페이지로
    슈퍼유저 이거나 본인이면 진행
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.model, pk=kwargs.get('pk', ''))
            login_check_mixin = super().dispatch(request, *args, **kwargs)
            if login_check_mixin.status_code == status.HTTP_200_OK:
                if instance.user.username != request.user.username and not request.user.is_superuser:
                    return HttpResponseRedirect('/')
            return login_check_mixin
        except Http404:
            return HttpResponseBadRequest()
```

뷰에서 사용

`UserDetailView`
```python
from django.contrib.auth import get_user_model

from .common_mixin import SelfSuperUserRequiredMixin


User = get_user_model()


class UserDetailView(SelfSuperUserRequiredMixin, DetailView):
    model = User
```
