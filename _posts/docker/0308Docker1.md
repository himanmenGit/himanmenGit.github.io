### Docker
일반적으로 서버를 관리 하는건 복잡하고 어려우며 고급 개발자들의 섬세한 작업이 필요 함.

여러대의 서버에서 돌아가고 있는 프로그램의 하나중 업데이트를 할 경우
사이드 이펙트가 어디서 나타날지 아무도 모른다. 그만큼 리스크가 큰 일이다. 그래서 아주 옛날 버전의 프로그램을 쓰는 경우가 많다.

하나의 서버에 여러개의 프로그램을 설치 하는 경우에도 프로그램끼리의 서로 사용하는 라이브러리의 버전이 다르거나 동일한 포트를 사용하는 경우 문제가 될수 있다. 그래서 다른 서버를 설치 하는 경우가 많았고 자원은 낭비되게 된다.

서버환경도 계속 바뀌는 일이 많아 발생한다.

DevOps의 등장으로 한사람이 서버를 관리하기가 쉬워 지고, 마이크로서비스 아키텍쳐가 유행하면서 프로그램은 더 잘게 쪼개져 관리가 복잡해짐. 새로운 툴은 계속 나오고 클라우드의 발전으로 설치 해야할 서버가 많아지는 상황에서 도커가 등장하여 서버관리 방식이 완전히 바뀌게 됨.

도커는 컨테이너 기반의 가상화 플랫폼 이다.

컨테이너 기반이라는것은 우리가 사용하는 pyenv로 만든 가상환경을virtualevnv라는 어떤 environment라는 이름을 가지는데 도커는 그것 한개한개가 컨테이너라는 이름을 가짐.

컨테이너 안에서 OS 가 돌아가고 해당 컨테이너 안에 있는 내용은 완전 분리가 되고 원래 시스템에 깔려 있는 OS나 프로그램과 상관없이 컨테이너 안에 새로운 OS와 프로그램을 설치 하여 사용할 수 있다. 
> 컨테이너안에 들어가는 OS는 Linux만 사용가능 하다.

컨테이너는 격리된 공간에서 프로세스가 동작하는 기술
기존의 가상화 방식은 주로OS를 가상화 함
Vmware나 virtualBox의 경우 호스트 OS위에 게스트OS 전체를 가상화 하여 사용하는 방식인데 많이 느리다.

이런 환경을 개선하기 위해 CPU의 가상화 기술(HVM)을 이영한 KVM과 반가상화 방식의 Xen이 등장. 이러한 방식은 게스트OS가 필요하긴 하지만 전체 OS를 반가상화하는 방식이 아니였기 때문에 호스트형 가상화 방식에 비해 성능이 향상됨. 이러한 기술들이 OpenStack이나 AWS, Rackspace같은 클라우드 서비스에서 가상 컴퓨팅 기술의 기반이 됨.

전가상화든 반가상화든 추가적인 OS를 설치 하여 가상화하는 방법은 어쨋든 성능 문제가 있었는데 이를 개선ㅇ하기 위헤 프로세스를 격리 하는 방식이 등장. 리눅스에서는 이 방식을 리눅스 컨테이너 라고 하고 단순히 프로세스를 격리 시키기 때문에 가볍고 빠르게 동작한다. CPU나 메모리가 프로세스가 필요한 만큼만 추가로 사용하기 때문에 성능손실이 거의 없다.

각 컨테이너에 접속하여 명령어를 입력할 수 있고 패키지를 설치 할 수도 있다.사용자를 추가 할 수도 있고 여러개의 프로세스를 백그라운드로 실행 할 수도 있다. CPU와 메모리 사용량을 제한 할 수도 있고 특정 포트와 연결하거나 호스트의 특정 디렉토리를 내부 디렉토리 인 것처럼 사용 할 수도 있다.

새로운 컨테이너를 만드는 시간은 1~2초 정도 걸리며 가상 머신비해 많이 빠르다.

도커는 새로운 기술이 아니라 Linux에서 사용중이던 프로세스를 격리하는 방법을 잘 감싸서 쉽게 활용하능 하게 만들어진 프로그램.

도커에서 컨테이너는 각각의 OS시스템이 돌아 간다고 생각하면 된다.
그런데 어떤 시스템을 쓸 것이냐는 Image를 사용하여 정한다.
해당 Image를 이용하여 컨테이너를 만들면 해당 Image에 대한 프로그램이 컨테이너에서 바로 실행이 가능하다. 하나의 이미지를 가지고 여러 컨테이너를 실행 시킬 수 있다.

이미지는 컨테이너 실행에 필요한 파일과 설정값등을 포함하고 있고, 상태값을 가지지 않고 변하지 않는다.
컨테이너안에서 변경된 내용은 이미지 파일에 어떤 영향도 주지 않는다. 해당 변경 내용은 해당 컨테이너 안에서만 적용된다. 그리고 컨테이너가 없어지는 순간 변경사항은 모두 사라진다.
그래서 데이터를 저장하는 공간은 컨테이너 밖에 있어야 한다.(Rds, S3 등)

이미지는 컨테이너를 실행하기 위한 모든 정보를 가지고 있기 때문에 더이상 의존성 파일을 컴파일하고 이것저것 설치할 필요가 없다.

도커이미지는 DockerHub에 등록하거나 DockerRegistry저장소를 직접 만들어 관리 할 수 있다. 누구나 쉽게 이미지를 만들고 배포 할 수 있다.

도커는 새로운 기술이 아니며 이미 존재 하는 기술을 잘 포장했다고 볼 수 있다.

도커의 이미지 저장 방식은 레이어 저장 방식을 사용한다.
ubuntu 이미지가있고 nginx이미지를 만들고 싶은 경우 ubuntu이미지를 기반으로 nginx이미지를 만들기 때문에 용량이 추가적으로 늘어나거나 하지 않는다. 보통 이미지의 용량은 수백메가에 이른다. 

이미지는 url 방식으로 관리하며 태그를 붙일 수 있다.
ubuntu 14.04 이미지는 `docker.io/library/ubuntu:14.04` 또는 `docker.io/library/ubuntu:trusty` 이고 `docker.io/library`는 생략 가능하며 `ubuntu:14.04`로 사용 할 수 있다.

`Dockerfile`은 이미지를 만들기 위해 존재하는 파일 생성 문법이다.
`Dockerfile`을 만든 다음에 서버를 만들고 난후에 하는 셋팅들을 설정 해놓고 해당 파일을 실행시킨 결과를 이미지로 만든다.
`Dockerfile`은 실행파일이면서 어떤 설정을 저장해 놓은 기록도 되는 셈.

무료다.

설치
```
curl -fsSL https://get.docker.com/ | sudo sh
```
sudo 권한 주기
```
sudo usermod -aG docker $USER # 현재 접속중인 사용자에게 권한주기
sudo usermod -aG docker your-user # your-user 사용자에게 권한주기
```
컨테이너 만들기
```
docker run --rm -it ubuntu.16.04 /bin/bash
```
이렇게 하면 가상의 OS가 호스트 OS위에서 docker를 이용하여 실행 되고 있다. 
변경사항을 만들어 보자
```
apt-get update
```
만약 지금 컨테이너를 나가면 지금 한 변경 사항이 없어 진다.
그래서 데이터를 입력하여 새로운 이미지를 만들어 준다. (이미지는 불변)
`Dockerfile`을 이용하여 만들 수 있다.

프로젝트 폴더의 root에 `Dockerfile`을 만들어 보자 파일명은 `Dockerfile`이며 확장자는 없다. 이것이 기본 이름이다.

`Dockerfile`을 작성 해보자
```
FROM        python:3.6.4-slim
MAINTAINER  <메일 주소>

# apt-get으로 nginx, supervisor설치
RUN         apt-get -y update
RUN         apt-get -y dist-upgrade
RUN         apt-get -y install build-essential nginx supervisor

# requirements만 복사
COPY        .requirements/dev.txt /srv/requirements.txt

# pip install
WORKDIR     /srv
RUN         pip install -r  /srv/requirements.txt
RUN         rm -f           /srv/requirements.txt

# 소스폴더를 통째로 복사
COPY         . /srv/project

# nginx설정파일을 복사 및 링크
RUN         cp -f   /srv/project/.config/local/nginx.conf       /etc/nginx/nginx.conf &&\
            cp -f   /srv/project/.config/local/nginx-app.conf   /etc/nginx/sites-available/ &&\
            rm -f   /etc/nginx/sites-enabled/* &&\
            ln -sf  /etc/nginx/sites-available/nginx-app.conf   /etc/nginx/sites-enabled/

CMD	    pkill nginx
```
`MAINTAINER`는 메일 주소를 넣어 준다.
`FROM`으로 이미지를 불러 온다.
`RUN`은 명령 실행.
`SCP`와 비슷한 명령어인 `COPY`로 지정한 파일 및 폴더를 `docker container` 안으로 복사 할 수 있다. 정확히는 이미지 안으로 복사할 수 있다.
`WORKDIR`은 해당 디렉터리로 이동 하는 명령어.

이제 이미지를 만들어 보자 이미지를 만드는 명령어는
```
sudo docker build -t <Image name> -f <Dockerfile> <실행 기준 위치>
```
이미지가 잘 만들어 졌는지 확인해보자
```
docker images
```
지우고 싶은 이미지가 있다면 지워보자 
```
docker rmi <IMAGE ID(4글자만 쳐도 된다)>
```
이미지 실행 하기
```
# i 는 입력을 받을 수 있게 해주고
# t 는 터미널 환경에서 실행 할수 있게 해줌 
# /bin/bash 는 Dockerfile에 SMD가 있으면 빼야한다.

docker run --rm -it <Image Name>.<Version>:<Tag> /bin/bash
```

만약 컨테이너가 실행중 로컬 터미널에서 해당 컨테이너에 접근 하고 싶을 경우
`docker ps` 로 나온 `CONTAINER ID`를 이용하여 접근이 가능하다.
```
docker ps
CONTAINER ID
1234

docker exec 1234 /bin/bash
```
# supervisor
프로세스를 몇개를 정하여 프로세스 실행 명령을 정해 놓고 해당 프로세스들이 계속 해서 돌수 있도록 서비스처럼 관리 해주는 프로그램.

프로그램을 데몬형태 서비스 형태가 아닌 직접 실행하는 형태로만 실행 해야 한다.

nginx가 기본적으로 daemon 돌기 때문에 그것을 해지 해주어야한다.
`/etc/nginx/nginx.conf`의 가장윗 줄에 daemon off;를 적어 준다.

이 것으로 `nginx`와 `uwsgi`를 자동으로 실행 시켜 보자
`supervisord.conf`라는 파일을 만든다.
```
[program:nginx]
command=nginx

[program:uwsgi]
command=uwsgi --ini /srv/project/.config/local/uwsgi.ini
```
그리고 해당 파일을 복사하는 로직을 추가하자
```
# Dockerfile
RUN cp /srv/project/.config/local/supervisord.conf /etc/supervisor/conf.d/
```
`supervisor`는 nginx와 비슷해서 설정파일을 따로 줄수 있다. `/etc/supervisor`에 설정이 있는데 사용자가 원하는 설정을 넣고 싶을경우 `.conf` 파일을 `/etc/supervisor/conf.d/`안에 넣으면 `supervisor`가 실행될때 해당 설정을 가져와서 실행 된다. 데몬처럼 꺼지면 다시 켜주는 기능을 한다.

마지막으로 `supervisord -n`을 자동으로 실행하기 위해 `Dockerfile`의 마지막에 넣어 주자.
중요한것은 `CMD` 명령어 인데 도커파일 전체에서 딱 한번만 실행된다. 그래서 여러개의 실행문을 한줄에 적어 줘야 한다.
```
CMD pkill nginx; supervisord -n
```
으로 하고 `docker run`의 마지막에도 `/bin/bash`를 넣지 않는다
```
docker run --rm -it -p 8000:80 <Image Name>
```

그리고 도커파일을 개발 환경에 따라 다르게 빌드 되게 구성하여 사용 할 수도 있다.
```
Dockerfile.local
Dockerfile.procution
```
이런식으로 하면 된다.

그리고 테스트를 위하여 슈퍼유저를 만들어야 하는데 컨테이너를 만들 때 마다 슈퍼유저를 생성해야 하는 귀찮음이 생긴다. 그것을 해결하기 위해 `custom django-admin commands` 를 통하여 자신만의 커맨드를 `manage.py` 에 등록 할 수 있다. 마치 `./manage.py runserver`처럼 말이다.

일단 `members` 앱을 만들어 `AbstractUser`를 상속받는 사용자 지정 `User` 모델을 만들자.
```
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

```
그리고 `INSTALLED_APPS`에 추가하고 `AUTH_USER_MODEL = 'members.user'`를 할당하자.
```
AUTH_USER_MODEL = 'members.User'

INSTALLLED_APPS = [
    ...
    'members',
]
```
그리고 Command를 만들어 보자. 중요한것은 `def handle` 이다. 이 커맨드에 대해서 핸들 명령어를 써서 실행할 명령어를 구현 하면된다.
`members`에 파이썬 패키지로 `management`를 만들자. 이름을 정확하게 만들어야 한다. 그리고 그안에 `commands`라는 패키지를 또 만들고 그안에 `createsu.py`를 만들자. `.py` 파일의 이름이 명령어가 된다.
```
members
    ...
    ├── management
    │   ├── __init__.py
    │   └── commands
    │       ├── __init__.py
    │       └── createsu.py

```

그리고 `createsu.py` 에 커맨드를 만들어 넣자.
```
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
이제 `createsu`가 동작하는지 확인해보자 `./manage.py`를 해보면 명령어목록에 있을것이다.
```
[members]
    createsu
```
테스트를 위해 데이터베이스 `migrate`를 하고 `createsu`를 한다음에 `runserver`를 해서 `admin`에 접속해보자. 관리자 계정이 잘 들어가지는 것을 확인할 수 있다.
그러면 이제 데이터베이스 `migrate` 와 `createsu`를 자동으로 실행하기위해 `Dockerfile`에 넣자
```
...
# Sqlite DB migrate, createsupersuer
WORKDIR         /srv/project/app
RUN             python manage.py migrate
RUN             python manage.py createsu
...
```
이미지 파일을 만들어 보자. 파일명을 바꾼것을 확인하고 `local`이라는 태그도 붙여보자.
```
docker build -t docker-name:local -f Dockerfile .
```
그리면 도커를 실행하여 관리자 계정이 잘 되는 것을 볼 수 있다.