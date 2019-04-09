---
layout: post
title: "EC2에 docker-compse(django nginx uwsgi postgres)"
categories:
  - Deploy
tags:
  - Deploy
  - Docker
---

# ec2 on docker-compose (django uwsgi nginx postgres)

### 환경
`AWS ubuntu 16.04 LTS`
`docker 18.09.4`
`docker-compose 1.24.0`

### 코드
[ec2-on-docker-compose](https://github.com/himanmenGit/docker-practice)

### ec2 설정및 Docker CE 설치
[ec2-on-docker](https://himanmengit.github.io/deploy/2019/04/02/ec2-on-docker(django-nginx-uwsgi-supervisor).html)의 설치 과정을 그대로

### docker-compose 설치

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(una
me -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

```bash
$ docker-compose -v
docker-compose version 1.24.0
```

### Django 프로젝트 설정 및 docker-compose 설정

+ docker-compose.yml에서 web의 docker와 nginx의 docker를 관리 함.

```
ec2-docker-compose
├── docker-compose.yml
├── nginx
│   ├── Dockerfile
│   ├── nginx-app.conf
│   └── nginx.conf
└── web
    ├── Dockerfile
    ├── app
    │   ├── config
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   └── wsgi.py
    │   └── manage.py    
    ├── requirements.txt
    └── uwsgi.ini
```

### web

+ settings.py

```python

ALLOWED_HOSTS = [
    'localhost', '.amazonaws.com'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

+ url.py

```python
from django.contrib import admin
from django.urls import path

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home)
]
```

+ views.py

```python
from django.http import HttpResponse


def home(reqeust):
    return HttpResponse('<html><body><h1>Hello World</h1></body></html>')

```

+ requirements.txt

```bash
django==2.2
uwsgi==2.0.18
psycopg2-binary==2.7.7
```

+ uwsgi.ini

```ini
[uwsgi]
socket = /srv/ec2-docker-compose/apps.sock
master = true

processes = 4
threads = 2

chdir = /srv/ec2-docker-compose/app
module = config.wsgi

logto = /var/log/uwsgi/uwsgi.log
log-reopen = true

vacuum = true
```

+ Dockerfile

```
FROM python:3.6.7

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /srv/ec2-docker-compose
ADD requirements.txt /srv/ec2-docker-compose

WORKDIR /srv/ec2-docker-compose

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /srv/ec2-docker-compose
```

### nginx

+ nginx.conf

```nginx
user root; # <--- www-data에서바꿈
worker_processes 4;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    # multi_accept on;
}

http {

    ##
    # Basic Settings
    ##

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    # server_tokens off;

    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ##
    # SSL Settings
    ##

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;

    ##
    # Logging Settings
    ##

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    ##
    # Gzip Settings
    ##

    gzip on;
    gzip_disable "msie6";

    # gzip_vary on;
    # gzip_proxied any;
    # gzip_comp_level 6;
    # gzip_buffers 16 8k;
    # gzip_http_version 1.1;
    # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    ##
    # Virtual Host Configs
    ##

    # include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}


#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
#
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```

+ nginx-app.conf

```nginx

upstream uwsgi {
    server unix:/srv/ec2-docker-compose/apps.sock;
}

server {
    listen 80;
    server_name localhost *.amazonaws.com;
    charset utf-8;
    client_max_body_size 128M;

    location / {
        uwsgi_pass      uwsgi;
        include         uwsgi_params;
    }

    location /media/ {
        alias /srv/ec2-docker-compose/.media/;
    }

    location /static/ {
        alias /srv/ec2-docker-compose/.static/;
    }
}
```

+ Dockerfile

```
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml

```
version: '3'
services:

    db:
      container_name: postgres
      image: postgres
      environment:
        POSTGRES_PASSWORD: password123
      ports:
        - "5432:5432"
      volumes:
        - pgdata:/var/lib/postgresql/data/

    nginx:
        container_name: nginx
        build: ./nginx
        restart: always
        ports:
          - "80:80"
        volumes:
          - ./web:/srv/ec2-docker-compose
          - ./log:/var/log/nginx
        depends_on:
          - web

    web:
        container_name: web
        build: ./web
        restart: always
        command: uwsgi --ini uwsgi.ini
        volumes:
          - ./web:/srv/ec2-docker-compose
          - ./log:/var/log/uwsgi
        depends_on:
          - db

volumes:
    pgdata:
```

### ec2 설정

이전과 마찬가지로 `80` 포트를 열어 줌.
`ec2(80) -> docker(80[nginx:80]) -> web(uwsgi[apps.sock]) -> django`

```bash
scp -ri <aws_credential.pem> <project> ubuntu@<public ip>:/home/ubuntu/
```

### ec2 접속후 실행

```bash
cd ~/<project>
docker-compose up -d --build # 빌드 & 런

# 소스를 수정 했다면
docker-compose down # 내림
docker-compose up -d # 데몬으로 다시 돌림
```

## 참고
출처 : [twtrubiks github](https://github.com/twtrubiks/docker-django-nginx-uwsgi-postgres-tutorial)