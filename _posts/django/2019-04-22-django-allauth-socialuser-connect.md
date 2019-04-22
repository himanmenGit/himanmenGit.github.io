---
layout: post
title: "Django allauth에서 일반유저와 소셜유저 연결"
categories:
  - Django
tags:
  - Django
  - allauth  
---

{% raw %}

django에서 allauth를 사용시 일반 유저가 소셜로그인을 연동 하였을 경우에 일반 유저와 소셜 유저를 연결 하는 방법


```python
# settings.py

SOCIALACCOUNT_ADAPTER = 'member.adapter.SocialAccountRegisterAdapter'

```

```python
class SocialAccountRegisterAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.user.id:
            return
        if request.user and request.user.is_authenticated:
            try:
                login_user = User.objects.get(email=request.user)
                sociallogin.connect(request, login_user)                
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        serializer = UserResigerBaseSerializer(data=request.POST)
        serializer.is_valid()
        
        user = super().save_user(request, sociallogin, form)
        return user

```
## 참고 사이트
[코드로그](https://codeday.me/ko/qa/20190322/120669.html)      

{% endraw %}