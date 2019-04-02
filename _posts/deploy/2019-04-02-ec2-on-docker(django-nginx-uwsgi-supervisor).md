---
layout: post
title: "EC2에 docker(django nginx uwsgi supervisor)"
categories:
  - Deploy
tags:
  - Deploy
  - Docker
---

### 환경
`AWS ubuntu 16.04 LTS`

### 저장소를 사용 하여 설치

1. 업데이트
```
sudo apt-get update
sudo apt-get upgrade
```

2. 오래된 docker삭제 (혹시 있으면)
```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

3. apt가 HTTPS를 통해 저장소를 사용할 수 있도록 설정
```
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

4. Docker의 공식 GPG키 추가
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

5. 공식 키에 0EBFCD88 라는 마지막 지문이 있는지 확인
```
sudo apt-key fingerprint 0EBFCD88
```

6. stable저장소 추가
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

# Docker CE 설치

1. 업데이트
```
sudo apt-get udpate
```

2. 최신버전 docker ce 설치
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

3. 확인
```
docker -v
Docker version 18.09.4, build d14af54
sudo docker run hello-world
```

4. Docker 명령어 권한 root로
```
sudo usermod -aG docker ununtu
ec2재접속
docker run hello-world
```

# Django Project 설정후 Dockerfile 만들기
```
django==2.2
```
```
ec2-docker
├── .config
│   ├── nginx-app.conf
│   ├── super_uwsgi.conf
│   └── uwsgi.ini
├── app
│   ├── config
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   └── manage.py
├── Dockerfile
└── requirements.txt
```

### nginx-app.conf

```nginx
server {
    listen 80;
    server_name  *.amazonaws.com localhost;
    charset utf-8;
    client_max_body_size 128M;

    location / {
        uwsgi_pass      unix:///tmp/app.sock;
        include         uwsgi_params;
    }    

    location /media/ {
        alias /srv/project/.media/;
    }

    location /static/ {
        alias /srv/project/.static/;
    }
}
```

### uwsgi.ini

```ini
[uwsgi]
chmod-socket = 664
uid = www-data
gid = www-data

chdir = /srv/ec2-docker/app
module = config.wsgi

socket = /tmp/app.sock

master = true
vacuum = true
logto = /tmp/uwsgi.log
log-reopen = true
```

### super_uwsgi.conf
```conf
[program:uwsgi]
command = uwsgi -i /srv/ec2-docker/.config/uwsgi.ini
```

### Dockerfile

```
FROM            python:3.6.7-slim
MAINTAINER      study.himanmen@gmail.com

ENV             LANG    C.UTF-8

# apt-get으로 nginx, supervisor 설치
RUN             apt-get -y update
RUN             apt-get -y dist-upgrade
RUN             apt-get -y install build-essential nginx supervisor

# requirements만 복사
COPY            requirements.txt /srv/requirements.txt

# pip install
WORKDIR         /srv
RUN             pip install --upgrade pip
RUN             pip install -r  /srv/requirements.txt
RUN             rm -f           /srv/requirements.txt


ENV             DJANGO_SETTINGS_MODULE config.settings

# 소스 폴더 복사
COPY            . /srv/ec2-docker

# nginx 설정 파일 복사 후 링크
RUN             cp -f   /srv/ec2-docker/.config/nginx-app.conf         /etc/nginx/sites-available/
RUN             rm -f   /etc/nginx/sites-enalbed/*
RUN             ln -sf  /etc/nginx/sites-available/nginx-app.conf   /etc/nginx/sites-enabled/

# supervisor 설정 파일 복사
RUN             cp -f /srv/ec2-docker/.config/super_uwsgi.conf         /etc/supervisor/conf.d/

# pkill nginx후 supervisord -n 실행
CMD             nginx; supervisord -n
EXPOSE          80
```

# 프로젝트 복사
```bash
scp -ri <aws_credential.pem> <project> ubuntu@<public ip>:/home/ubuntu/
```
ec2 접속후 `/home/ubuntu/<project>/`로 감.
이후 Docker를 빌드 하고 런.

# DockerBuld & Run
ec2의 보안 그룹에 80포트를 열어 놓아야 한다. 해당 포트로 접속시 `docker`로 서빙(?) 된다.

```bash
cd ec2-docker
docker build -t . ec2-docker
docker run -it -p 80:80 ec2-docker
docker run -it -p 80:80 ec2-docker /bin/bash
docker run -it -d -p 80:80 ec2-docker
```

## 참고
출처 : [초보를 위한 도커 안내서](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)