---
layout: post
title: "Django 소셜로그인 패키지 allauth"
categories:
  - Django
tags:
  - Django
---

# allauth
`OAuth` 관련 패키지로 `all-in-one`으로 쓸수 있는것이 `django-allauth`이다.
* 대부분의 소셜 로그인을 지원하고 회원가입시킬 수 있다.
* 공급자가 제공하는 부 정확한 정보를 로그인 연동 과정에서 정확한 입력을 요구할 수 있다.
* 특히 `Django` 시스템의 기존 사용자의 경우에도 `/accounts/social/connections/`경로에서 소셜 로그인 계정을 연동할 수 있다.
* `rememberme`기능 도 지원한다.

## 설치 및 준비
```bash
pip install django-allauth
```
`settings.py`
```python
INSTALLED_APPS = [    
    'django.contrib.admin',
    'django.contrib.auth', # <- 의존성 앱
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # <- 의존성 앱
    'allauth', # <- 추가
    'allauth.account', # <- 추가
    'allauth.socialaccount', # <- 추가
    # 'allauth.socialaccount.providers.facebook', # <- 필요한 소셜 로그인 추가
]
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # <- 디폴트 모델 백엔드
    'allauth.account.auth_backends.AuthenticationBackend', # <- 추가
)
SITE_ID = 1 # 사이트 아이디 기본값
```
`urls.py`
```python
urlpatterns = [
  url(r'admin/', admin.site.urls),
  url(r'^accounts/', include('allauth.urls')), # <- 추가
]
```

## 주요 설정 값
* `ACCOUNT_AUTHENTICATION_METHOD`: 로그인 인증 방법으로 `username, email, username_email` 을 지정할 수 있다. email로 설정할 때는 `ACCOUNT_EMAIL_REQUIRED = True` 옵션을 같이 설정 해야 한다.
* `ACCOUNT_EMAIL_REQUIRED`: 회원가입을 할 때 이메일 주소 입력 필수 여부. 디폴트 - `False` 이므로 이메일 주소를 입력하지 않아도 가입 된다.
* `ACCOUNT_USERNAME_REQUIRED`: 회원가입을 할 때 `username` 입력 필수 여부. 디폴트 - `True` 이므로 `ACCOUNT_AUTHENTICATION_METHOD` 를 통해 이메일로 로그인으로 설정하더라도 반드시 `username` 을 입력해야 가입된다.
* `ACCOUNT_EMAIL_VERIFICATION`: 이메일 유효성 인증이 필요한지 여부. `mandatory`, `optional`, `none` 값을 지정할 수 있으며 `mandatory` 는 회원가입 후 이메일 주소를 인증하지 않으면 회원가입을 하더라도 로그인 할 수 없다. `optional` 은 인증 이메일은 발송 되지만 인증하지 않아도 로그인할 수 있고 `none` 은 인증 메일을 보내지도 않고 로그인 할 수 있다.
* `ACCOUNT_LOGIN_ATTEMPTS_LIMIT`: 지정된 횟수(디폴트-5회) 만큼 로그인 실패 할 경우 `ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT` 설정값으로 지정한 시간(단위-초)만큼 로그인 할 수 없다. `allauth` 로그인 뷰에서 적용되고 `Django` 기본 관리자 로그인 뷰에는 적용되지 않는다.
* `ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT`: 로그인 실패 시 다시 로그인 할 수 없는 시간(디폴트-300초)
* `ACCOUNT_USER_MODEL_USERNAME_FIELD`: 커스텀 사용자 모델을 사용하는 경우 아이디 필드의 이름이 `username` 이 아닌 다른 이름일 경우 지정한다. 만약 `None` 으로 지정할 경우 `allauth` 에서 `username` 과 관련된 모든 기능을 사용하지 않는다. 이 경우 `ACCOUNT_USERNAME_REQUIRED` 값 또한 반드시 `False` 로 지정해야 한다.
* `ACCOUNT_USER_MODEL_EMAIL_FIELD`: 커스텀 사용자 모델을 사용하는 경우 이메일 필드의 이름이 기본값 `email` 이 아닌 다른 이름일 경우 지정한다. 만약 `None` 으로 지정할 경우 `allauth` 에서 `email` 과 관련된 모든 기능을 사용하지 않는다. 이경우 `ACCOUNT_EMAIL_REQUIRED` 값 또한 반드시 `False` 로 지정 해야 한다.
* `ACCOUNT_SIGNUP_FORM_CLASS`: 회원가입 폼 클래스를 지정하고 해당 클래스는 `def signup(self, request, user)` 메소드를 반드시 구현해야 한다.
* `SOCIALACCOUNT_AUTO_SIGNUP`: 디폴트 값은 `True` 이며 SNS 공급자에서 넘겨받은 정보를 가지고 바로 회원가입 시킨다. 부가정보를 입력 받기 위해 `False` 로 설정할 수 있다.
