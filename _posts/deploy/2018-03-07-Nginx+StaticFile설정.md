---
layout: post
title: "Nginx와 Staticfile 설정"
categories:
  - Deploy
tags:
  - Deploy
---

앞 서 본 `nginx`의 `/static/`의 셋팅은 자신의 `app` 내에서만 Nginx로 처리가 가능하다. `django.contrib.admin` 라는 앱에도 정적 파일이 존재 하지만 접근 해당 셋팅으로는 접근 할 수가 없다. 

모든 설치된 애플리케이션의 정적 파일을 `Nginx`가 서빙하기 위해서는 `./manage.py collectstatic` 를 사용하여야 한다. 
`collectstatic`은 `STATIC_ROOT`라고 지정한 폴더에 모든 애플리케이션이 가진 `static folder`의 내용과 `STATICFILES_DIRS`에 지정 한 내용의 모든파일을 복사 한다. 기존에 있던 파일은 덮어 쓴다.
자동으로 만들어 지는것이 아니라 해당 앱의 폴더의 내용을 그냥 복사 하는것이므로 static 파일의 이름이나 경로가 겹치지 않게 주의 하자.
`.gitingnore`에 해당 폴더를 넣어 주자. 
```bash
/.media
/.static
```
```bash
./manage.py collectstatic
```
그리고 나서 `/static/` 요청을 `Nginx`가 서빙하게 하자
```python
# nginx-app.conf
location /static/ {
    alias /src/ec2/deploy/.static/;
}
```

그리고 서버에서 `./manage.py collectstatic`을 실행 시키기 위해 `deploy.sh`를 수정 해보자
```bash
# deploy.sh
# collectstatic을 위한 과정
cd /srv/ec2-deploy/app
# ubuntu유저로 collectstatic명령어를 실행 (deploy스크립트가 root권한으로 실행되므로)
/bin/bash -c \
'/home/ubuntu/.pyenv/versions/fc-ec2-deploy/bin/python \
/srv/ec2-deploy/app/manage.py collectstatic --noinput' ubuntu

# 서버 재시작 전
```

> 하지만 정적파일이 서버에 없는 경우 결국 `Django`까지 접근 해야 한다.
> `AWS 의 S3`에 데이터를 넣었을 경우 어쩔수 없이 밖에서 꺼내 와야 한다. `Nginx`를 사용할 수도 있긴하다...