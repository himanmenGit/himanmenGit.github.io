---
layout: post
title: "ec2에서 django와 channels를 이용하여 웹소켓 적용1"
categories:
  - Django
tags:
  - Django
---

{% raw %}

# `django channels on ec2`
`django channels`를 `ec2`에 올려 노티 기능을 만들어 보기 위한 프로젝트

# 프로젝트 셋팅
1. `mkdir django-channels-on-ec2`
2. `cd django-channels-on-ec2`
3. `git init`
4. `touch .gitignore` <https://www.gitignore.io/>에서 `git,linux,macos,python,django,pycharm+all` 검색후 복사      
        1. `.secrets`를 `.gitignore`에 추가        
5. `pyenv virtualenv 3.6.5 ec2`
6. `pyenv local ec2`
7. `pip install django`
8. `django-admin startproject config`
9. `mv config app`
10. `pip freeze > requirements.txt`
11. `settings.py` 수정
    ```python
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.path.dirname(BASE_DIR)
    
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    
    SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
    SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')
    
    secrets = json.loads(open(SECRETS_BASE, 'rt').read())
    
    SECRET_KEY = secrets['SECRET_KEY']
    
    ALLOWED_HOSTS = [
        '.amazonaws.com',
    ]
    ```    
12. `.secret/base.json` 파일 추가       
    ```json
    {
      "SECRET_KEY": "<django secret key>"
    }
    ```  

13. `git hub` 설정         
        1. `git hub` -> `new repository` -> `django-channels-on-ec2`        
        2. `git remote add origin git@github.com:himanmenGit/django-channels-on-ec2.git`        
        3. `git push -u origin master`
14. `git add -A && git commit -m 'first commit'`

# ec2 셋팅
1. `ec2 instance 생성`
2. `ubuntu 16.04` 선택
3. `t2.micro` 프리티어 선택
4. 다음,다음,다음 6단계 보안 그룹 구성
5. 새 보안 그룹 생성       
        1. 보안 그룹 이름 - `EC2 Security Group`  
        2. 보안 그룹 설명 - `Ec2 Deploy Security Group`   
        3. 소스 - `내 IP`, 설명 - `ssh`  
        4. 규칙 추가 - `사용자 지정 TCP`, 포트 번호 `8000`, 소스 `내 IP`, 설명 `web`
6. 검토 및 시작 - 시작
7. 키페어를 저장 후 인스턴스 시작 (`permission` 에러 나면 `chmod 400 <key pair>.pem`)
8.  `'ssh -i <key path>ex)~/key.pem ubuntu@<ec2 ip4 퍼블릭 IP>',`
9. `YES` - `Welcome to Ubuntu 16.04`
10. `linux setting`     
        1. `sudo vi /etc/default/locale`    
        2. `locale` 수정 후 재 접속      
    ```
    LC_CTYPE="en_US.UTF-8"
    LC_ALL="en_US.UTF-8"
    LANG="en_US.UTF-8"
    ```   
                
11. `linux update`      
        1. `sudo apt-get update`    
        2. `sudo apt-get dist upgrade` 마지막에 엔터       
        3. `sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev`        
12. `pyenv` 설치      
        1. `curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`          
        2. `vi ~/.bash_profile`에 마지막 설정 복사      
        3. `source ~/.bash_profile`적용       
        4. `pyenv` 명령 확인              
    ```
    export PATH="/home/ubuntu/.pyenv/bin:$PATH"            
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ``` 
                
13. `git`설치      
        1. `sudo apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev`      
        2. `git` 확인
        
14. `srv`폴더 유저 변경       
        1. `sudo chown -R ubuntu:ubuntu /srv/`
15. 프로젝트 `clone` 및 `pyenv` 설정   
        1. `git clone <django-channels-on-ec2 repository url>.git`      
        2. `cd django-channels-on-ec2`      
        3. `pyenv install 3.6.5`        
        4. `pyenv virtualenv 3.6.5 ec2`     
        5. `pyenv local ec2`        
16. `.secrets`폴더 업로드        
        1. `scp -ri <key_path>.pem .secrets ubuntu@<public ipv4>:/srv/django-channels-on-ec2/` 
17. `runserver`     
        1. `pip install -r requirements.txt`        
        2. `./manage.py runserver 0:8000`       
18. 브라우저 확인     
        1. 브라우저에 `<public dns주소>:8000`으로 접속         
        2. 로켓 발싸!

19. `redis-server`설치
`redis-channel-layer`를 사용하려면 필요.
`sudo apt-get install redis-server`

20. `tmux` 설치
`sudo apt-get install tmux`

21. `tmux` 키고 `redis-server` 켬
    1. `tmux new`
    2. `(ctrl+b) + %`후 창이 나뉘어 지면 `(ctrl+b) + q`를 사용하여 창 이동후
    3. `redis-server` 작동시킴  

![](/assets/django/2019-01-07/django-channels-tmux.png)

# chat 설정
1. `django-admin startapp chat`
2. `model`
    ```python
    from django.db import models
    
    
    class Room(models.Model):
        name = models.CharField(verbose_name='채팅방 이름', max_length=255)
        group_name = models.SlugField(verbose_name='채팅방 그룹 이름', unique=True)
    
        def __str__(self):
            return self.name
    
    
    class RoomMessage(models.Model):
        room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
        message = models.TextField(verbose_name='메세지')
        created = models.DateTimeField(verbose_name='생성 날짜', auto_now_add=True, db_index=True)
    
        def __str__(self):
            return self.message
    
        def get_created(self):
            return self.created.strftime('%p %I:%M')
    ```

3. `routing.py`
    ```python
    from django.urls import path
    
    from . import consumers
    
    websocket_urlpatterns = [
        path('ws/main/', consumers.ChatConsumer),
    ]
    ```
    
4. `consumers.py`
    ```python
    import json
    
    from channels.generic.websocket import AsyncJsonWebsocketConsumer
    
    
    class ChatConsumer(AsyncJsonWebsocketConsumer):
        async def connect(self):
            self.noti_group_name = 'main'
    
            await self.channel_layer.group_add(
                self.noti_group_name,
                self.channel_name
            )
    
            await self.accept()
    
        async def disconnect(self, code):
            await self.channel_layer.group_discard(
                self.noti_group_name,
                self.channel_name
            )
    
        async def chat_message(self, event):
            message = event['message']
            created = event['created']
            await self.send(text_data=json.dumps({
                'message': message,
                'created': created
            }))
    
    ```

5. `config`에 `asgi.py` 추가
    ```python
    """    
    ASGI entrypoint. Configures Django and then runs the application
    defined in the ASGI_APPLICATION setting.
    """
    
    import os
    import django
    from channels.routing import get_default_application
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    application = get_default_application()
    ```
6. `config` `routing.py`추가
    ```python
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    from chat.routing import websocket_urlpatterns
    
    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    })
    
    ``` 

7. `templatestags`폴더 추가 및 코드 추가       
    ```
    # chat app
    ├── templatetags
    │   ├── __init__.py
    │   └── chat_extra_tags.py
    ```
    
    ```python
    # chat_extra_tags.py
    from django import template
    from chat.models import Room
    
    register = template.Library()
    
    
    @register.simple_tag
    def get_main_message():
        room = Room.objects.get(group_name='main')
        old_messages = room.messages.order_by('-created')[:50]
        return old_messages
    
    ```
    
    ```python
    # settings.py
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # 추가
                'templates'
            ],
       ...
    
    ```

8. `settings.py`
    ```python
    INSTALLED_APPS = [
        'channels',
    
        ...
    
        'chat',
    ]
    ...
    ASGI_APPLICATION = 'config.routing.application'
    
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            },
        },
    }
    
    ```

9. `channels`, `channels-redis`설치       
        1. `pip install channels`       
        2. `pip install channels-redis`     
        3. `pip freeze > requirements.txt`      
        4. `git commit and push`
        
# ec2 에서 pull받아 작업
1. `git pull origin master`
2. `pip install -r requirements.txt`
3. `./manage.py makemigraions && migrate` 실행후 다음 메시지로 변경
    ```shell
    System check identified no issues (0 silenced).
    January 04, 2019 - 09:00:48
    Django version 2.1.4, using settings 'config.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
    에서 
    
    System check identified no issues (0 silenced).
    January 04, 2019 - 08:59:23
    Django version 2.1.4, using settings 'config.settings'
    # 아래 부분에 development server 가 ASGI로 바뀜 
    Starting ASGI/Channels version 2.1.6 development server at http://0:8000/
    Quit the server with CONTROL-C.
    ```

# view에 index.html 추가
```python
#chat/views.py
from django.views.generic import TemplateView

from chat.models import Room


class Home(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # 단순히 시작히 룸을 만들기 위한 장치
        Room.objects.get_or_create(name='노티룸', group_name='main')
        return super().get(request, *args, **kwargs)
```

```html
# index.html 
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Room</title>
</head>

<body>
<textarea id="chat-log" cols="100" rows="20"></textarea><br/>
</body>
{% load chat_extra_tags %}
<script src="//cdnjs.cloudflare.com/ajax/libs/reconnecting-websocket/1.0.0/reconnecting-websocket.min.js"></script>
<script>
    {% get_main_message as old_messages %}

    let chat_log = document.querySelector("#chat-log");

    (function () {
        let messages = [{% for message in old_messages %}'{{ message }}',{% endfor %}];        
        let creaties = [{% for message in old_messages %}'{{ message.get_created }}',{% endfor %}];
        for (i = messages.length; i > 0; i--) {
            chat_log.value += ('message:[' + messages[i - 1] +']-- created:[' + creaties[i - 1] + ']\n');
        }
    })();

    let chatSocket = new ReconnectingWebSocket('ws://' + window.location.host + '/ws/main/');

    chatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        let message = data['message'];
        let created = data['created'];
        chat_log.value += ('message:[' + message +']-- created:[' + created + ']\n');
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly', e);
    };
</script>

</html>

```

서버에서 `redis-server`가 켜진 상태로 `runserver`를 해서 접속하면 
```shell
HTTP GET / 200 
WebSocket DISCONNECT /ws/main/ 
WebSocket HANDSHAKING /ws/main/ 
WebSocket CONNECT /ws/main/ 
```
이런 로그가 나오면 성공.

# api를 하나 열어서 메세지를 웹 소켓으로 전달          
1. `django-rest-framework`설치 `pip install djangorestframework`  

2. `chat/views.py`에 `API` 추가
    ```python
    from rest_framework.response import Response
    from rest_framework.views import APIView
    
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    
    ...
    
    class Notification(APIView):
        def post(self, request, *args, **kwargs):
            room = Room.objects.get(group_name='main')
            message = room.messages.create(message=request.data.get('message'))
    
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'main',
                {
                    'type': 'chat_message',
                    'message': str(message),
                    'created': message.created.strftime('%p %I:%M')
                }
            )
    
            return Response({'status': 200, 'meesage': '{} send success'.format(message)})
    
    
    ```
3. `urls.py`에 `api`용 `url`추가
    ```python
    # urls.py
    ...
    urlpatterns = [
        ...
        path('notification/', Notification.as_view())
    ]
                   
    ```
2. `pip freeze > requirements.txt`      
4. `git commit and push`

# 확인
1. 서버에 가서 `git pull origin master`를 한후 
2. `pip install -r requirements.txt`로 `drf`를 설치 한다음 
3. 서버를 다시 실행 `./manage.py runserver 0:8000`
4. `ec2`의 `public dns`의 `url`을 기준으로한 `api`주소를 `requests`를 이용하여 `post`       
    ```python
    import requests
    res = requests.post('http://123.456.789.0.ap-northeast-2.compute.amazonaws.com:8000/notification/', data={'message':'hello'})
    print(res)
    >>> <Response [200]>
    print(res.content)
    >>> b'{"status":200,"meesage":"hello send success"}'
    ```
    
### `localhost:8000`
![](/assets/django/2019-01-07/django-channels-local.png)

### `aws public dns`
![](/assets/django/2019-01-07/django-channels-production.png)


다음편 에서는 `ssl`을 통해 웹소켓을 `wss`로 암호화하여 통신하는 법에 대해 알아 보자.


## 참고 사이트
[victolee](https://victorydntmd.tistory.com/265)님의 블로그      
[darkblank](https://darkblank.github.io/development/Django-Channels/)님의 블로그     
[readthedocs](https://channels.readthedocs.io/en/latest/)

{% endraw %}