---
layout: post
title: "Elastic Beanstalk에 Docker를 이용하여 Django 배포"
categories:
  - Deploy
tags:
  - Deploy
  - Docker
---

# aws elastic beanstalk docker deploy 

### 환경
`python 3.6.7`
`docker 18.09.4`
`eb cli 3.15. 0`

### Docker CE 설치
[ec2-on-docker](https://himanmengit.github.io/deploy/2019/04/02/ec2-on-docker(django-nginx-uwsgi-supervisor).html)의 설치 과정을 그대로

### 프로젝트 환경
[ec2-on-docker](https://himanmengit.github.io/deploy/2019/04/02/ec2-on-docker(django-nginx-uwsgi-supervisor).html)의 환경과 동일

`nginx-app.conf`의 `server_name`에 `*.elasticbeanstalk.com`추가
```nginx
server_name  *.elasticbeanstalk.com *.amazonaws.com localhost;
```
그외 프로젝트 및 docker의 이름은 eb-docker로 함.

### Elastic beanstalk cli

```bash
# init
$ eb init

# region을 지정
Select a default region
1) us-east-1 : US East (N. Virginia)
2) us-west-1 : US West (N. California)
3) us-west-2 : US West (Oregon)
4) eu-west-1 : EU (Ireland)
5) eu-central-1 : EU (Frankfurt)
6) ap-south-1 : Asia Pacific (Mumbai)
7) ap-southeast-1 : Asia Pacific (Singapore)
8) ap-southeast-2 : Asia Pacific (Sydney)
9) ap-northeast-1 : Asia Pacific (Tokyo)
10) ap-northeast-2 : Asia Pacific (Seoul)
11) sa-east-1 : South America (Sao Paulo)
12) cn-north-1 : China (Beijing)
13) us-east-2 : US East (Ohio)
14) ca-central-1 : Canada (Central)
15) eu-west-2 : EU (London)
(default is 3): 10

# Application 생성
Enter Application Name
(default is "eb-docker"): eb-docker
Application eb-docker has been created.

# Docker 를 사용 하자
It appears you are using Docker. Is this correct?
(Y/n): Y

# SSH로 접근을 할 수 있게 한다.
Cannot setup CodeCommit because there is no Source Control setup, continuing with initialization
Do you want to set up SSH for your instances?
(Y/n):

# 사용중인 KeyPair를 쓰거나 만들자
Select a keypair.
1) oh-my-keypair
2) [ Create new KeyPair ]
(default is 1): []
```
여기까지 진행하면 프로젝트 폴더에

.elasticbeanstalk 폴더와 config.yml이 생겼을 것이고

```yml
# .elasticbeanstalk/config.yml

branch-defaults:
  default:
    environment: null
    group_suffix: null
global:
  application_name: eb-docker
  branch: null
  default_ec2_keyname: oh-my-keypair
  default_platform: Docker 18.06.1-ce
  default_region: ap-northeast-2
  include_git_submodules: true
  instance_profile: null
  platform_name: null
  platform_version: null
  profile: null
  repository: null
  sc: null
  workspace_type: Application
```

.gitignore에 해당 폴더들을 git에서 제외 시키는 설정이 추가 될 것이다.

```
# .gitignore

# Elastic Beanstalk Files
.elasticbeanstalk/*
!.elasticbeanstalk/*.cfg.yml
!.elasticbeanstalk/*.global.yml
```

### create

설정을 만든후 eb를 만들자
```bash
$eb create

# Envrionment Name을 설정하자 Application의 하위에 존재 하는 것이다.
Enter Environment Name
(default is eb-docker-dev): eb-docker-dev

# 해당 env에 DNS CNAME을 지정하자
Enter DNS CNAME prefix
(default is eb-docker-dev): eb-docker-dev-cname

# 로드밸런서 타입을 지정한다.
Select a load balancer type
1) classic
2) application
3) network
(default is 2): 2

Creating application version archive "zip_file".
Uploading eb-docker/<zip_file>.zip to S3. This may take a while.
Upload Complete.
Environment details for: eb-docker-dev
...
```

이제 s3에 eb용 bucket이 생길것이고 eb가 셋팅되기 시작한다 기다리자.
모든 설정이 끝나면 cli에서 오픈 해보자
```
eb open
```

Hello World

> eb local run 을 하면 `ERROR: UnicodeDecodeError - 'ascii' codec can't decode byte 0xec in position 118: ordinal not in range(128)` 이라는 에러가 난다 이유를 모르겠다..


### elb의 health-check가 자꾸 안된다면 이렇게 해보자..
```nginx
server {
    listen 80;
    server_name  *.elasticbeanstalk.com *.amazonaws.com localhost;
    charset utf-8;
    client_max_body_size 128M;
    
    # health-check 추가
    location /health-check {
        access_log off;
        return 200;
    }
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
elb의 대상 그룹에 상태 검사 url 부분을 /health-check로 바꾸어 주자

## 참고
출처 : [스승님 블로그](https://lhy.kr/eb-docker)
출처 : [KH BYUN님 블로그](https://novemberde.github.io/docker/2017/07/03/Elastic_Beanstalk.html)