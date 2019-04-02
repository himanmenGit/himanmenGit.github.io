---
layout: post
title: "EC2에 redis-server, nginx, supervisor 설치"
categories:
  - Deploy
tags:
  - Deploy
---

# 환경

* ubuntu 16.04
* 설치일 2019년 4월 2일 기준 버전. 
* ec2 python version 2.7.12

## 초기 설정

EC2를 만들고 `apt-get`을 업데이트 한다.

```bash
sudo apt-get udpate
sudo apt-get upgrade
```

# redis-server 설치

`ppa`에 `redis-server`를 등록후 설치 한다. 
```bash
sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get install redis-server
```

```bash
redis-server -v
Redis server v=5.0.4 sha=00000000:0 malloc=jemalloc-5.1.0 bits=64 build=6840e401a1a58e85
```

버전 `v = 5.0.4` 이다.

`/etc/redis/redis.conf`에 설정을 수정 하고 `redis-server`를 재시작

```bash
sudo systemctl restart redis-server.service
```

## 자동 재시작

```bash
sudo systemctl enable redis-server.service

Synchronizing state of redis-server.service with SysV init with /lib/systemd/systemd-sysv-install...
Executing /lib/systemd/systemd-sysv-install enable redis-server
Created symlink from /etc/systemd/system/redis.service to /lib/systemd/system/redis-server.service.
```
이후 ec2를 재부팅 하고 `redis-cli`로 `ping`하면 `pong`

```bash
redis-cli
127.0.0.1:6379> ping
PONG
``` 

> 설치 방법중 제일 간단했따. 

# nginx 설치

```bash
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update
sudo apt-get install nginx
```

```bash
sudo nginx -v
nginx version: nginx/1.14.2
```

## nginx 설정
```bash
/etc/nginx/sites-available
/etc/nginx/sites-enabled
```
`sites-available`에 잇는 `conf`로 여러 가상서버를 만들고 사용하고 싶은 서버를 `sites-enabled`로 링크를 걸면 된다.
기본은 `default` 파일로 설정 되어 있다. 

## 확인 및 재시작

* 위 설정으로 설치시 daemon으로 자동으로 서버 구동시 재시작이 된다.
* `sudo nginx -t`로 설정 파일 검사
* `sudo systemctl restart nginx`로 `nginx` 설정 변경후 재시작.


# supervisor 설치

```bash
sudo apt-get install supervisor
```

```bash
sudo supervisord -v
3.2.0
```

```bash
sudo touch /etc/supervisor/conf.d/supervisor_nginx.conf
sudo vim /etc/supervisor/conf.d/supervisor_nginx.conf
```

해당 파일에 데몬을 돌릴 프로그램을 명명 할수도 있다.
```bash
[program:uwsgi]
command = uwsgi -i /srv/project/.config/dev/uwsgi.ini
```

uwsgi.ini
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

아니면 각각의 프로세스를 다른 파일로 만들어서 사용할 수도 있다.
```bash
[program:example]
user = root
name = %(program_name)
command = /home/ubuntu/example/gunicorn/start.sh
stdout_logfile = /home/ubuntu/example/logs/gunicorn_supervisor.log
stopsignal=INT
redirect_stderr = true
environment=LANG=en_US.UTF-8, LC_ALL=en_US.UTF-8
```

start.sh
```bash
#!/bin/bash

TARGET_VENV=/home/ubuntu/.pyenv/versions/example
source ${TARGET_VENV}/bin/activate

SOCKFILE=/home/ubuntu/webapp/example/run/example.sock
cd /home/ubuntu/webapp/example/app

exec gunicorn config.wsgi.dev \
  --name=example \
  --timeout=120 \
  --workers=5 \
  --worker-class=gevent \
  --user=root --group=root \
  --bind=unix:${SOCKFILE} \
  --log-level=debug \
```

## 참고

### redis-server
출처 : [스택오버플로우](https://askubuntu.com/questions/868848/how-to-install-redis-on-ubuntu-16-04)
출처 : [TongChun님 블로그](https://dejavuqa.tistory.com/153)

### nginx
출처 : [recordingbetter`s devlog](http://recordingbetter.com/aws/2017/07/05/06-Nginx-Supervisor)
