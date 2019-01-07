---
layout: post
title: "ec2에서 django와 channels를 이용하여 웹소켓 적용2"
categories:
  - Django
tags:
  - Django
---

{% raw %}


전 포스트에서 단순히 웹소켓을 적용하고 채팅기반 모델에서 노티피케이션 기능을 하게 만들어 놓았다.

`nginx`를 앞에 두고 웹서버와 소켓서버를 같이 서빙하게 해보자.

# aws 셋팅
`ec2` -> `보안 그룹` -> `Ec2 Security Group` -> `인바운드` -> `편집` -> `규칙추가` ->  `HTTP/TCP/80/내 IP/nginx`

# ec2 셋팅
`nginx` 설치       
```
add-apt-repository ppa:nginx/stable
apt-get update
apt-get install nginx
nginx -v
nginx version: nginx/1.14.1 
```
이후 브라우저에서 80포트로 접속      
![](/assets/django/2019-01-07/django-channels-welcome-nginx.png)

# nginx 설정
`nginx`의 `default`설정은 버리고 `django-channels`의 런서버와 `daphne`로 서빙되게 하는 설정 추가

1. 새로운 `nginx`
프로젝트의 최상위 루트에 `server_info`라는 폴더를 만든후 `nginx`폴더 안에 `app`이라는 파일을 만듬      
    ```
    # server_info/nginx/app
    server {
        listen 80;
        server_name *.amazonaws.com;
    
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    
        location /ws {
            proxy_pass http://127.0.0.1:8001;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
    
    }
    ```
커밋하고 `ec2`에서 `git pull origin master`

2. `/etc/nginx/sites-enables/default`는 삭제       
    `sudo rm /etc/nginx/sites-enables/default/`

3. `/etc/nginx/sites-available/app`에 `server_info/nginx/app`파일 복사후 `/etc/nginx/sites-enabled/`에 심볼릭 링크 생성        
    ```
    sudo cp /srv/django-channels-on-ec2/server_info/nginx/app /etc/nginx/sites-available/app
    sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app
    ```

4. `nginx` 재시작
    `sudo service nginx restart`


# daphne 켜기     
`nginx` 와 `channels`를 사용하기 위해서는 `ws`를 `nginx`에서 `daphne`로 서빙해 주어야 한다.       
```
# /srv/django-channels-on-ec2/app
daphne -b 0.0.0.0 -p 8001 config.asgi:application
```
을 실행 시킨후 `public dns`주소로 접속 하면 아까 장고로 돌아가는 화면을 볼 수 있다.

다시 `API`를 호출하여 실행 여부를 확인하자.


# ssl설정
`route53`으로 적용한 도메인에 `ssl`을 적용하여 `https`로 접속이 되도록 해보자.
`route53`으로 도메인을 적용 하는 방법은 [날개의 노트](http://wingsnote.com/57)님 블로그에 정리가 잘 되어 있다.
  
도메인으로 잘 접속이 된다면, `ec2`로 접속하여 `ssl`을 적용 하여 보자
`certbot`을 이용하면 `ssl`발급과 `nginx`설정 까지 다 해준다.

1. `ec2`의 인바운드 옵션을 정리        
![](/assets/django/2019-01-07/django-channels-inbound.png)

2. `certbot` 설치     
    ```
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt update
    sudo apt install python-certbot-nginx
    ```

3. 도메인에 `ssl 인증서`를 발급 받자        
    ```
    sudo certbot --nginx -d example.com -d www.example.com
    ```
이후 질문들에는 `A or Y`로 넘어가고 `nginx`에서의 `https` `redirect`설정 부분은 (2)로 넘어가 주면 된다.

4. `nginx` 재시작      
    `sudo service nginx restart`


6. `index.html`수정       
    ```javascript
    let chatSocket = new ReconnectingWebSocket('ws://' + window.location.host + '/ws/main/');
    ```
    을
    ```javascript
    let chatSocket = new ReconnectingWebSocket('wss://' + window.location.host + '/ws/main/');
    ```
    으로 `ws` -> `wss`로 바뀌었다.
    
`runserver` 서버를 재시작후 브라우저의 시크릿 탭을 열어 도메인을 접속하면 `https`로 리다이렉트 되는것을 볼 수 있다.

### himanmen.com
![](/assets/django/2019-01-07/django-channels-result1.png)

### www.himanmen.com
![](/assets/django/2019-01-07/django-channels-result2.png)



## 배운점
1. `ec2`의 `public dns`에는 외부 인증서로(?) `https`를 적용 할 수 없다. (확실치 않음)
2. 브라우저 테스트는 시크릿탭으로 해보자.. 크롬 브라우저 캐싱 기능덕분에 시간을 많이 소모 했다. `http` -> `https` -> `http` 
3. `ec2`의 보안 그룹에 대해 약간더 알게 되었다. `80`번 포트가 열려 있어도 `https`로 접속을 하게되면 `443`도 열려 있어야 한다. 당연한 건가..
4. `route53`을 새로이 적용 해 보면서 오리지날 `ec2`에는 로드 밸런서가 없어서 `alias`가 적용이 안되며 `public ip`로 해야 한다는 것을 알았다. 


## 참고 사이트
[허진수](https://blog.koriel.kr/aws-lighstsailro-ghost-beulrogeu-unyeonghagi-2/)님의 블로그에 SSL 인증서 발급 부분      
[readthedocs](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)      
[daphne](https://github.com/django/daphne)      
[날개의 노트](http://wingsnote.com/57)님 블로그      

{% endraw %}