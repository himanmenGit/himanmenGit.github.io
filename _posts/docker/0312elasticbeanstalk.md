# Elasticbeanstalk 기초

`EC2`를 사용하면 모니터링, 로드 밸런싱 등의 기능을 하나씩 붙여 줘야 쓸 수있는데, `Elastic Beanstalk`를 쓰면 모니터링, 로드밸런싱 같은 기능을 쉽게 사용 할 수 있게 해준다.

`PaaS` 서비스다. 그래서 우리는 `Application`만 올리면 된다. 하지만 설정을 많이 해야한다. 그런데 `docker`를 이용하여 그 설정을 최소한으로 할 수 있다.

`Docker` 이미지 한개가 하나의 `Application`이 된다. 

물론 `Docker`뿐 만아니라 `PHP`, `JAVA`, `Python`, `Ruby`, `Node.js`등등 을 올릴 수 있다.

만약 `Django`를 `Eb`에 올릴 경우 `Django`와 연결되는 웹 서버가 있어야 하는데 `EB`는 `apache`를 쓴다. 그래서 `apache`와 관련된 설정을 이해 하고 있어야 하고, 붙여주는 config파일에 `apache`에 관련된 설정을 넣어 줘야 한다. 그래서 매우 복잡하다. 하지만 `Docker`를 쓰면 `EB`에 있는 `Nginx`와 `Docker`의 `Nginx`를 연결 해 주면 된다.

## Elastic Beanstalk 만들기
새 애플리케이션을 생성하는 것을 CLI 로 해보자.
`EB`를 만드는데 필요한 것은 `EB CLI`라고 따로 존재 한다.
애플리케이션은 보통은 배포를 위한 프로젝트 1개를 말한다. 
하나의 프로젝트에는 여러개의 `EC2`서버가 돌 수 있다.

EC2 -> production

Deploy (Application)
    Production (Environment) -> Users
        branch: master or production
        EC2
        EC2
        EC2
    Dev (Environment)        -> Developers
        branch: dev
    issue91    -> Issue91 -> Developers
로 만들어 쓸수 있다. 여기서 보는 것은 `git`과 매우 밀접하게 관련이 있다는 것이다. 결국 커밋 당뉘로 프로젝트를 `EB`에서 관리 할 수 있다는 것이다.
그리고 하나의 `Environment`는 Load Balancing(Auto Scaling)을 이용해 `EC2`를 여러개 가질 수 있다. 실제 동작하는 `EC2`개수는 `Environment`개수가 최소한이다.

`EB`를 만들고 사용하기 위한 추가권한이 있는 `IAM`을 만들어야 한다. 
사용자 추가를 들어 가보자.
사용자 이름을 넣고 CLI를 이용 할 것이기 때문에 프로그래밍 방식 엑세스를 선택한다.
그리고 기존 정책 직접 연결을 선택하고 `Elasticbeanstalk`를 검색하여 `AWSElasticBeanstalkFullAccess` 를 추가하고 검토 한다음 사용자 보안 자격증명을 다운받고 해당 자격증명을 `~/.aws/credential`에 추가하자.
***`EB`는 여러가지 `AWS`서비스를 모아서 서비스 한다. 그중에 `EC2`도 포함 되어 있기 때문에 매우 위험한 권한이다. 그렇기 때문에 이 코드는 절대 외부로 유출 되어서는 안된다.***

설치 해보자
```
pip install awsebcli
```
그리고 `EB`를 초기화 해주어야 한다. 
프로젝트 폴더로 가서
```
eb init --profile <profile_name>
```
이후 해당 목록을 보고 진행을 하면된다.
기본 지역 선택을 자신의 aws 지역을 선택
애플리케이션네임도 만들어 주자.
그리고 만약 프로젝트에 `Dockerfile`이 없으면 플랫폼을 선택 하라고 뜨는데 우린 7번 `Docker`를 선택하자. `Dockerfile`이 있으면 생략이 된다.
도커 버전은 최신버전인 1번.
엔터
엔터
EC2를 사용하기 때문에 키페어가 필요 하다. 키페어는 원래 사용하던 녀석을 사용 하도록 하자. (새로 만들어서 사용해도 상관 없다)

이제 프로젝트 폴더에 `.elasticbeanstalk` 폴더가 만들어진 것을 볼 수 있다.
이렇게 하면 애플리케이션이 만들어진 것이다. `AWS` 사이트의 `Elastic Beanstalk`를 가보면 환경이 없는 빈 애플리케이션이 하나 만들어 져있다. 이제 여기에 환경을 하나 만들고 그 환경에 우리의 애플리케이션을 배포 하면 된다.

이제 `Elastic Beanstalk`에 `Docker`를 올리는 방법을 알아 보자. `EB`에는 이미 `Docker`가 설치 되어 있다. 그래서 `Docker`에서 동작할 수 있는 `Container`하나만 올리면 알아서 구성을 해준다.
단일 컨테이너 Docker
하나의 `EB`에서 하나의 컨테이너만 돌리는 방법
`Dockerfile`(빌드할 이미지)만 전달하면 해당 도커파일만 가지고 설정을 해준다.
`Dockerfile`이라는 이미지를 만든다. 내용은 `Dockerfile.production`과 동일하게 한다.
그리고 필수명령인 `EXPOSE`를 사용하여 포트를 나열하면 외부에서 해당 포트로 접속 할 수 있도록 열리게 된다. `EXPOSE`의 첫번째 포트를 사용하여 호스트의 역방향 프록시에 컨테이너를 연결하고 퍼블릭 인터넷의 요청을 라우팅 한다.
`EB`를 이용하게 되면
브라우저 에서 요청이 오면 `EB`가 요청을 받는다. 그러면 `EB` 내부의 `Nginx`가 요청을 받아 프록시를 통해 (프록시란 어떤 요청을 다른 곳으로 전달 하는것) 도커 컨테이너로 전달된다. 그럼 이 요청은 도커 애플리케이션의 `Nginx`로 전달되고 다시 도커 안에 있는 `uWSGI`로 전달 이후 도커의 `Django`로 전달 되는 것이다.
```
Browser -> EB -> EB-Nginx -> (proxy) -> Docker Container -> DockerApp-Nginx -> DockerApp-uWSGI -> DockerApp -> Django
```
결국 브라우저에온 요청을 도커 컨테이너로 전달(라우팅) 해주는 것을 `EXPOSE` 의 첫번째 포트를 통해서 한다는 것이다. 

```
# Dockerfile
...
CMD	pkill nginx; supervisord -n
# EB에서 프록시로 연결될 Port를 열어줌
EXPOSE	80
```
여기서 80번 포트를 여는 이유는 `.config/production/nginx-app.conf`의 `listen`이 80번으로 열려 있기 때문이다.
그리고 `nginx-app.conf` 의 `server_name` 에 `*.elasticbeanstalk.com` 추가. `settings.ALLOWD_HOSTS` 에 `'.elasticbeanstalk.com',` 추가.

그리고 배포를 할때 10분이상의 시간이 걸리면 배포를 실패 했다고 판단한다. 그래서 배포할때의 시간을 최대한 줄여야 하는데, 헤당 `Dockerfile` 을 만들때 퍼블릭 리포지토리, 즉 `Docker Hub`를 이용해서 할 수 있다. 만들어 놓은 이미지의 용량이 크므로 베이스가 되는 부분은 도커허브에 올려 놓고 변경사항에 대해서만 배포가 되게 하면 빠르게 할 수 있다.

일단 배포를 한번 해보자
```
eb create --profile eb
```
하게 되면 `Environment Name`을 적으라고 나온다. 적당하게 넣어 주자. (ex. Production)
그리고 `DNS CNAME`을 적으라고 하는데 이것은 `EB`에서 고유한 것이기 때문에 유니크한 이름을 적어 주자. 로드밸런스는 2번 `Application`을 선택하자.
그리고 엔터를 치면 첫 배포가 진행이 된다.

그렇게 해놓고 배포 시간을 줄이기 위해 베이스가 되는 부분을 `Dockerfile.base`로 만들어 보자
```
FROM        python:3.6.4-slim
MAINTAINER  <Your Email>

ENV         LANG C.UTF-8

# apt-get으로 nginx, supervisor설치
RUN         apt-get -y update
RUN         apt-get -y dist-upgrade
RUN         apt-get -y install build-essential nginx supervisor

# requirements만 복사
COPY        .requirements /srv/.requirements

# pip install
WORKDIR     /srv
RUN         pip install -r /srv/.requirements/production.txt
```
대충 이정도로 시간이 소비 될거 같은 기본 이미지를 만든다. 그리고 이 이미지를 도커빌드 하여 이미지로 만들어보자
```
docker build -t eb-docker:base -f Dockerfile.base .
```
이미 만들어진 레이어들이기 때문에 금방 만들어 진다. 그러면 이 이미지를 도커허브에 올려 보자.
도커 허브에 새로운 레포지토리를 만들자 eb-docker라는 이름으로 만들자. 일단 퍼블릭으로!
그리고 만들어진 레포지토리의 이름 [계정명/레포지토리 이름] 으로 저장소의 주소를 사용할 수 있다.
이 것으로 `push`와 `pull`을 사용한다. 그럼 이미지를 한번 `push`해보자
일단 도커 로그인을 하자
```
docker login
```
도커허브 계정정보를 넣자. 그리고 태그를 붙여놓고 `push`를 하자. 
```
docker tag eb-docker:base <도커허브계정명/eb-docer:base>
docker push <도커허브계정명/eb-docker:base>
```
그리고 우리가 만든 저장소 명이랑 로컬에서 `tag` 명령어로 만든 `Tag`명(이미지 명)을 똑같이 지어줘야 한다. 그러면 `push`를 할때 이미지가 자기 이름에 해당하는 저장소에 올라간다.

그러면 저장소에 base라는 이름으로 압축된 용량으로 올라가 있는것을 확인할 수 있다.

그리고 `Dockerfile`을 수정하자. `Dockerfile.base`에 들어 간 내용을 지우고 저장소의 도커파일을 불러오도록 하자
```
FROM	<도커허브계정명/eb-docker:base>

```
그리고 `EB`가 기본적으로 `Git`에 의해서 동작하게 되어 있다. 커밋을 하지 않은 내용은 `EB`에 포함되지 않는다. 그래서 수정된 부분을 반영 시키기 위해서를 커밋을 해야 한다.

커밋을 하고 배포를 해보자. 재배포는 첫 배포와는 다른 명령어를 사용한다.
```
eb deploy --profile eb
```

그리고 내부적으로 배포 스크립트를 만든다고 하면 도커이미지를 빌드하고 도커허브에 푸시한다음 배포를 실행하게 하면 로컬에서 변경사항이 있어도 베이스 이미지를 도커허브에 올려 새로올린 이미지를 사용하므로 소스코드의 변경 내용을 반영 시킬 수 있다.

그리고 배포가 완료되면 `eb open`으로 해당 서비스를 실행시켜 볼 수 있다.
만약 `Internal server Error`가 발생하면 `Sentry`를 통해서 확인하거나, 해당 도커 안으로 들어 가서 로그를 확인해봐야 한다.

`EB` 로 만들어진 `EC2`를 접속하기 위해서는 `eb ssh`를 사용하여 접속 할수 있고, 해당 `EC2`내에서 다시 `Docker` 내로 진입 하려면 아래 명령을 사용하면된다.

`EB`에서 만들어진 `EC2`는 `Amazon Lunux`를 사용한다 이것은 `CentOs` 기반이다.

도커로 접속 해보자
```
sudo Docker ps
# CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
# 68be8c55be0a        c93666c7b5ad        "/bin/sh -c 'pkill..."   14 hours ago        Up 14 hours         80/tcp              vibrant_wilson
```
`CONTAINER ID` 를 통해 도커 내부로 들어 갈수 있다.
```
sudo Docker exec -it 68bbe /bin/bash
```
그리고 로그 확인
```
cat /tmp/uwsgi.log
```
아니면 `EC2`로 들어가기 전에 해당 `EB`의 로그를 모두 가져 올수도 있다.
```
eb logs
```
이 로그중에 `/var/log/eb-activity.log` 부분에 오류 잘 나온다.

로그를 확인해보면 아마도 `base.json` 을 읽지 못했다는 오류가 발생 할 것이다.
이것은 `.gitignore`에 `.secrets`가 포함되어 있는데 이거 때문에 도커에 전달이 되지 않는다. 배포를 할때 `EB`에서 복사하는 파일 목록에 해당 파일이 제외가 된다.
그래서 `.gitignore`와 동일한 역활을 하는 `.ebignore`라는 파일을 만들어 `.secrets` 를 포함시키게 한다.
```
# .ebignore
!/.secrets
```
그리고 해당 변경사항들을 커밋하고 다시 배포를 하고 확인을 해보자. 하지만 관리자 페이지를 가서 로그인을 해보면 접속이 되지 않고 타임아웃이 뜰 것이다.
이유는 `EB`에서 만들어진 `EC2`가는 `RDS`에 들어갈수 있는 권한이 없기 때문이다.
`RDS`의 보안그룹에 `EC2`의 보안그룹에 `EB`의 `Environment`이름인 `Producion`중 `SecurityGroup for ElasticBeanstalk environment.` 을 인바운드로 포함 시키자.
그러면 로그인이 될 것이다.
이렇게 하면 `Elastic BeansTalk`를 이용한 가장 기본적인 배포 방법을 알아 보았다.

그런데 `.ebignore`를 사용하면 `.gitignore`의 내용이 무시 되는 경우가 있다고 한다. 그래서 `.ebiginre`를 없애고 배포 스크립트를 통해 해당 `.secrets`폴더를 깃의 `stage`에 올렸다가(`git add -f .secrets`) 배포후 다시 `stage`에서 빼는 작업(`reset HEAD .secrets`)을 해야 한다.
***만약 배포중 취소를 하게 되면 `.secrets`폴더는 `git`의 `stage`에 올라 가 있기 때문에 해당 타이밍에 `commit`이나 `reset --hard`를 하게되면 파일이 완전 삭제 되거나 `push`할 경우 깃허브에 중요한 정보들이 올라 갈 수 있으므로 주의를 요한다.***
배포 스크립트인 `deploy.sh`를 만들고 `chmod`를 통해 사용 권한을 주자
```
# deploy.sh
#!/usr/bin/env bash
git add -f .secrets && eb deploy --staged --profile=eb && git rest HEAD .secrets
```
```
sudo chmod 755 deploy.sh
```
그리고 해당 스크립트로 배포를 하면 된다.

그리고 만약 `EC2` 안의 `Docker` 내에서 실행시켜야 할 명령들이 있다면 매번 해당 `Docker`를 찾아 들어가 실행시키기는 너무 귀찮다. 우리는 배포가 모두 끝나고 모든 내용이 `EC2` 안에 적용 되어 있을때 특정 커맨드를 실행 시키고 싶은 경우거나 배포전에 커맨드를 실행시키거나 특정 타이밍에 커맨드를 실행 시키고 싶은 경우들이 존재 한다. 그것이 `.ebextensions`를 이용한 방법이다. `EB`는 `.ebextensions` 내에 `.config`라는 파일을 찾아 커맨드를 실행한다. 
`Eelastic Beanstalk`는 어떤 시점에 기능을 실행하고 싶은 스크립트를 넣어 놓을수 있는 디렉토리를 제공한다. `hook platform`을 이용하여 특정 디렉토리에 스크립트를 넣어 놓으면 해당 시점에 맞게 스크립트를 실행 시켜 준다.
EC2 내의 `/opt/elasticbeanstalk/hooks/appdeploy/<시점>/<스크립트파일>` 에서 동작한다.
* appdeploy - 애플리케이션을 배포할 때 실행되는 스크립트. 새 인스턴스가 시작될 떄와 클라이언트에서 새 배포 버전을 초기화 했을때 `Elastic Beanstalk가 애플리케이션 배포를 수행한다.
* configdeploy - 인스턴스에서 소프트웨어 구성에 영향을 미치는 업데이트를 클라이언트에서 수행하면 실행되는 스크립트.
* restartappserver - 클라이언트에서 앱 서버 작업 재시작을 수행하면 실행되는 스크립트.
* preinit - 인스턴스 부트스트래핑 중 실행되는 스크립트
* postinit - 인스턴스 부트스트래핑 후 실행되는 스크립트.
`appdepoly`를 사용하여 배포를 한후에 스크립트를 실행하게 하자.
그럴려면 배포 스크립트를 만들어야 한다. `files` 키를 사용하여 EC2 인스턴스에서 파일을 생성 할 수 있다. 콘텐츠는 구성파일의 인라인이거나 URL에서 내용을 가져 올 수 있다.
`.ebextensions`에 `00_command_files.config`를 만들고 커맨드파일을 만들게 하자. 그리고 만들어진 스크립트는 `container_commands`라는 옵션을 통해 배포가 되기 전에 임시 파일을 만들고 배포후에 해당 파일이 있으면 실행하게 하자.
```
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
`container_commands`는 애플리케이션과 웹 서버를 설정하고 애플리케이션 버전 아카이브의 압축을 푼 후 애플리케이션 버전을 배포하기 이전에 실행된다. 그리고 `leader_only`를 사용하여 여러개의 `EC2`가 존재 할 경우 리더격이 되는 `EC2`에서만 한번 실행 할 수 있다.
`.ebextensions`폴더에 `01_django.config`라는 파일을 만들자, 
그리고 공부중 AWS의 S3가 프리티어 용량을 초과했다. 그래서 collectstatic 을 EC2안에서 직접 서빌되게 하기로 했다. 방법은 배포가 끝나고 EC2에서 collectstatic 스크립트를 실행 시키게 하는 것이다.
1. `STATICFILES_STORAGE`를 기본 값으로 만들어 준다.
`settings`의 `dev`, `production`에 `STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'`를 주석 처리
2. `nginx-app.conf` 에 `/static/` URL 서빙
```
    ...
    location /static/ {
        alias /srv/project/.static/;
    }
```
3. `config/settings`에 `STATIC_ROOT`, `STATIC_URL`설정
```
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATIC_URL = '/static/'
```
```
container_commands:
  01_migrate:
    command:  "touch /tmp/migrate"
    leader_only: true
  02_collectstatic:
    command:  "touch /tmp/collectstatic"
    # S3를 사용하지 않도록 설정하였으므로 모든 EC2에 정적파일이 존재할 수 있도록 leader_only 옵션 해제
  # leader_only: true
  03_createsu:
    command:  "touch /tmp/createsu"
    leader_only: true
```
그리고 `static`파일 주소가 바뀐것을 확인 할 수 있다.
이렇게 하면 배포가 끝난후 해당 도커에서 `migrate`,`collectstatic`, `createsu`를 차례로 실행한다.

### 배포 과정
1. 로컬 Git에서 git archive 명령을 사용해서 소스코드 압축 파일 생성.
2. 소스코드를 eb용 S3에 업로드
3. 동작하고 있던 EC2에 해당 소스코드를 다운로드
4. 소스코드에 포함된 Dockerfile을 실행
5. 생성된 이미지를 사용해서 Container실행
6. EC2의 Nginx에 Container를 프록시 연결

### 서버 접속 단계
```
Browser -> EB -> ELB -> EC2 -> Nginx -> docker run (자동)
                        -> Dockerfile -> DockerContainer(EB-Nginx)
                                -> EXPOSE 첫 번째 포트
                                	-> uWSGI -> Django

```
### `EB`의 구조

```
EC2
    AmazonLinux
        Nginx
        Docker
        배포 스크립트 - Dockerfile or Dockerrun.aws.json
            Dockerfile을 사용해서 DockerImage생성
            생성한 이미지를 run
            갖고있는 Nginx와 이미지를 실행한 컨테이너를 연결

        우리가 생성한 배포 스크립트와의 연결 설정 파일
            .elasticbeanstalk/config.yml
            Dockerfile
```
### EB는 실체가 없이 여러가지 시스템을 구성 해주는 시스템이다.
```
EB (ELB -> (AutoScaling) -> EC2... -> Application(Docker))
	# 부가기능
	Monitoring...
	Alarm..
	
Browser -> ELB(로드밸런스) -> EC2
			   -> EC2
```
