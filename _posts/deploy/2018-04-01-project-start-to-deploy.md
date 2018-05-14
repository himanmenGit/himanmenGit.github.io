---
layout: post
title: "프로젝트 생성부터 배포까지"
categories:
  - Deploy
tags:
  - Deploy
---


# 처음부터 하는 배포

**1. 프로젝트 생성 및 설정**
```bash
mdkir project
cd project

pyenv virtualenv 3.6.4 project-env
pyenv localenv project-env

pip install django
django-admin startproject config
mv config app

git init
git remote add <git hub repository>

touch .gitignore 

www.gitignore.io에서 .gitignore작성
<Git, macOS, Linux, Python, PyCharm+all, Django>

파이참을 열어 app 루트 폴더 지정
프로젝트 인터프리터 project-env로 지정

mkdir .requirements
pip freeze > .requirements/local.txt
```
---
**2. 프로젝트 설정 분리**
config의 settings 와 uwsgi를 환경별로 분리
```bash
├── __init__.py
├── settings
│   ├── __init__.py
│   ├── base.py
│   ├── dev.py
│   ├── local.py
│   └── production.py
├── urls.py
└── wsgi
    ├── __init__.py
    ├── dev.py
    ├── local.py
    └── production.py
```
==settings.base==
공통된 속성들을 정의
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')
SECRETS_LOCAL = os.path.join(SECRETS_DIR, 'local.json')
SECRETS_DEV = os.path.join(SECRETS_DIR, 'dev.json')
SECRETS_PRODUCTION = os.path.join(SECRETS_DIR, 'production.json')

secrets = json.loads(open(SECRETS_BASE, 'rt').read())

# Static
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
...
```
==settings.[dev|local|production]==
각 개발 환경에 맞는 설정
```python
from .base import *

secrets = json.loads(open(SECRETS_[LOCAL|DEV|PRODUCTION], 'rt').read())
set_config(secrets, __name__, root=True)

# local|dev True 
# production False
DEBUG = True

# local
ALLOWED_HOSTS = []

# dev
ALLOWED_HOSTS = [
    '.himanmen.com'
    '.elasticbeanstalk.com',
    'localhost',
    '127.0.0.1',

]

# production
ALLOWED_HOSTS = [
    '.himanmen.com'
    '.elasticbeanstalk.com',
]

WSGI_APPLICATION = 'config.wsgi.[local|dev|production].application'

INSTALLED_APPS += [
    # dev|production
    'storages',
]

# dev|production
DEFAULT_FILE_STORAGE = 'config.storage.DefaultFilesStorage'
STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'
```

==uwsgi.[dev|local|production]==
```python
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.<local|dev|production>")

application = get_wsgi_application()
```
**3. .config폴더 분리**
```bash
├── dev
│   ├── nginx-app.conf
│   ├── nginx.conf
│   ├── supervisor.conf
│   └── uwsgi.ini
├── local
│   ├── nginx-app.conf
│   ├── nginx.conf
│   ├── supervisor.conf
│   └── uwsgi.ini
└── production
    ├── nginx-app.conf
    ├── nginx.conf
    ├── supervisor.conf
    └── uwsgi.ini
```
==nginx.conf==
```bash
daemon off;
user root;
worker_processes 4;
pid /run/nginx.pid;

events {
    worker_connections 768;
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

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```
==nginx-app.conf==
```bash
server {
    listen 80;
    # [local|dev|production] 분리 가능
    server_name *.elasticbeanstalk.com localhost .himanmen.com;
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
        alias /stv/project/.static/;
    }
}
```

==supercisor.conf==
```bash
[program:nginx]
command : nginx

[program:uwsgi]
command = uwsgi -i /srv/project/.config/[local|dev|production]/uwsgi.ini
```

==uwsgi.ini==
```bash
[uwsgi]
chdir = /srv/project/app
module = config.wsgi.dev

socket = /tmp/app.sock

master = true
vacuum = true
logto = /tmp/uwsgi.log
log-reopen = true
```
---
**4. .requirements 분리**
각 환경 별로 필요한 `pip list` 분리
```bash
├── dev.txt
├── local.txt
└── production.txt
```
---
**5. .secrets 분리**
```bash
├── base.txt
├── dev.txt
├── local.txt
└── production.txt
```
==base.json==
```json
{
  "SECRET_KEY": "<DJANGO SECRET KEY>"
  ...
}
```
==local.json==
```json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.sqlite3",
      "NAME": "os.path.join(BASE_DIR, 'db.sqlite3')"
    }
  }
}
```
===dev.json==
```json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "<AWS RDS ENDPOINT>",
      "NAME": "<DATABASE NAME>",
      "USER": "<USER NAME>",
      "PASSWORD": "<PASSWORD>",
      "PORT": <PORT DEFAULT 5432>
    }
  }
}
```

==production.json==
```json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "<AWS RDS ENDPOINT>",
      "NAME": "<DATABASE NAME>",
      "USER": "<USER NAME>",
      "PASSWORD": "<PASSWORD>",
      "PORT": <PORT DEFAULT 5432>
    }
  }
}
```

**7. .gitignore 추가 작성**
```bash
# Custom
/.media
/.static
/.secrets

...
```
**9. 환경 별 Dockerfile추가**
```bash
FROM            python:3.6.4-slim
MAINTAINER      study.himanmen@gmail.com

# apt-get으로 nginx, supervisor 설치
RUN             apt-get -y update
RUN             apt-get -y dist-upgrade
RUN             apt-get -y install build-essential nginx supervisor

# requirements만 복사
COPY            .requirements/[local|dev|production].txt /srv/requirements.txt

# pip install
WORKDIR         /srv
RUN             pip install -r  /srv/requirements.txt
RUN             rm -f           /srv/requirements.txt

ENV         BUILD_MODE [local|dev|production]
ENV         DJANGO_SETTINGS_MODULE config.settings.${BUILD_MODE}

# 소스폴더를 통째로 복사
COPY            . /srv/project

# nginx 설정 파일을 복사 및 링크
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx.conf       /etc/nginx/nginx.conf
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx-app.conf  /etc/nginx/sites-available/
RUN             rm -f   /etc/nginx/sites-enalbed/*
RUN             ln -sf  /etc/nginx/sites-available/nginx-app.conf   /etc/nginx/sites-enabled/

# supervisor설정 파일을 복사
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/supervisord.conf  /etc/supervisor/conf.d/

# pkil niginx후 supervisord -n실행
CMD             pkill nginx; supervisord -n
```
**10. uwsgi 설치후 requirements 추가**
```bash
pip install uwsgi
pip freeze > .requirements/local.txt
```
**11. local에서 DockerRun 실행후 잘 실행되는지 확인**
```bash
docker build -t project:local -f Dockerfile.local .
docker run --rm -it -p 8000:80 project:local
```
**12. sentry 붙이기**

```bash
pip install raven --upgrade
pip freeze > .requirements/local.txt
```
==senty에 가서 프로젝트 만들고 키 받아와서 base.json에 넣기==

```json
"RAVEN_CONFIG": {
    "dsn": "https://<Sentry DSN>",
    "release": "raven.fetch_git_sha(os.path.abspath(os.pardir)),"
  },
  
  
  "LOGGING": {
    "version": 1,
    "disable_existing_loggers": "True",
    "root": {
      "level": "WARNING",
      "handlers": [
        "sentry"
      ]
    },
    "formatters": {
      "verbose": {
        "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
      }
    },
    "handlers": {
      "sentry": {
        "level": "ERROR",
        "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        "tags": {
          "custom-tag": "x"
        }
      },
      "console": {
        "level": "DEBUG",
        "class": "logging.StreamHandler",
        "formatter": "verbose"
      }
    },
    "loggers": {
      "django.db.backends": {
        "level": "ERROR",
        "handlers": [
          "console"
        ],
        "propagate": "False"
      },
      "raven": {
        "level": "DEBUG",
        "handlers": [
          "console"
        ],
        "propagate": "False"
      },
      "sentry.errors": {
        "level": "DEBUG",
        "handlers": [
          "console"
        ],
        "propagate": "False"
      }
    }
  }
```
==settings.base 에 raven 불러 오기==
```python
setattr(sys.modules[__name__], 'raven', importlib.import_module('raven'))
INSTALLED_APPS = [
    ....
    
    'raven.contrib.django.raven_compat',
]
```
==테스트==
```bash
./manage.py raven test
```

**13. AWS RDS 만들기**

1. 시작
2. PostgreSQL선택(RDS 프리티어에 적용되는 옵션만 사용 체크)
3. DB 세부 정보 지정
4. 인스턴스 식별자 모두 소문자
5. 마스터 사용자 이름(데이터베이스 기본 사용자 이름 | 데이터 베이스의 슈퍼 유저)
6. 고급 설정 구성
7. 퍼블릭 엑세스 가능성 (예)
8. 기존 vpc보안 그룹 사용(RDS Secutiry Group 만들어서 적용) default 는 삭제
	* 새 보안 그룹 생성
	* RDS Security Group
9. 데이터베이스 옵션 -> 데이터 베이스 이름 <name>
10. 인스턴스 시작

==[dev/production].json 파일 수정==
```json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "<RDS EndPoint>",
      "NAME": "<DB Name>",
      "USER": "<DB SuperUser>",
      "PASSWORD": "<PassWord>",
      "PORT": 5432
    }
  }
}
```

*RDS Security Group 인바운드 규칙 추가*
```bash
Postgres|TCP|5432|내 IP|...|설명
```

**14. S3 관련 설정추가**
```bash
pip install django-storages
pip install boto3
pip freeze > .requirements/local.txt
```

==config에 storages.py 추가==
```python
from storages.backends.s3boto3 import S3Boto3Storage


class StaticFilesStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class DefaultFilesStorage(S3Boto3Storage):
    location = 'media'
```
==config.urls.py 에 MEDIA_ROOT추가==
```python
from django.conf import settings
from django.conf.urls.static import static

...

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
```
AWS S3 Bucket 만들기
1. IAM에 S3 유저를 만들고 
2. ~/.aws/credentials 에 [s3] 프로필을 가진 유저를 만듬
```python
import boto3
session = boto3.Session(profile_name='s3')
client = session.client('s3')
client.create_bucket(Bucket='fc-7th-ec2-deploy-himanmen', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
```

> `create_bucket(Bucket='name')`에서 `name`은 전 세계에서 유일한 이름이어야 한다. 다른 AWS 사용자의 `bucket`이름을 사용 할 수 없다. 그리고 언더스코어가 아닌 하이픈을 사용 해야 한다.
를 하게되면 `AWS S3`에 `Bucket`이 생성된 것을 볼수 있다.

==base.json에 s3관련 설정 추가==

```json
  ....
  "AWS_STORAGE_BUCKET_NAME": "<AWS S3 BUCKET NAME>",
  "AWS_DEFAULT_ACL": "private",
  "AWS_S3_REGION_NAME": "ap-northeast-2",
  "AWS_S3_SIGNATURE_VERSION": "s3v4",
  "AWS_S3_ENDPOINT_URL": "https://s3.ap-northeast-2.amazonaws.com",
```

**15. IAM에 eb전용 유저 만들기**
1. 사용자 추가
2. 프로그래밍 방식 액세스
3. 기존 정책 직접 연결 후 `elastickbeanstalk`검색
4. `AWSElasticBeanstalkFullAccess` 선택
5. 사용자 만들고 해당 키 저장
6. 엑세스 키 ID와 비밀 액세스 키를 가지고 `~/.aws`에 `credentials`에 유저 저장
==~/.aws/credentials==
```python
[airbnb]
aws_access_key_id = <AWS ACCESS KEY ID>
aws_secret_access_key = <AWS SECRET ACCESS KEY>
```
**16. ebcli를 이용해서 eb application을 설정**
```bash
pip install awsebcli
pip freeze > .requirements/local.txt
```

프로젝트 폴더 루트로 간후
```bash
eb init --profile <profile name>
# region 설정
10) ap-northeast-2 : Asia Pacific (Seoul)
(default is 3): 10

# Create New Application을 선택하거나 
# Enter Application Name이 나오면 이름을 적어줌
(default is "<Project name>") : <EB Application Name>

# 플랫폼은 도커
# 만약 Dockerfile이 있으면 기본 인식 없으면 선택
7) Docker
(default is 1): 7

# 버전은 일단 최신 버전
1) Docker 17.12.0-ce
(default is 1): 1

# 엔터
# 엔터
# 키페어를 선택 하라고 나옴
# 만약 EC2를 만들었었다면 해당 키페어를 사용 아니면 새로 만듬
Type a keypair name.
(Defalut is aws-eb): Airbnb-ec2-key
이후 암호를 넣지 않고 엔터 두번
이러면 AWS에 키페어가 생성되어 있음.
그리고 프로젝트에 `.elasticbeanstalk`폴더가 생성됨.
```
**17. eb에 올릴 Docker을 만듬***
`Dockerfile.production`을 복사해 `Dockerfile`이라는 파일을 만듬
`Dokcerfile.base`를 만들어 `Dockerfile`에서 오래 걸리는 부분만 따로 떼어 냄.
`apt-get` 부분과 `pip install -r` 부분
그리고 `Dockerfile`마지막에 80번 포트를 열어줌
```bash
EXPOSE	80
```
**18. eb 환경 만들기***
```bash
수정사항들을 커밋을 해주고 (안하면 오류남)

eb create --profile <profile name>
Enter Environment Name
(default is <Default Name>): Production

# DNS는 모든 AWS네임에 유일한 이름이어야 한다.
Enter DNS CANME prefix
(default is Production): <unique name>

# 로브 밸런스 타입은 2번 application으로
Select a load balancer type
2) application
(default is 1): 2

# 엔터

```

**18. Docker Hub에 Dockerfile.base 올리기**
`Dockerfile.base`를 빌드해서 허브에 올려야 한다.
```bash
docker build -t <docker images name>:<tag> -f Dockerfile.base .
```
도커 허브에 저장소를 만들자
`<계정명>:<repository name>`이 저장소 주소가 된다.
그리고 만들어 놓은 도커 이미지에 저장소로 태그를 붙임.
```bash
docker tag <docker images name>:<tag>
```
그리고 도커 허브에 해당 이미지를 `push`
```bash
docker push <계정명>/<repository name>:<tag>
```
위에서 만든 태그 네임과 똑같이 사용
만약 도커허브 접근 권한이 없으면 로그인을 한다
도커허브 저장소의 tag탭을 보면 base로 올라간것을 볼 수 있다.
```bash
docker login
```
그리고 커밋을 하고 배포를 하면
```bash
eb delpoy --profile=<profile name>
eb open
```
Interner server error !

**19. ignore된 .secrets들을 관리**
`.secrets`를 스테이징에 올려서 배포를 한후 다시 스테이징에서 지우는 작업을 해야함.
`deploy.sh`파일을 만들고 내용을 추가
```bash
#!/usr/bin/env bash
# 2. eb-deploy시 .secrets폴더를 stage영역에 추가한 후 작업 완료 후 삭제
git add -f .secrets && eb deploy --staged --profile=<profile name>; git reset HEAD .secrets
```

**20. .ebextensions로 migrate collectstatic 자동화**
==00.command_files.config==
```bash
files:
  "/opt/elasticbeanstalk/hooks/appdeploy/post/01_migrate.sh":
    mode: "000755"
    owner: root
    group: root
    content: |
      #!/usr/bin/env bash
      if [ -f /tmp/migrate ]
      then
        rm /tmp/migrate
        sudo docker exec `sudo docker ps -q` /srv/project/app/manage.py migrate --noinput
      fi

  "/opt/elasticbeanstalk/hooks/appdeploy/post/02_collectstatic.sh":
    mode: "000755"
    owner: root
    group: root
    content: |
      #!/usr/bin/env bash
      if [ -f /tmp/collectstatic ]
      then
        rm /tmp/collectstatic
        sudo docker exec `sudo docker ps -q` /srv/project/app/manage.py collectstatic --noinput
      fi

  "/opt/elasticbeanstalk/hooks/appdeploy/post/03_createsu.sh":
    mode: "000755"
    owner: root
    group: root
    content: |
      #!/usr/bin/env bash
      if [ -f /tmp/createsu ]
      then
        rm /tmp/createsu
        sudo docker exec `sudo docker ps -q` /srv/project/app/manage.py createsu
      fi
```
==01_django.config==
```bash
container_commands:
  01_migrate:
    command:  "touch /tmp/migrate"
    leader_only: true
  02_collectstatic:
    command:  "touch /tmp/collectstatic"
# S3를 사용하지 않도록 설정하였으므로 모든 EC2에 정적파일이 존재할 수 있도록 leader_only 옵션 해제
#    leader_only: true
  03_createsu:
    command:  "touch /tmp/createsu"
    leader_only: true
```

**사용자 정의 유저 만들기**
```bash
./manage.py startapp members
```
==models.py==
```python
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
```
==settings.base==
```python
AUTH_USER_MODEL = 'members.User'
...
INSTALLED_APPS = [
    ....
    'members',
]
```

**슈퍼유저 만드는 커맨드 추가**
```bash
├── management
│   ├── __init__.py
│   └── commands
│       ├── __init__.py
│       └── createsu.py
```
==createsu.py==
```python
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                username=settings.SUPERUSER_USERNAME,
                password=settings.SUPERUSER_PASSWORD,
                email=settings.SUPERUSER_EMAIL,
            )
```
==base.json에 계정 설정==
```json
  "SUPERUSER_USERNAME": "<USERNAME>",
  "SUPERUSER_PASSWORD": "<PASSWORD>",
  "SUPERUSER_EMAIL": "<EMAIL>",
```

### eb에 만들어진 ec2 접속 방법
```bash
eb ssh
```
### eb안에 있는 ec2안에 있는 docker접속 방법
```bash
sudo docker exec -it <dokcer Container ID> /bin/bash
```

### uwsgi로그 확인
```bash
cat /tmp/uwsgi.log
```

### 자동으로 로그 보는 법
```bash
eb log
```
eb=activity.log에서 많이 난다.
