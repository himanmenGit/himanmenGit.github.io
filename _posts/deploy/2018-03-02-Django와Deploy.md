---
layout: post
title: "Django와 Deploy"
categories:
  - Deploy
tags:
  - Deploy
---

### 이메일 인증
* 회원가입을 할때 로그인이 될수도 안될수도
* 이메일 인증을 하기 전에 로그인이 안되는 경우
* 이메일 인증을 안해도 로그인은 되지만 기능을 못사용

* 유저 계정의 is_active 
* 기본 장고 시스템에서는 True
* 유저에게 is_Active 값을 False를 넣어 인증 과정을 거치게 한다.

* 입력한 이메일에 인증 메일을 보내줌
* 유저의 여러 정보 내용을 해시하고
* 우리 디비에 해시값을 만들고
* 메일에 해시값을 보내줌
* 해시값이 달린 링크를 보내서 그 링크를 타고 갔을 경우
* 우리 서버에 요청 확인되게 하는 과정
* 디비에 일치하는 해시값이 있는 경우 is_Active를 True로 만들어 준다
* 이 과정이 인증 과정이다.


### base64
* 2진 데이터를 어떤 아스키 문자로 바꾸는 인코딩
* 2진 데이터를 아스키 문자로 바꾸면 텍스트 데이터 형태로 파일을 전송 할 수 있다.
* 문자열을 보내는 프로토콜을 가지고 보내서 받은곳에서 다시 디코딩을 통해 복원한다.
* 원본파일 보다 사이즈가 좀 커진다.
* 제작하는 API에 json으로 보낼때 파일을 base64형태로 바꿔서 보내기도 함.

### site 프레임 워크
* 하나의 장고 프로젝트에서 여러개의 사이트를 한번에 운영할때 쓰는 프레임워크.
* DB는 공유 하면서 실제 보여지는 화면은 다르게.

### Django 프로젝트 만들기
```bash
mkdir django-project
cd django-project
pyenv virtualenv 3.6.4 pyenv-name
pyenv local pyenv-name

git init
mv ~/project/django/melon/.gitignore .
# pip install -r requirements.txt 에 있는 list 모두 설치
mv ~/project/django/melon/requirements.txt requirements.txt

pip install -r requirements.txt
# 또는 하나하나 설치
#pip install django
#pip install ...
#pip freeze > requirements.txt

django-admin startproject config
# 폴더 이름 app으로 바꿈 이후 이후 루트폴더로 바꿈
mv config app

# git 저장소 만들고 remote 설정
git remote ...
```
* PyCharm에서 app폴더 루트폴더로 만들기
* PyCharm에서 Python 인터프리터를 방금 만들었던 local-pyenv version으로 하기

### settings의 secret keys들 숨기기
* .secrets 폴더를 만들고 base.json파일을 만듬
* json 형태로 데이터를 가져다가 쓸 것.
* json 에서는 따옴표 한개`'` 짜리는 지원 하지 않음. `"` 쓸것.
* 마지막에 쉼표가 붙으면 안된다.

```python
# .secrets/base.json
{
  "SECRET_KEY" : "key...asdasd"
}

# .config/settings.py

# ec2-deploy
ROOT_DIR = os.path.dirname(BASE_DIR)

# ec2-deploy/.secrets
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
# ec2-deploy/.secrets/base.json
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')

# base.json파일을 읽어온 결과
f = open(SECRETS_BASE, 'rt')
base_text = f.read()
f.close()

# 위 결과 (JSON형식의 문자열)를 파이썬 객체로 변환
secrets_base = json.loads(base_text)
# or
# 한줄로 요약
secrets_base = json.loads(open(SECRETS_BASE, 'rt').read())

# secrets_base에서 key 값 가져옴
SECRET_KEY = secrets_base['SECRET_KEY']
```

***중요***

`gitignore`에 `.secrets/` 추가해서 깃헙에 안올라가게 함

### EC2 인바운드 규칙 편집
* EC2 - 보안그룹 - EC2 Secutiry Group - 인바운드 규칙 편집 - 80번 포트 추가
```
HTTP|TCP|80|위치무관|Nginx 후 저장!
```

### AWS에서는 ipv4, ipv6 둘다 받는다.
* 점으로 구분된 기준은 ipv4 `0.0.0.0/0`
* 콜론으로 구분된 기준은 ipv6 `0.0.0.0/0, ::/0`

### 연결
EC2 -> Django(8000)
EC2 -> uWSGI(8000) -> Django(wsgi모듈)
EC2 -> Nginx(Nginx virtual server) <->(Unix Socket) uWSGI -> Django

* uWSGI를 소켓모드로 실행
```bash
/home/ubuntu/.pyenv/versions/runserver-test/bin/uwsgi \
--socket /tmp/app.sock \
--home /home/ubuntu/.pyenv/versions/runserver-test \
--chdir /srv/runserver-test/mysite \
--module mysite.wsgi \
--vacuum
```
* `/tmp/`에 `app.sock`이 생긴다.
* 서버가 끊어지면 `app.sock`이 사라진다.

* EC2 -> Nginx(Nginx Configuration이 필요/virtual server) ->(Unix socket) -> uWSGI -> Django
* nginx의 설정파일은 
```bash
cd /etc/nginx/sites-available
```
* `nginx`의 `default`파일이 존재
* nginx는 가상 서버라는 것을 만들어 동작함.
* 하나의 컴퓨터에서는 여러 도메인에 대한 접속을 처리 할 수 있다. 그것을 각각의 가상 서버에서 처리 하게 하는 것이 nginx다

## nginx default
* nginx는 시작시 모든 nginx sites-enabled 파일에 대해 검사를 한다.

```bash
# listten 80, 80번 포트에 대해서 응답을 받음, default_server는 도메인에 일치하지 않는(특정 가상서버를 가리키지 않을경우) 기본적으로 80번 포트가 응답 받는다.
listen 80 default_server;

# ipv6용
listen [::]:80 default_server;

# root에 /var/www/html 에서 index들을 찾음.
# nginx를 설치하면 /var/www/html에 자동으로 파일이 추가 됨.
root /var/www/html;
index index.html index.html ...

# location / 은 django의 root-url 을 말하고
# $url은 / 다음에 오는 문자열을 말하고 문자열과 매칭되는 파일이 있는지 검사 없으면 404에러 발생.
location / {
	try_files $uri $uri/
}
```

`vi /ect/nginx/sites-available/app`으로 설정파일 nginx의 설정파일을 만듬.
```bash
server {
        listen 80;
        server_name *.amazonaws.com;
        charset utf-8;
        client_max_body_size 128M;

        location / {
                uwsgi_pass      unix:///tmp/app.sock;
                include         uwsgi_params;
        }
}
```

### Socket
* 데이터를 교환하기 위한 통신방법

### OSI 7 Layer
* 우리가 사용하는 통신 계층은 7단계로 나뉘어져 있다.
* 1층 하드웨어가 단에서 통신을 하기 위해 쓰는것이 3층 IP 이 위에서 데이터의신뢰성을 따져서 전송하는 것이 4층 TCP이다.
* 어디로 통신하고 통신내용에 대해서 손실이 없을 거라는 것은 HTTP를 구성하는 하위 계층인 3,4 층에서 담당을 한다.

### Unix Domain Socket
> 파일 시스템을 통해서 소켓통신 방식으로 내부 프로세스 간의 통신하는 구조
> 로컬 프로세서와의 효율적 통신을 가능하게 함.
> 부하가 적다.
> OSI 7 Layer를 사용하지 않기에 빠르다.
* `unix///app.socket` 으로 사용
* 외부에서 데이터를 받을때는 어쩔수 없이 HTTP로 받지만 내부에서는 Unix Sokect방식을 사용하여 속도를 높인다.
* Nginx는 여러개의 가상 서버를 만들수 있다. 서비스를 한 컴퓨터에 10개를 만들고 그 10개중 한개의서버만 중단해야 한다.
* sites_available 동작할수 있는 모든 서버의 정보를 가짐
* sites_enabled는 실제 동작하고 싶은 서버만 링크를 검.

```
/etc/nginx/sites-available
		default,
		app
		
/etc/nginx/sites-enabled
		default는 삭제
		그러면 두개의 작동 가능한 가상 서버가 있지만
		그중 한개(default)는 무시됨.
		(app의 link)
		app
```
```bash
sudo ln -s ../sites-available/app app
sudo rm default
```
* 시스템에서 돌아가고 있는 nginx를 재시작 해야 한다.
하지만 502 Bad Gateway가 뜬다!
* log를 확인해보자 `cd /var/log/nginx/error.log`
`unix:///tmp/app.sock failed (13: Permission denied)` 에러가 뜸
app.socket에 nginx를 실행할 프로세서가 접근할 권한이 없다는 말!
`ps -aux | grep nginx` 를 사용하여 nginx라는 이름이 들어간 프로세서를 검색 한다.
nginx를 sudo apt-get으로 설치 했기때문에 root에 깔려 있음.
nginx라는 프로세서를 실행하는 유저는 www-data라는 유저고 기본적으로 만들어 져있다.
www-data가 app.sock에 접근할 권한이 없기 때문에. 에러가 남.
nginx설정을 열어 유저를 바꾸자
`sudo vi /etc/nginx/nginx.conf`

```
user www-data;
# ->
user ubuntu;
```
이후 nginx 재시작 `sudo systemctl restart nginx`

### 파일을 링크 하는 방법
* 심볼릭 링크, 하드링크
ln은 링크의 약어 -s는 심볼릭 
ln -s는 바로가기 수준의 복사를 하는 것.
링크를 삭제 해도 원본 파일은 삭제 되지 않는다.

하드 링크는 원본파일을 삭제해도 링크가 남아 있음 그래서 링크된 모든 파일이 삭제 되어야 정말 삭제 된다.

### ini
* 설정파일에 대한 표준 단순 텍스트 파일로 이루어져 있고
* name, value, section, comment로 이루어짐

### uWSGI 설정 파일 만들기
```bash
vi /srv/runserver-test/uwsgi.ini
```

* 설정 파일을 만들고 내용을 넣는다.

```bash
runserver-test Django프로젝트에 대한 uwsgi설정파일
[uwsgi]
chdir = /srv/runserver-test/mysite
module = mysite.wsgi
home = /home/ubuntu/.pyenv/versions/runserver-test

socket = /tmp/app.sock

master = true
vacuum = true
;logoto = /var/log/uwsgi/mysite/@(exec://date +%%Y-%%m-%%d).log
;log-reopen = true
```
* .ini 파일을 기준으로 실행

```bash
/home/ubuntu/.pyenv/versions/runserver-test/bin/uwsgi -i /srv/runserver-test/uwsgi.ini 
```

### pycham에서 설정후 deploy 하기
### Django uwsgi.ini nginx-app.conf 설정
* nginx-app.conf만들고 설정의 Editor의 FileTypes Nginx Config에 *.conf 추가
* ini4idea 플러그인 설치후 Editor의 ini에 *.ini, *.service

* uwsgi.ini만들고 서버의`/srv/runserver-test/uwsgi.ini`의 내용복사
* nginx-app.conf 에 서버의`/etc/nginx/sites-available/app` 파일 내용 복사

### SCP 프로토콜
* 로컬 호스트나 원격 호스트 간 또는 두개의 원격 호스트간에 컴퓨터 파일을 안전하게 전송하는 수단. ssh 프로토콜 기반이다.
scp 원본 사용자@호스트주소:디렉토리/대상파일
scp로 ssh 개인키를 써서 나의 프로젝트 경로를 우분투서버의 경로/srv/에 복사한다

scp -i 자동인증용 옵션을 사용하여 인증한다.
scp -r(리커시브 약자) 폴더를 복사 할때 항상 -r을 써야함
```bash
scp -i ~/.ssh/fc-7th.pem \
-r ~/projects/django/deploy/ec2-deploy \
ubuntu@ec2-13-124-48-143.ap-northeast-2.compute.amazonaws.com:/srv/ec2-deploy
```
하기전 이미 있던 파일은 지우는것도 좋다
```bash
ssh -i ~/.ssh/fc-7th.pem ubuntu@ec2-13-124-48-143.ap-northeast-2.compute.amazonaws.com rm -rf /srv/ec2-deploy
```

* 한땀한땀 치기 힘드므로 shell의 alias로 만들어 보자

```bash
# scp
EC2_USER="ubuntu"
EC2_DOMAIN="ec2-13-124-48-143.apnortheast-2.compute.amazonaws.com"
EC2_PEM="~/.ssh/fc-7th.pem"
EC2_DIR="~/projects/django/deploy/ec2-deploy"
 
alias con-ec2="ssh -i $EC2_PEM $EC2_USER@$EC2_DOMAIN"
alias copy-ec2="scp -i $EC2_PEM -r $EC2_DIR $EC2_USER@$EC2_DOMAIN:/srv"
alias deploy-ec2="con-ec2 rm -rf /srv/ec2-deploy; copy-ec2"
```

# .service를 만들어 백그라운드에 돌게 하자
* Service

```
# 직접 프로그램을 실행하는것이 아닌, (시스템 트레이에 들어 있듯이) 백그라운드에서 실행되고 있는 프로그램 
# service 는 윈도우의 시작 프로그램과 같다.
# service = daemon
# 프로세스를 demoniation -> 백그라운드에 서비스화 시킨다.
Nginx (default)
uWSGI
    1. /etc/systemd/system/uwsgi.service파일에 서비스 내용을 작성
    2. sudo systemctl enable uwsgi로 uwsgi.service를 서비스에 등록
    3. sudo systemctl daemon-reload로 systemctl에 등록된 서비스들의 내용이 바뀌었을 경우 적용
    4. sudo systemctl restart uwsgi로 uwsgi서비스를 재시작
```
* .config 에 uwsgi.service 파일 만듬

```bash
[Unit]
Description=EC2 Deploy uWSGI service
after=syslog.target

[Service]
ExecStart=/home/ubuntu/.pyenv/versions/fc-ec2-deploy/bin/uwsgi -i /srv/ec2-deploy/.config/uwsgi.ini

Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NorifyAccess=all

[Install]
WantedBy=multi-user.target
```
* 서버의시작프로그램 느낌의 폴더안에 .service복사

```bash
/srv sudo cp -f /srv/ec2-deploy/.config/uwsgi.service /etc/systemd/system/uwsgi.service # .service 파일 복사
/srv sudo systemctl enable uwsgi # uwsgi 적용
/srv sudo systemctl daemon-reload # 백그라운드 서비스에 리로드
/srv sudo systemctl restart uwsgi nginx # uwsgi 재시작 하면 에러남
# app.sock 파일의 권한이 없다.
# uwsgi.ini 파일에 app.sock 생성 권한을 주는 셋팅을 하자..
```

# 정리
### Nginx - uWSGI - Service
* Nginx (Wev server)
> 80번 포트 요청을 받아서 uWSGI와 서로 통신

* uWSGI (Web server Gateway Interface)
> Nginx로 부터 받아온 요청을 Django에서 처리한 후 돌려줌

* service
> 우리가 직접 실행한 프로그램이 아닌, 백드라운드에서 실행되고 있는 프로세스
> Nginx의 경우에는 기본적으로 서비스에 등록되어 있음.
> 하지만 uWSGI는 아님. 그래서 서비스를 작성 해줘야 한다.

* 직접 등록하는 Service의 경우
> `/etc/systemd/system/<서비스명>.service` 파일에 작성
* uWSGI의 Service에 대한 정보 파일
> `/etc/systemd/system/uWSGI.service` -> 이후 `sudo systemctl <멍령어> uwsgi` <- 이부분에 사용 가능

* `/etc/systemd/system/uwsgi.service`에서 실행 명령어

```bash
[Service]
ExecStart=/home/ubuntu/.pyenv/versions/fc-ec2-deploy2/bin/uwsgi -i /srv/ec2-deploy/.config/uwsgi.ini
```

### 경로 정리
EC2-Deploy 프로젝트
* 프로젝트 경로
> `/srv/ec2-deploy`
* 프로젝트 소스 루트 (파이썬 환경에서의 최상위 폴더, 파이썬 애플리케이션의 위치)
> `srv/ec2-deploy/app`
* 파이썬 가상환경
> `/home/ubuntu/.pyenv/versions/fc-ec2-deploy`
* uWSGI 프로그램의 위치
> `/home/ubuntu/.pyenv/versions/fc-ec2-deploy/bin/uwsgi`

### EC2-Deploy 프로젝트의 '배포용' 설정들
* Nginx 가상 서버 설정
> `/srv/ec2-deploy/.config/nginx-app.conf`
* uWSGI 설정
> `/srv/ec2-deploy/.cnfig/uwsgi.ini`
* uWSGI의 '서비스' 설정
> `/srv/ec2-deploy/.config/uwsgi.service`

### 순서
1. Django runserver (0:8000) 접속 확인
2. uwsgi에 직접 옵션 붙여서 실행
3. 옵션들을 정리한 ini파일을 사용해서 uwsgi --ini <ini파일경로>로 실행 후 접속 확인
4. uwsgi서비스를 등록후 접속 확인 파일을 `/etc/systemd/system/`폴더에 복사
   
```bash
sudo systemctl enable uwsgi
sudo systemctl daemon-reload
sudo systemctl restart uwsgi
```
-> `tmp/app.sock`파일을 리눅스 소켓으로 사용해서 uwsgi를 실행하도록 함

5. `/tmp/app.sock`파일과 통신하는 Nginx 가상서버 설정을 생성 및 링크

   5.1. 파일 복사
     `sudo cp -f /srv/ec2-deploy/.config/nginx-app.conf /etc/nginx/sites-available/nginx-app.conf`
     
   5.2 sites-enabled 폴더의 모든 링크 삭제
    `sudo rm -rf /etc/nginx/sites-enabled/*.*`
     
   5.3 복사한 파일의 링크를 sited-enable에 생성
    `sudo ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enalbed/nginx-app.conf`
     
   5.4. 재시작
   
```bash
sudo systemctl daemon-reload
sudo systemctl restart nginx
```