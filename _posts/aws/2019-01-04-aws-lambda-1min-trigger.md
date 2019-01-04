---
layout: post
title: "lambda에서 국내 코인 거래소 공지사항 크롤링후 텔레그램 봇으로 전송하기2 - trigger"
categories:
  - Aws
tags:
  - Aws
  - serverless
---

### 해당 포스트는 [lambda에서 국내 코인 거래소 공지사항 크롤링후 텔레그램 봇으로 전송하기1 - crawler](https://himanmengit.github.io/aws/2019/01/03/aws-lambda-crawling-selenium.html)에 이어지는 포스팅 입니다.

# 기능
[lambda에서 국내 코인 거래소 공지사항 크롤링후 텔레그램 봇으로 전송하기1 - crawler](https://himanmengit.github.io/aws/2019/01/03/aws-lambda-crawling-selenium.html) 에서 만든 `crawler`를 매 1분 마다 호출하여 크롤링을 하게 함.

# 완료 된 비즈니스 플로우   
* `trigger`(lambda)     
`git push` -> `CI(bitbucket pipeline)` -> `1분 반복 trigger(lambda, cloud watch event rate 1)` -> `invoke crawler`


# requirements

**OS**  
`MacOx High Sierra 10.13.6`

**Docker 환경**   
[Docker](https://www.docker.com/products/docker-desktop)    
[Docker-compose](https://docs.docker.com/compose/)  
[Docker-Desktop](https://www.docker.com/products/docker-desktop) 맥과 윈도에선 이것들을 한번에   
> 도커는 최대한 `lambda` 환경과 비슷한 환경에서 작업 및 테스트를 해보기 위해 필요함.

**local 환경**        
```
python==3.6
awscli==1.16.70
```

**lambda 환경**          
```
python==3.6
```

# 시작
# Step0 `trigger`코드 추가
```
├── src
│   ├── __init__.py
│   └── trigger.py
```
[소스 코드](https://github.com/himanmenGit/aws_lambda_exchange_crawler_to_trigger/tree/master/src)

* 이전과 동일하게 최상위 폴더에 `.aws.env` 을 만들고 자격증명 키를 넣는다 (아래에)

# 중요!!!!!
# 세번 읽으시오!
## 여기서 중요한것 `.gitignore`에 `.aws.env` 파일을 추가하여 깃에 올리지 말것!!!!!!!

# Step1 Makefile, Dockerfile, docker-compose.yml 만들기
* `trigger`에서는 `lambda`에 내장된 `boto3`를 사용하기 때문에 `requirements`가 없다.
        
1. `Makefile`
    ```bash
    docker-build:
	    docker-compose build

    docker-run:
        docker-compose run lambda src.trigger.trigger_func
    
    clean:
        rm -rf trigger trigger.zip
        rm -rf __pycache__
    
    build-trigger-package: clean
        mkdir trigger
        cp -r src trigger/.
        cd trigger; zip -9qr trigger.zip .
        cp trigger/trigger.zip .
        rm -rf trigger
    
    make-trigger-s3-upload: build-trigger-package
        aws s3 cp trigger.zip s3://${BUCKET_NAME} --profile=${PROFILE}
     
    ```

2. `Dockerfile`      
    ```dockerfile
    FROM lambci/lambda:python3.6
    MAINTAINER tech@21buttons.com
    
    USER root
    
    ENV APP_DIR /var/task
    
    WORKDIR $APP_DIR
 
    ```

3. `docker-compose.yml`      
    ```dockerfile
    version: '3'

    services:
      lambda:
        build: .
        env_file:
         - ./.aws.env
        volumes:
          - ./src/:/var/task/src/
        command: src.trigger.trigger_func
     
    ```

# Step2 도커빌드 해보기
1. `.aws.env` 파일을 루트 디렉토리에 생성        
    ```bash
    AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>
    AWS_BUCKET_NAME=<AWS_BUCKET_NAME>
    AWS_LAMBDA_ROLE=<AWS_LAMBDA_ROLE>
    AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
    AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
    AWS_PROFILE=<AWS_PROFILE>
    AWS_LAMBDA_FUNC_NAME=<AWS_LAMBDA_FUNC_NAME>
    AWS_CLOUD_WATCH_EVENT_NAME=<AWS_CLOUD_WATCH_EVENT_NAME>
    AWS_CLOUD_WATCH_EVENT_RULE=<AWS_CLOUD_WATCH_EVENT_RULE>
    
    ```

2. 빌드
`make docker-build` or `docker-compose build` 후 빌드가 성공 하면 

3. 실행
`make docker-run` or `docker-compose run lambda` or `docker-compose up`

4. 결과       
```
bithumb - 202
coinone - 202
```
이런 로그가 찍힌다면 성공!

***`.aws.env`파일은 절대절대 `git`에 포함되어서는 안된다***


# Step3 람다 함수 만들기

1. `create_lambda.sh`파일을 만든다     
    ```bash
    #!/bin/bash


    while read LINE; do
        eval $LINE
    done < .aws.env
    
    REGION=${AWS_DEFAULT_REGION}
    FUNCTION_NAME=${AWS_LAMBDA_FUNC_NAME}
    BUCKET_NAME=${AWS_BUCKET_NAME}
    S3Key=trigger.zip
    CODE=S3Bucket=${BUCKET_NAME},S3Key=${S3Key}
    ROLE=${AWS_LAMBDA_ROLE}
    HANDLER=src.trigger.trigger_func
    RUNTIME=python3.6
    TIMEOUT=60
    MEMORY_SIZE=512
    PROFILE=${AWS_PROFILE}
    
    make make-trigger-s3-upload BUCKET_NAME=${BUCKET_NAME} PROFILE=${PROFILE}
    
    # 함수 만듬
    aws lambda create-function \
    --region ${REGION} \
    --function-name ${FUNCTION_NAME} \
    --code ${CODE} \
    --role ${ROLE} \
    --handler ${HANDLER} \
    --runtime ${RUNTIME} \
    --timeout ${TIMEOUT} \
    --memory-size ${MEMORY_SIZE} \
    --profile ${PROFILE}
    
    # CLOUD WATCH EVENT 를 만듬
    RULE_NAME=${AWS_CLOUD_WATCH_EVENT_NAME}
    
    aws events put-rule \
    --name ${RULE_NAME} \
    --schedule-expression 'cron(* * * * ? *)' \
    --profile ${PROFILE}
    
    # 만든 이벤트에 퍼미션을 줌
    SOURCE_ARN=${AWS_CLOUD_WATCH_EVENT_RULE}
    ACTION='lambda:*'
    
    aws lambda add-permission \
    --function-name ${FUNCTION_NAME} \
    --statement-id ${RULE_NAME} \
    --action ${ACTION} \
    --principal events.amazonaws.com \
    --source-arn ${SOURCE_ARN} \
    --profile ${PROFILE}
    
    # 이벤트를 trigger 연결
    TARGETS_FILE=file://targets.json
    aws events put-targets \
    --rule ${RULE_NAME} \
    --targets ${TARGETS_FILE} \
    --profile ${PROFILE}
    
    ```
2. 최상위 디렉토리에 `targets.json`이라는 파일을 하나 만들고 해당 정보를 넣는다.
    ```json
    [
      {
        "Id": "1",
        "Arn": "trigger lambda의 arn"
      }
    ]
    ```   
    
3. 실행 빠밤    
`./create_lambda.sh`         

4. 확인   
`aws` 웹 페이지를 가서 파일을 업로드 한 `bucket`을 확인해보자.      
`trigger.zip`이 있으면 성공.      
`lambda`로 가서 새로운 람다 함수가 생겨 있으면 성공!      
그리고 `Cloud Watch Event`를 보면 아래에 1분 짜리 `trigger`이 생긴것을 확인 할 수 있다.

5. `log`확인
`lambda`의 모니터링에 `cloud watch log`로 가서 최신자 로그를 보면 이렇게 나올 것이다.
![](/assets/aws/crawler/aws_lambda_trigger_log.png)

> 혹시 에러가 뜬다면 정보들을 잘 확인해보자. 
> `aws: error: argument --source-arn: expected one argument` 에러가 뜬다면 `.aws.env`파일 마지막에 빈줄 하나 추가 해보자. 

> ***이제 1분마다 `trigger`람다가 작동하여 `crawler`를 호출하면서 새로운 공지가 있으면 텔레그램에 공지를 보여 줄 것이다.***

# Step4 람다 함수 업데이트 하기
크롤러와 동일 하다. 함수 이름과 파일이름만 다를 뿐       


# Step5 비트버켓 파이프라인 연결 하기
비트버켓 `PipeLine`사용 하는 부분도 `crawler`부분과 완전 동일 하다.



### 이제 잘 작동되는지 모니터링을 해보자.


# 끝!

# 알게 된 점.
1. `aws lambda`에서 다른 서비스(`lambda`, `s3`)를 호출 할때 `boto3`에 직접 `aws credential`을 넣어 주지 않아도
해당 서비스의 `role`이 호출 할 서비스에 정책이 연결이 되어 있으면 바로 사용 할 수 있다.

2. `docker-compose`의 `env_file`을 이용하여 환경변수를 셋팅 할수 있다.

3. `lambda`에서 `PYTHONPATH`를 환경변수에 등록하면 기본적으로 셋팅되어 있는 `LAMBDA_RUNTIME_DIR`을 덮어서 못 쓰게 된다.      
그것은 `lambda`에서는 기본적으로 `boto3`를 사용할 수 있지만 `requirements`들을 설치 하고 해당 라이브러리들이 있는 폴더를 환경 변수로 잡아 주게 되면       
기본으로 런타임 라이브러리인 `boto3`는 사용 할 수 없다는 것. 해결 방법은 두가지 이다.
`PYTHONPATH`에 `/var/runtime`을 추가 하는것과 `boto3`를 직접 `requirements`에 추가하는 것이다.


## 소스코드
[링크](https://github.com/himanmenGit/aws_lambda_exchange_crawler_to_trigger)

