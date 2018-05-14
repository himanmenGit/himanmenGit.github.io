---
layout: post
title: "Django Storage 1"
categories:
  - Deploy
tags:
  - Deploy
---

IAM
    AWS에서 제공하는 기능에 대한 인증/인가를 위한 유저 관리 시스템
    특정 권한을 가진 유저를 생성하고, 자격증명 (Access Key ID, Secret Access Key)생성
    
Boto3
    Python과 AWS API를 연결 시켜 주는 라이브러리

AWS CLI
    Boto3를 기반으로 AWS의 서비스를 쉽게 사용할 수 있도록 도와주는 라이브러리

`Boto3`를 쓰기 위해 `.secrets/base.json`에 AWS KEY를 넣어 보자.
```bash
{
...
AWS_ACCESS_KEY_ID: "<AWS_ACCESS_KEY_ID>"
AWS_STORAGE_BUCKET_NAME: "<AWS_STORAGE_BUCKET_NAME>"
AWS_SECRET_ACCESS_KEY: "<AWS_SECRET_ACCESS_KEY>"
AWS_S3_ENDPOINT_URL = 'https://s3.ap-northeast-2.amazonaws.com'
AWS_DEFAULT_ACL = 'private'
}
```
`Storage`를 직접 구현할 수 있지만 매우 오래 걸림. 그래서 오픈 소스인 `django-storages`를 이용하자
`boto`와 `boto3`중 `boto3`를 사용하는 것이 좋다.

설치
```bash
pip install django-storages
```
설정
```python
INSTALLED_APPS = (
    ...
    'storages',
    ...
)
```
`Django`의 기본 파일 저장소는 `DEFAULT_FILE_STORAGE` 설정에 의해 제공 된다. 명시적으로 `Storage`시스템을 제공하지 않으면 이 스토리지 시스템이 사용 된다. 

`STATICFILES_STORAGE`는 `collectstatic` 이라는 커맨드를 실행했을때 어떤 스토리지를 쓸 것인가에 대한 것이다.

이 설정들을 `S3`를 쓰는경우 기본 실행 `backends`를 바꿔 주어야 한다.
`config/settings.dev 와 production .py`에 추가하자
```python
# Media(User-uploaded files)를 위한 스토리지
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Static files(collectstatic)를 위한 스토리지
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```
그리고 필수 적용 사항이 있다.
버켓에 대해 데이터를 올릴 수 있는 권한을 가진 자격 인증이 필요함
조금전 `base.json`에 넣어 놓은 키들을 `/config/settings.base.py` 에 넣어보자
```python
AWS_ACCESS_KEY_ID = secrets_base['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets_base['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets_base['AWS_STORAGE_BUCKET_NAME']
```
그리고 셸의 환경변수를 `dev`로 만들고 `./manage.py collectstatic`을 해보자 그럼 만들어진 `bucket`에 `collectstatic`으로 복사해온 정적 파일들이 올라 갔을 것이다.