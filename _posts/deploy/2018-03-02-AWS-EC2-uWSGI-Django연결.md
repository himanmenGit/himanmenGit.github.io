---
layout: post
title: "AWS의 EC2에 UWSGI Django 연결"
categories:
  - Deploy
tags:
  - Deploy
---

# 인스턴스 생성 방법 및 설정
## EC2
* 로그인 후 `AWS` 서비스 창에서 `EC2` 검색 후 접속
* 인스턴스 시작
* `Ubuntu server 16.04 LTS` 선택 
* `t2.micro` (프리티어 사용가능) 선택
* 다음을 눌러 6단계 보안 그룹 구성으로 감
* 새 보안 그룹 생성 `EC2 Security Group` 설명: `EC2 Deploy Security Group`
* 검토 및 시작!
* 시작!
* 키페어 선택 

## 키페어
암호화 관련해서 공개키 암호화 기법. 개인키 공개키가 있어 자신의 개인키를 이용해 인증 하면 특정 사용자라는걸 상대에게 알려 줄수 있다.
`AWS`에서는 만든적이 없다.
`AWS`자체에 개인키 공유키가 있다. 키페어를 만드는 순간 개인키 공개키를 다 준다. 그순간이 마지막! 처음에 한번 보여주고 절대 보여 주지 않는다.

* 새 키 페어 생성
* 키 페어 이름 `fc-7th`
* 키 페어 다운로드 `fc-7th.pem`
* 해당 파일을 받은 폴더로 터미널로 이동후 `~/.ssh/`로 이동
* `mv fc-7th.pem ~/.ssh/` 이 개인키 파일을 어디에도 노출이 되어선 안된다.
* 인스턴스 시작!

## 예상 요금 알림 받기
* `AWS`키를 `Git`에 넣어서 결제가 되는 경우가 있다.
* 결제 알림 받기 체크 후 예상 요금 알림 받기 (새로운 예산 기능)
* 예산 작성
* 이름 - 프리티어, 예산 금액 - $1.00 , 다음 경우에 알림 - 실제 비용이 > 100 % 이메일 주소는 쉼표로 구분!
* 작성 !
* 하나더 만들기 
* 예산 작성 - 진짜 안되는 비용 $10.00 실제 비용이 > 100% - 작성!
* 메일 잘 확인 하기!!

## 다시 EC2
* `EC2` 다시 가보면 실행 중인 인스턴스가 생성됨! 인스턴스 상태는 `running`
* 인스턴스 Name `EC2 Deploy`

## 보안그룹
* `EC2` 인스턴스 설명에 보안그룹 인바운드 규칙 보기
* 22번포트(ssh프로토콜)에 대해서 `tcp`로 `0.0.0.0/0` 을 헝용함 
* `SSH`는 네트워크 상의 다른 컴퓨터에 로그인하거나 원격 시스템에서 명령을 실행하고 다른 시스템으로 파일을 복사 할 수 있도록 해주는 프로토콜 기본적으로는 `22`번 포트를 사용 한다.
* 기본 보안그룹에 `22`번 포트가 열려 있는 상태로 만들어 진다
* `SSH`를 이용하여 접근하는건 가능하지만 브라우저로 접근할수는 없다
* 브라우저로 접근하는 포트는 `80`번 이기 때문이다.

* `퍼블릭(public)DNS`로 접근가능하다. 하지만 인스턴스가 중단 됬거나 다시 켜지면 바뀔 수 있다.
* `퍼블릭DNS` 복사 

```
ssh -i(identity file) <공개키 파일경로.pem> user_name@public_dns_name`
```
* 사용자 이름은 설정 하지 않았다 
* `EC2`는 기본적으로 `amazon linux`를 사용 한다.
* 서버주소 `northeast-2` 인지 확인

* 연결방법 
* `ssh -i ~/.ssh/fc-7th.prem ubuntu@public_dns_name` 하고 yes를 하면 `bad permissions`이 난다.

* 파일의 권한은 숫자 3개로 나타남
* `0664` - 파일의 권한이 1소유자 2그룹 3에브리원 
* 왼쪽부터 `rwx` 각각 이진수 1자리 수고 `r읽기`, `w쓰기`, `x실행` 권한
* 하지만 기본적으로 원하는 권한은 400을 원한다. 소유자만 읽을수 있는 권한. 그래서 개인키의 권한을 `400(r--/---/---)`으로 바꾼다
* `chmod 400 ~/.ssh/fc-7th.pem`
* 다시 접속하면 `welcome to ubuntu` 가 뜬당!

# EC2 Ubunut 환경 python&django 설정하기
1. 패키지 관리자가 옛날 버전이라 apt를 업데이트 
`sudo apt-get update` 
2. 기존에 깔려 있던 패키지도 업데이트 
`sudo apt-get dist-upgrade`
3. `Keep the local version currently installed` 선택
4. pyenv Common Build problems 해결 
`sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev`
5. `pyenv-installer`를 이용해 설치 
```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```
6. pyenv 설정 텍스트 복사 우분투는 PATH가 다르기 때문에 로컬설정과 다름
```
export PATH="/home/ubuntu/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
7. zsh 설치 
`sudo apt-get install zsh`
6. ohmy zsh 설치 
`curl -L http://install.ohmyz.sh | sh`
7. 기본셸 zsh로 변경 ubuntu 유저에 대해서변경 
```
sudo chsh ubuntu -s- `which zsh`
```
8. 서버를 나갔다가 다시 들어가면 `zsh`로 바뀜 
9. 이제 zhs 설정을 함 
`vi ~/.zshrc`
두번째 줄 주석 해제 Shift-g를 통해 마지막 줄로 가서 위에서 복사 해놓은 설정을 붙여 넣기 그런다음 서버 재접속이나 `source ~/.zshrc`로 설정 적용.

10. `/srv`로 가서 프로젝트 폴더를 만듬 그런데 `/srv` 폴더는 root 권한임 그래서 `ubuntu`계정 권한으로 바꿔 줘야함 
> `sudo chown -R ubuntu:ubuntu srv`
> root/srv -> cd / srv/ 에 pyenv install 3.6.4 설치
> /srv /var 디렉터리에 서비스를 많이 넣어 놓는다.
> /srv 서비스 디렉토리로 주로 인터넷 관련 파일이 위치.l
> /var 운영도중 파일의 크기가 변하는 요소를 담는 디렉토리. 보통 로그파일을 담음. 
> Home/srv 가 아님. root/srv/임 cd /로 감.

```
sudo chown -R ubuntu:ubuntu srv

cd /srv
mkdir runserver-test
cd runserver-test
pyenv install 3.6.4
```
11. 가상 환경을 만들어줌
```
pyenv virtualenv 3.6.4 runserver-test
pyenv local runserver-test
```

12. 이후 장고 설치 및 프로젝트 생성후 `runserver` 확인
```
pip install django
django-admin startproject mysite
cd mysite
./manage.py runserver 0:8000 
```
13. 브라우저에 접속 ec2-13-124-253-19.ap-northeast-2.compute.amazonaws.com:8000
하지만 연결 안됨. 

14. EC2안의 보안그룹안에 두개가 있는데 우리가 만든 EC2 Security Gropu를 선택 -> 인바운드로 가서 -> 편집 -> 규칙 추가 -> 사용자 지정 TCP|프로토콜 TCP|포트범위 8000|소스 위치무관|설명 Django runserver 로 추가, 저장한다. 이후 다시 접속 allowed_host 가 비어 있어서 에러가 남. `Django`의 `DEBUG` 가 `TRUE` 이면  `allowd_host`는 `['localhost', '127.0.0.1', '[::1]']`을 추가함. 에러가 나지 않도록 `mysite/settings.py`에 
```
ALLOWED_HOST [ 
    '.amazonaws.com', 
]
```
을 넣어 준다.
15. 이후 ./manage.py runserver 0:8000 으로 서버 실행 0:8000을 꼭 넣어야함.

16. 하지만 실제 서버에서는 runserver를 쓰지 않는다.

# 지금까지 한 시스템의 구성

Browser(Client) -> runserver -> Django <==> PostgreSQL

실제 서버에서는
Browser(Client) -> 
	# AWS의 설정
	-> (Security Group) -> EC2(Port 80)
	
	# EC22 내부에서의 설정 
	-> Nginx(WebServer) -> uWSGI(Web server gateway interface) -> Django
를 구축 해야 함!.

* uWSGI는 프로그램 이름이고 WSGI는 웹 서버 게이트웨이 인터페이스
> 웹서버와 웹 애플리케이션의 인터페이스를 위한 파이선 프레임워크
> 웹서버와 웹 애플리케이션의 연결을 만들어 주는 것. 
> 예전 프레임워크들은 웹서버마다 규격이 달라서 웹 애플리케이션이 웹서버를 선택하는데 제약이 있었음
> 하지만 WSGI는 low-level로 만들어 일괄적인 요청으로 바꿔서 어떤 규격을 사용하던지 모두 연결이 가능하도록 한다.

* 정적 파일은 Django 까지 가지 않고 들어온 요청에 대해서 웹 서버가 바로 처리 해주는게 빠름. Nginx에서 다시 돌려준다.
* 하지만 로그인, 로그인된 페이지 렌더링 경우는 uWSGI를 통해 Django에서 처리 해 준다. 

## nginx
* 그래서 Nginx를 설치 해보자
* apt에 등록되어 잇는 nginx는 최신 버전이 아니다 버전에 맞게 깔자.
```
add-apt-repository ppa:nginx/stable
apt-get update
apt-get install nginx
nginx -v
# 2018/03/02
# nginx version: nginx/1.12.2 
```

## uWSGI
* uwsgi는 파이썬 패키지 안에서 돌아감. 그래서 가상 환경 안에서 설치.
```
pip install uwsgi
```

## 서버 테스트
EC2 -> Django(8000)
EC2 -> uWSGI(8000) -> Django(wsgi모듈)
EC2 -> Nginx(Nginx virtual server) <->(Unix Socket) uWSGI -> Django

## EC2 -> runserver(8000) -> Django
```
./manage.py runserver 0:8000
```

## EC2 -> uWSGI(8000) -> Django
* `--http :(port)` - 어떤 프로토콜을 쓸 것인가?
* `--home /home/ubuntu/.pyenv/versions/runserver-test` virtualenv경로
* `--chdir /srv/runserver-test/mysite` django 프로젝트 루트 경로
* `--module mysite.wsgi` 은 wsgi 모듈 이름을 적는 곳
* `runserver-test`의 모듈인 `mysite(config)`의 `wsgi.py` 를 모듈로 한다.
```
uwsgi \
--http :8000 \
> --home /home/ubuntu/.pyenv/versions/runserver-test \ 
> --chdir /srv/runserver-test/mysite \
> --module mysite.wsgi
```