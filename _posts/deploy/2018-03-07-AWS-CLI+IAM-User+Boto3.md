---
layout: post
title: "AWS CLI와 Boto3를 이용한 S3버켓 만들기"
categories:
  - Deploy
tags:
  - Deploy
---

# Boto3
터미널 창에서도 AWS 서비스를 사용 할 수 있게 만든 것.
S3에 접근을 할때, Storage를 만들때 사용 해볼 것.

 배포 방법중에는 S3와 Rds는 나두고 EC2의 인스턴스만 새로 생성하면서 배포하는 방법도 있음. 그러면 코드가 변경된 적용사항이 자주 적용 되었이 떄문에 오류가 적다. 메모리 누수에 대한 걱정이 없다.
 
 설치
 ```
 pip install boto3
 ```
 하지만 `boto3`를 쓰기 위해서는 자격 증명이 필요 한데. 이것은 `IAM` 콘솔을 사용 해야 한다.
`IAM` 콘솔로 가서 사용자를 추가 한다.
 엑세스 유형은 프로그래밍 방식 엑세스를 사용하면 `CLI` 환경에서만 작동 한다. (boto3, AWS CLI 등)
메니지 먼트경우 인터넷을 이용한 콘솔을 사용함
우리는 프로그래밍 방식 엑세스를 사용하자.
기존 정책에 직접 연결 - 정책유형 `AmazonS3FullAccess` 검색후 체크 다음 진행
`.csv` 키파일을 다운 받고 안전한곳에 저장 하자. 이 키들을 한번만 보여주고 보여 주지 않는다. 이제 이 키파일을 추가 해야 한다.
`AWS CLI`는 `boto3`를 기반으로 만들어진 것. 간단한 명령어로 파일을 `S3`에 복사하거나 `AWS` 서비스를 이용할 수 있다. 하지만 자격 증명이 필요 한데, 이 자격 증명에는 방금전 발급 받은 엑세스 키들이 필요 하다.
이 엑세스 키들을 `aws config`에 기록 해놓으면 그 데이터를 기반으로 `AWS boto3`가 동작한다. 
설치
*** 글로벌로 설치 하는것이 좋다 ***
```
pip install awscli --upgrade --user
```
설치 하면 `/home/sumin/.local/bin/aws`에 `aws`를 찾을수 있다.

설정
`aws configure` 명령으로 설정하면되는데 여기에 키 값을 넣어 주면 해당 키들로 설정이 된다.
```
AWS Access KEY ID [None] : <Access key ID>
AWS Secret Access KEY ID [None] : <Secret access key>
Default region name [None] : <ap-northeast-2>
Default output format [None] : json 
```
이렇게 하면 `~/.aws` 폴더가 생겨 있고 `config`와 `credentials`가 있다.
credentials에는 현재 설정된 프로필과 acces_key들이 있다. 프로필 이름을 `s3`로 변경하자
```
# [defalut]
[s3]
```
` Boto3`에서 `IAM` 콘솔 들어가서 새로운 유저를 만들었고 `AccessKey`를 이용하여 `AWS Configure`에 해당 `AccessKey`의 내용을 넣었다.

`Bucket`은 저장소를 한개 씩 구분 하는 것. 프로젝트 한개당 버킷을 여러개 사용 할수 있는데 보통 장고 프로젝트 에서는 한개의 버킷에 `static`과 `media` 폴더를 따로 두는 형식을 사용한다. 

이제 아까 만들어 놓은 `s3`라는 프로필의 유저로 `Boto3`이용하여 `Bucket`을 만들 것이다. 
`ipython`을 이용하여 만들어 보자
설치
```
pip install ipython
```
설치한 패키지를 requirements.txt에 넣는 것을 잊지 말자.
그리고 `Bucket` 만들기
```
import boto3
session = boto3.Session(profile_name='s3')
client = session.client('s3')
client.create_bucket(Bucket='fc-7th-ec2-deploy-himanmen', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
```
> `create_bucket(Bucket='name')`에서 `name`은 전 세계에서 유일한 이름이어야 한다. 다른 AWS 사용자의 `bucket`이름을 사용 할 수 없다. 그리고 언더스코어가 아닌 하이픈을 사용 해야 한다.
를 하게되면 `AWS S3`에 `Bucket`이 생성된 것을 볼수 있다.
