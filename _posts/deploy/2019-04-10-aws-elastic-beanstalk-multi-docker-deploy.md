---
layout: post
title: "Elastic Beanstalk에 Docker-compose를 이용하여 Django 배포"
categories:
  - Deploy
tags:
  - Deploy
  - Docker
---

# aws elastic beanstalk multi docker deploy 

### 환경
`python 3.6.7`
`docker 18.09.4`
`docker-compose 1.23.2`
`eb cli 3.15. 0`

### 링크
[eb-docker-compose-ecs](https://github.com/himanmenGit/docker-practice/tree/master/eb-docker-compose-ecs)

### Docker CE 설치
[ec2-on-docker](https://himanmengit.github.io/deploy/2019/04/02/ec2-on-docker(django-nginx-uwsgi-supervisor).html)의 설치 과정을 그대로

### Docker Compose 설치
[ec2-on-docker-compose](https://himanmengit.github.io/deploy/2019/04/04/ec2-on-docker-compose(django-nginx-uwsgi-postgres).html)

### 프로젝트 환경
[ec2-on-docker-compose](https://himanmengit.github.io/deploy/2019/04/04/ec2-on-docker-compose(django-nginx-uwsgi-postgres).html)에서 조금 수정 됨.

nginx에서 uwsgi의 socket위치를 수정

```nginx
# nginx-app.conf
upstream uwsgi {
    server unix:/tmp/apps.sock;
}

```

uwsgi에서 socket위치를 수정

```ini
# uwsgi.ini
[uwsgi]
socket = /tmp/apps.sock
...

```

nginx/web 을 build하여 DockerHub로 푸시한다음 docker-compose 수정

Docker-compose.yml 파일에서 볼륨 수정

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
    image: <docker hub username>/<dockerhub container tag>
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./web:/tmp
      - ./log:/var/log/nginx
    depends_on:
      - web

  web:
    container_name: web
    image: <docker hub username>/<dockerhub container tag>
    restart: always
    command: uwsgi --ini uwsgi.ini
    volumes:
      - ./web:/tmp
      - ./log:/var/log/uwsgi
    depends_on:
      - db
volumes:
  pgdata:


```

### Dokcerrun.aws.json
eb에서는 multi container를 사용하기위해 Dockerrun.aws.json파일을 사용해야 한다.
ocker-compose.yml 파일을 편하게 Dockerrun.aws.json으로 만들어 주는 서드파티를 이용하자.

```bash
$ pip install container-transform
$ container-transform --version
1.1.5
```

docker-compose.yml파일이 있는 곳에서 빌드
```bash
container-transform --input-type compose --output-type ecs docker-compose.yml > Dockerrun.aws.json
```

이런 에러가 뜰 것이다
```bash
Container web is missing required parameter "memory".
Container nginx is missing required parameter "memory".
Container db is missing required parameter "memory".
```

docker-compose.yml에서 
`mem_limit: XXX` 으로 수정해주어도 되지만 Dockerrun.aws.json 파일에 바로 수정 하자.

### 수정 하자
주석을 참고하여 수정 해주세용..

```json
{   
    "AWSEBDockerrunVersion": "2", // 추가 1,2 버전중 2번을 꼭 사용 해야 함.
    "containerDefinitions": [
        {   
            "environment": [
                {
                    "name": "POSTGRES_PASSWORD",
                    "value": "password123"
                }
            ],
            "essential": true,
            "image": "postgres",
            "mountPoints": [
                {
                    "containerPath": "/var/lib/postgresql/data/",
                    "sourceVolume": "Pgdata"
                }
            ],
            "name": "db",
            "memory":128,
            "portMappings": [
                {
                    "containerPort": 5432,
                    "hostPort": 5432
                }
            ]
        },
        {
            // docker-compose.yml의 dependencies를 표현
            "links": [  
              "web"
            ],
            "essential": true,
            "image": "himanmen/nginx",
            "mountPoints": [
                {
                    "containerPath": "/tmp",
                    "sourceVolume": "_Web"
                },
                {
                    "containerPath": "/var/log/nginx",
                    "sourceVolume": "_Log"
                }
            ],
            "name": "nginx",
            "memory":128,
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80
                }
            ]
        },
        {
            // docker-compose.yml의 dependencies를 표현
            "links": [  
              "db"
            ],
            "command": [
                "uwsgi",
                "--ini",
                "uwsgi.ini"
            ],
            "essential": true,
            "image": "himanmen/web",
            "mountPoints": [
                {
                    "containerPath": "/tmp",
                    "sourceVolume": "_Web"
                },
                {
                    "containerPath": "/var/log/uwsgi",
                    "sourceVolume": "_Log"
                }
            ],
            "name": "web",
            "memory":128
        }
    ],
    "family": "",
    "volumes": [
        {
            "host": {
                "sourcePath": "pgdata"
            },
            "name": "Pgdata"
        },
        {
            "host": {
                "sourcePath": "web" // 앞의 ./를 지워줌
            },
            "name": "_Web"
        },
        {
            "host": {
                "sourcePath": "log" // 앞의 ./를 지워줌
            },
            "name": "_Log"
        }
    ]
}

```

설정을 다 했으면 `eb init`!

다른점은 Docker설정시 MultiContainer를 물어 보는 것.

eb설정을 끝내고 `eb local run`을 해보자 그리고 `localhost:80` 접속! 잘 뜬다면 성공 이겠죵

이제 eb create로 elastick beanstalk앱을 만들고 배포! 이후 eb dns로 접속하여 확인

추가로 ecs에 컨테이너 들이 있는지 한번 확인 해보쟝.
