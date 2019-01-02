---
layout: post
title: "s3에 올라온 이미지를 aws lambda를 이용하여 썸네일 만들기"
categories:
  - Aws
tags:
  - Aws
  - serverless
---

# 기능
`s3`에 업로드된 이미지를 `lambda`와 `Pillow`를 사용하여 썸네일을 만든후 다시 `s3`에 업로드.
![](/assets/aws/thumbnail/aws_lambda_s3_thumbnail_architecture.jpg)

# requirements

**OS**  
`MacOx High Sierra 10.13.6`

**Docker 환경**   
[Docker](https://www.docker.com/products/docker-desktop)    
[Docker-compose](https://docs.docker.com/compose/)  
[Docker-Desktop](https://www.docker.com/products/docker-desktop) 맥과 윈도에선 이것들을 한번에
> 도커가 필요 한 이유는 썸네일을 만드는 기능을 `lambda`에 올리기 위해선 `Pillow`를 추출하여 소스와 같이 패키징 한다음 `s3`에 패키지를 업로드 해야 하는데   
`Pillow`를 `pip install -r requirements.txt -t pil/lib/.` 과 같이 추출 할 경우 기능이 정상 동작 하지 않는다.     
그래서 `"errorMessage": "Unable to import module 'XXXX'"`라는 에러를 볼 수도 있는데 이를 해결 하기 위한 간단한 방법으로      
도커를 사용하여 `Pillow`를 설치하고 해당 패키지 파일을 `volume`옵션을 통해 프로젝트와 파일을 연결하여 추출하기 위함.

**lambda 환경**   
```
python==3.6
Pillow==5.3.0      
boto3==1.6.18
```

# 시작
### step0 역할(role) 만들기
1. IAM -> 역할 -> 역할 만들기
2. AWS 서비스(Lambda) -> 정책검색(AWSLambdaFullAccess, AmazonS3FullAccess) 후 체크박스 체크   
-> 태그 추가(패스) -> 검토 역할 이름 ex)aws-lambda-thumbnail-role -> 역할 만들기
    * 리스트
    ![리스트](/assets/aws/thumbnail/aws_role_list.png)
    * 디테일
    ![디테일](/assets/aws/thumbnail/aws_role_detail.png)

### Step1 람다 함수 만들기
1. Lambda -> 함수 생성 -> 새로 작성   
    * 이름 - `myThumbnailFunc   `
    * 런타임 - `Python 3.6`
    * 역할 - 기존 역할 선택 `aws-lambda-thumbnail-role`    
    ![](/assets/aws/thumbnail/aws_create_lambda1.png)

2. 함수 생성
    * 생성 완료
    ![](/assets/aws/thumbnail/aws_create_lambda2.png)


3. 테스트    
    * 코드 수정   
    ![](/assets/aws/thumbnail/aws_lambda_test1.png)
    * 테스트
    ![](/assets/aws/thumbnail/aws_lambda_test2.png)
    위 사진과 같이 설정후 테스트 버튼 ㄱㄱ  
    * 결과  
      ![](/assets/aws/thumbnail/aws_lambda_test3.png)

    이제 람다 함수는 제대로 만들어 진 것을 확인 함.

### Step2 썸네일 만들기 코드 작성
1. 적절한곳에 폴더를 만들고 virtualenv 적용
    ```shell
    mkdir aws_lambda_pil
    cd aws_lambda_pil
    pyenv virtualenv 3.6.5 aws_lambda_pil_3.6.5
    pyenv local aws_lambda_pil_3.6.5
    mkdir src
    touch src/__init__.py
    touch src/thumbnail.py
    ```
2. `requiremnets.txt` 만들기
    ```bash
    Pillow==5.3.0
    boto3==1.6.18
    ```
3. `thumbnail.py` 코드 작성
    ```python
    # thumbnail.py
    import urllib.parse
    import boto3
    import uuid
    from PIL import Image

    # aws내에서는 서비스 끼리 명시적인 credential이 없어도 호출이 가능 하다.
    s3_client = boto3.client('s3')

    # 이미지 사이즈 반으로 리사이즈
    def resize_image(image_path, resized_path):
        with Image.open(image_path) as image:
            image.thumbnail(tuple(x / 2 for x in image.size))
            image.save(resized_path)


    # 람다가 호출할 함수
    # 등록한 버킷에 파일이 올라가면 람다함수가 트리거 되면서 event에 해당 정보가 담겨 옴.
    def handler_func(event, context):
        try:
            for record in event['Records']:
                # 버켓 네임을 받음
                bucket = record['s3']['bucket']['name']
                # 파일 Key를 받음
                key = record['s3']['object']['key']

                # 람다함수는 /tmp/에만 파일을 쓸 수 있다.
                download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
                upload_path = '/tmp/resized-{}'.format(key)

                # 한글 파일명을 위한 디코딩
                decode_key = urllib.parse.unquote(key)
                # himanmen-aws-lambda-thumbnail에서 파일을 받아
                s3_client.download_file(bucket, decode_key, download_path)

                # 리사이징 후
                resize_image(download_path, upload_path)

                # himanmen-aws-lambda-thumbnail-resized로 파일을 업로드
                # ACL을 퍼블릭으로 메타데이터는 image/jpeg로
                s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key,
                                  ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'})
        except Exception as e:
            print(e)
    ```

### Step3 `code,boto3,Pillow`를 패키징
1. 패키징을 편하게 하기위해 `Makefile` 생성
    ```shell
    clean:
      rm -rf pil pil.zip
      rm -rf __pycache__

    fetch-dependencies:
      mkdir -p lib/

    build-pil-package: clean fetch-dependencies
      mkdir pil
      cp -r src pil/.
      cp -r lib pil/.
      pip install -r requirements.txt -t pil/lib/.
      cd pil; zip -9qr pil.zip .
      cp pil/pil.zip .
      rm -rf pil
    ```

2. `pil.zip`파일 생성   
이 파일에는 `src`와 `boto3, Pillow`등의 라이브러리 파일이 포함 되어 있음.   
`> make build-pil-package` 실행 후 `pil.zip`파일 생성   
이 파일의 압축을 풀어 보면   
![](/assets/aws/thumbnail/aws_lambda_pil_zip1.png)
![](/assets/aws/thumbnail/aws_lambda_pil_zip2.png)
위 사진과 같이 파일들이 압축 되어 있는것을 볼 수 있다.

### Step4 압축된 `pil.zip`파일을 `S3 bucket`에 업로드
용량이 큰 소스 코드는 `s3`에 올려서 `lambda`를 사용 해야 한다.    
버킷 이름은 전체 아마존 서비스 내에서 유일 해야 한다. (중복 불가)

1. 버켓 만들기 3개    
    * 소스코드를 올릴 버킷 1개 ex)`himanmen-aws-lambda-thumbnail-code`
    * 이미지를 업로드 할 버킷 1개 ex)`himanmen-aws-lambda-thumbnail`
    * 썸네일 이미지를 저장할 버킷 1개 ex)`himanmen-aws-lambda-thumbnail-resized`
    * 썸네일 이미지를 저장할 버킷은 퍼블릭 액세스 설정을 해제 해 준다.
    * 새 퍼블릭 ACL 및 퍼블릭 객체 업로드 차단 (권장) 해제
    * 퍼블릭 ACL을 통해 부여된 퍼블릭 액세스 권한 제거 (권장) 해제
    * 이는 썸네일로 만들어진 이미지는 외부에 공개 되어야 하기 때문이다.
    ![](/assets/aws/thumbnail/aws_lambda_create_bucket.png)

2. 소스 코드 올리기
    * 코드를 올릴 버킷에 `pil.zip`를 업로드 한다.
    * 그리고 해당 객체의 url을 복사한다.
    ![](/assets/aws/thumbnail/aws_lambda_upload_code.png)

3. `lambda`에 코드 적용
    * `lambda`로 가서 함수 코드 부분의 코드 입력 유형을 `Amazon S3에서 파일 업로드`로 변경
    * 아래 `Amazon S3 Url`에 위에서 복사한 파일의 `URL`을 넣음.
    * 그리고 오른쪽에 핸들러 부분에 `src.thumbnail.make_thumbnail_func` 이라고 입력.
    ![](/assets/aws/thumbnail/aws_lambda_upload_code2.png)
    * 그리고 소스와 `boto3`,`Pillow`를 사용하기 위해 `src`, `lib`폴더를 `lambda`의 환경 변수로 지정
    * `PYTHONPATH` 를 `/var/task/src:/var/task/lib`
    ![](/assets/aws/thumbnail/aws_lambda_upload_code3.png)
    * 저장

4. 이미지가 업로드 될 버켓을 연결   
    * `lambda`의 `Designer`에서 왼쪽 네비 바의 `S3`를 선택
    ![](/assets/aws/thumbnail/aws_lambda_connect_s3_1.png)
    * 아래 트리거 구성 설정
    ![](/assets/aws/thumbnail/aws_lambda_connect_s3_2.png)
    * 설정후 저장!

5. 테스트 및 모니터링
    * `aws-lambda-thumbnail` 버켓에 아무 이미지나 업로드.
    * 그리고 `lambda`의 모니터링 -> CloudWatch에서 로그 보기
    * 최신 로그를 찾아 보면 아마도 에러가 났을 것이다.
    ![](/assets/aws/thumbnail/aws_lambda_monitoring.png)
    이유는 `Pillow`가 제대로 패키징 되지 않았기 때문, 이를 해결 하기위해 `Dokcer`를 사용해 보자. (EC2에서도 가능하다.)

### Step5 `Pillow`의 `import`에러를 잡아보자
1. `Dockerfile`과 `docker-compose.yml`파일 작성
    ```docker
    # Dockerfile
    FROM lambci/lambda:build-python3.6

    USER root

    WORKDIR /code
    ```
    ```docker
    # docker-compose.yml
    version: '3'

    services:
      env:
        build: .
        volumes:
          - ./:/code/
        command: bash -c "virtualenv env && source env/bin/activate && pip install pillow"
    ```
2. 빌드
    > 빌드 전 `DockerDestop`을 실행하여 주어야 한다.
    ```shell
    docker-compose build
    docker-compose up
    ```
    빌드를 하게 되면 프로젝트 폴더에 `env`라는 폴더가 생기게 되고 이곳의 `lib > python3.6 > site-package`에 `Pillow`이 설치가 된다   
    기존에 `requirements.txt`에 있던 `Pillow`를 빼고 `env`에 있는 `Pillow`를 압축하여 다시 실행 해
보자    
    그럴려면 `Makefile`을 조금 수정 해야 한다.

    ```shell
    clean:
      rm -rf pil pil.zip
      rm -rf __pycache__

    fetch-dependencies:
      mkdir -p lib/

    build-pil-package: clean fetch-dependencies
      mkdir pil
      cp -r src pil/.
      cp -r lib pil/.
      pip install -r requirements.txt -t pil/lib/.
      # 추가 된 부분 env에 있는 Pillow를 pil/lib에 넣고 lib를 압축
      cp -r ./env/lib/python3.6/site-packages/PIL pil/lib/.      
      cd pil; zip -9qr pil.zip .
      cp pil/pil.zip .
      rm -rf pil
      rm -rf lib
    ```

3. 다시 업로드
    * 압축한 파일을 다시 코드가 있는 버킷에 업로드 하자.
    * 업로드후 `lambda`의 s3파일 주소를 갱신 (어차피 똑같지만 새로고침)후 저장
    * 그리고 `aws-lambda-thumbnail`에 이미지를 한장 업로드 하고 기다림.
    * 조금후 `aws-lambda-thumbnail-resized`에 파일이 생성!
    * 혹시 에러가 날경우 CloudWatch로 가서 에러내용을 확인 해보자


이렇게 `s3`에 업로드 되는 이미지들을 `lambda`를 통해 `resizing` 하는 방법을 알아 보았다.
더 좋은 방법을 많고 여기서 본 방법은 매우 심플한 기본 예제 이다.


# 참고 사이트
<https://learn-serverless.org/post/deploying-pillow-aws-lambda/>
