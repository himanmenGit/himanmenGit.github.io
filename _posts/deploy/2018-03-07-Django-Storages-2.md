---
layout: post
title: "Django Storage 2"
categories:
  - Deploy
tags:
  - Deploy
---

셸을 `dev`로 만들고 `./manage.py runserver 0:8000`을 하면 `WSGI APPLICATION`을 로드 하지 못했다는 에러가 발생한다.

`runserver <command>`가 실행 될때 `runserver.py`의 `Command class` 가 실행된다.
마지막에 `get_handler` 가 실행되면서 `get_internal_wsgi_applications()` 를 리턴 한다. 이것은 현재 `settings`모듈에서 `WSGI_APPLICATION`이 있으면 꺼내 오는 함수다. 없으면 조금 전과 같은 에러를 발생 시킨다.

그렇다면 `django.conf.settings.WSGI_APPLICATION`을 꺼내 온 것과 같은 것이다.

`base.py`에 보면 `WSGI_APPLICATION = 'config.wsgi.application'` 가 있다. 이것을 개발 환경별로 또 빼주면 된다.
```
# local.py
WSGI_APPLICATION = 'config.wsgi.local.application'
# dev.py
WSGI_APPLICATION = 'config.wsgi.dev.application'
# production.py
WSGI_APPLICATION = 'config.wsgi.production.application'
```
이제 `deploy-ec2`를 하고 `./manage.py runserver 0:8000`을 하고 파일을 올려보면 `s3`에 파일이 제대로 올라가는것을 볼 수 있다.

`admin`에서 파일을 지워도 `s3`에서는 지워지지 않는다.
일종의 안정 장치 인거 같은데 `admin`에서 지우면 `s3`에서도 지워지게 만들어 보자
`delete_post` 시그널을 이용하자
```
# .photo.models.py
@receiver(post_delete, sender=Photo)
def model_post_delete(sender, instance, **kwargs):
    default_storage.delete(instance.__dict__['file'])
```