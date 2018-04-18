---
layout: post
title: "배포 스크립트"
categories:
  - Deploy
tags:
  - Deploy
---

개발 서버를 만들 때
```
Browser -> runserver -> Django
``` 

실제 배포 환경을 만들 경우 일반 적인 요청
```
Browser -> EC2 -> Nginx -> uWSGI -> Django
``` 

정적 파일을 접근 할 경우
```
Browser(/static/, /media/) -> EC2 -> Nginx
```
이렇게 하는 이유는 Django까지 갔다 오는것 보다 Nginx에서 처리 하는것이 빠르기 때문. (정적 파일 한정)

`config/settings.py`에 추가
```
# ec2-deploy/.static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

# MEDIA (user-uploaded files)
# ec2-deploy /.media
MEDIA_URL = '/media/
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# Static
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
```
`config/urls.py`에 추가
```
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT
)
```
는 `Debug=True` 일 경우에만 동작 한다.
그래서 앞단에서 Nginx가 따로 설정을 할 수 있도록 해야 한다.
`.config`의 `nginx-app.conf`
```
#location /static/ {
#    alias /srv/ec2-deploy/.static/;
#}
location /media/ {
    alias /srv/ec2-deploy/.media/;
}
```
이렇게 해주는 이유는 `/static/` 이나 `/media/`로 오는 요청 같은 경우에는 Django로 넘겨주는것이 아니라 Nginx 자체에서 처리 해주기 위함이다. 

그리고 서버환경에서 파일의 배포 환경 설정을 좀더 편하게 하기 위해 `deploy.sh` 라는 파일을 이용하여 자동으로 서버의 환경을 설정해 보자.
배포 하는 순간(`deploy-ec2`) 복사가 끝나고 자동으로 커맨드가 실행되게 만듬.
> `deploy.sh` 파일의 아이콘이 제대로 나오지 않을경우 `BashSupport` 플로그인을 설치 한다.
> 권한 오류가 날 경우 `deploy.sh` 파일의 권한을 모두사용 가능한 권한으로 바꿔야 한다.`sudo chmod 755 deploy.sh` 를 하자.
```
# .config/deploy.sh

#!/usr/bin/env bash
#export DJANGO_SETTINGS_MODULE=config.settings.production
# Nginx에 존재하던 모든 enabled서버 설정 링크 삭제
sudo rm -rf /etc/nginx/sites-enabled/*
# 프로젝트의 Nginx설정 (nginx-app.conf)를 복사
sudo cp -f /srv/ec2-deploy/.config/nginx-app.conf \
           /etc/nginx/sites-available/nginx-app.conf
# 복사한 Nginx설정을 enabled에 링크
sudo ln -sf /etc/nginx/sites-available/nginx-app.conf \
            /etc/nginx/sites-enabled/nginx-app.conf
# uWSGI서비스 파일을 /etc/systemd/system폴더에 복사
sudo cp -f /srv/ec2-deploy/.config/uwsgi.service \
           /etc/systemd/system/uwsgi.service

## collectstatic을 위한 과정
#cd /srv/ec2-deploy/app
## ubuntu유저로 collectstatic명령어를 실행 (deploy스크립트가 root권한으로 실행되므로)
#/bin/bash -c \
#'/home/ubuntu/.pyenv/versions/fc-ec2-deploy/bin/python \
#/srv/ec2-deploy/app/manage.py collectstatic --noinput' ubuntu

# uwsgi, nginx를 재시작
sudo systemctl enable uwsgi
sudo systemctl daemon-reload
sudo systemctl restart uwsgi nginx
```