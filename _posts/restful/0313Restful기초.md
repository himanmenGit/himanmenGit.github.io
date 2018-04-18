# Django REST_framework

## RESTful API
REST는 `Representational State Transfer` 의 약자. 분산 하이퍼미디어 시스템을 위한 소프트웨어 아키텍처의 한 형식. **웹에 있는 자원을 표시하는 방법.**

### 왜 필요 하나?
* 프론트엔드, IOS, Android등 모든 플랫폼에서 사용할 수 있도록 데이터만 전달하기위해 사용.
* Django에 기본적으로 내장 되어 있지 않기 때문에 따로 설치 해야 한다.


### 구성
* 자원(Resource) -URI
* 행위(Verb) - HTTP METHOD
* 표현(Representations) - 표현이 Restful 하다는 방식이 된다.
표현방식에 따라서 이 API가 어떤 역활을 하는지, 그 API에 어떤 행위를 보내면 어떤 자원에 대해서 무슨 행위를 할수 있는지 라는것을 나타냄.

#### REST API 규칙
* URI는 정보의 자원을 표현해야 한다.(리소스명은 동사보다는 명사를 사용)
* 자원에 댛한 행위는 HTTP Method(GET, POST, PUT, DELETE 등)로 표현
```
GET /membser/delete/1 (x)
DELETE /members/1 (o)
```
회원 정보를 가져 오는 URI
```
GET /members/show/1	(x)
GET /membets/1		(o)
```
회원을 추가 할 때
```
GET /members/insert/2	(x)
POST /members		(o)
```

#### HTTP METHOD 의 역활

|METHOD||
|------||
|POST| POST를 통해 해당 URI를 요청하면 리소스를 생성합니다.|
|GET| GET를 통해 해당 리소스를 조회합니다. 리소스를 조회하고 해당 도큐먼트에 대한 자세한 정보를 가져온다.|
|PUT|PUT을 통해 해당 리소스 전체를 수정 합니다.|
|DELETE|DELETE를 통해 리소스를 삭제 합니다.|
|PATCH|PACH를 통해 해당 리소스 일부를 수정 합니다.|

#### URI 설계시 주의점
* `/` 구분자는 꼐층 관게를 나타내는데 사용함.
* URI 마지막 문자로 `/`를 포함하지 않는다.
> 하지만 `Django` 는 마지막에 `/`를 넣는 것이 기본 규칙이다.
* URI에 밑줄 `_` 대신 하이픈 `-`을 사용한다.
* URI경로는 소문자를 사용한다.

이러한 방식으로 쉽게 설계를 할 수 있게 도와주는 것이 `REST framework` 이다.
