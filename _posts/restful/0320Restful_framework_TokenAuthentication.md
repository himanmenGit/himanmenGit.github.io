# Authentication

인증은 들어오는 요청을 사용자 또는 서명된 토큰과 같은 식별 자격 증명 세트와 연관 시키는 메커니즘. 권한 및 제한 정책은 이러한 자격증명을 사용하여 요청을 허용 해야하는지 결정 할 수 있다.

`REST framework`는 여러가지 인증 스키마를 제공하며 사용자 정의 스키마를 구현 할 수도 있다.
인증은 항상 뷰의 맨처음 퍼미션과 스로틀링 검사를 하기 전에 이루어 진다.
`request.user` 속성은 일반적으로 `contrib.auth` 클래스 인스턴스로 설정된다.
`request.auth` 등록정보는 추가 인증 정보를 나타내는데 사용된다. 예를 들어서 요청이 서명된 인증토큰을 나타내는 데 사용될수 있다. 이것은 `BasicAuthentication`, `TokenAuthentication`, `SessionAuthentication`, `RemoteUserAuthentication` 의 인증 방식에 따른 정보들이 `request.auth`에 들어 있다는 것을 말한다.

인증 자체만으로는 들어오는 요청을 허용하거나 거부하지 않으며 단순히 요청이 이루어진 자격 증명을 식별한다. 유저에 대한 인증은 하지만 해당 유저에 대한 권한은 따로 지정 해야 한다는 것.

 인증 체계는 항상 클래스 목록으로 정의 되는데 REST 프레임워크는 목록의 각 클래스에 대해 인증을 시도 하고 성공적으로 인증 한 첫 번째의 클래스의 반환값을 사용하여 `request.user`및 `request.auth`를 설정한다. 장고의 인증 백엔드 설정과 비슷한 개념이다.
 
 클래스가 모두 인증 되지 않으면 `request.user` 는 유저가 `AnonymousUser`가 되고 `request.auth`는 `None`이 된다.
 
 인증되지 않은 요청에 대한 `request.user` 및 `request.auth`의 값은 `UNAUTHENTICATED_USER` 및 `UNAUTHENTICATED_TOKEN`설정을 사용하여 수정 할 수 있다.
 
 `django_rest_framework`는 기본적으로 `BasicAuthentication`와 `SessionAuthentication`을 사용한다. 추가하거나 제외 할 경우 `settings.py`에 아래에 해당하는 설정을 추가하거나 삭제 하면 된다.
 
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.RemoteUserAuthentication',
    )
}
```

인증이 실패하면 `HTTP_401_Unauthorized` 권한이 없으면 `HTTP_403_Permission_Denied` 에러가 난다.

### BasicAuthentication
`Authorization` 이라는 HTTP Header를 쓴다. `request.user`에는 장고 유저가 들어가고 `request.auth`는 `None`이 들어간다. 유저네임, 패스워드 외에는 추가 인증 정보가 없다는 것이다.


### SessionAuthentication
장고에서 세션을 쓰는 경우에는 백그라운드에서 로그인을 하는 순간 서버에는 세션이 저장되고 해당 세션에 해당하는 특정 키 값을 `SetCookie`라는 HTTP Header로 응답 해줘서 클라이언트에 쿠키로 저장되고 앞으로 해당 쿠키는 매 요청시마다 같이 가서 계속해서 유저인식이 가능 한것. 자동이다!

세션은 브라우저 전용이다.

### TokenAuthentication
토큰을 사용하는 경우 토큰값을 서버에서 직접 생성 하고 저장 해야한다. 그렇게 만들어진 값을 어떤 방법을 사용하던지 간에 클라이언트에 전달 해야 하고 클라이언트는 해당 토큰을 받아서 자기가 저장할 수 있는 임의의 공간에 저장 해 놓는다. 이후 요청을 보낼때 해당 토큰을 담아서 보낸다. 그 과정은 수동이다!

이 인증 체계는 간단한 토큰 기반 HTTP 인증 체계를 사용한다. 토큰 인증은 네이티브 데스크톱 및 모바일 클라이언트와 같은 클라이언트-서버 설정에 적합하다. 브라우저든 모바일 앱이든 모두 사용 가능 하다.

토큰 인증 스키마를 아요하려면 토큰 인증을 포함하도록 인증 클랙스를 구성 하고 django `INSTALLED_APPS`에 `rest_framework.authtoken`을 추가 해야 한다.
```
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
]
```
이렇게 하고 마이그레이션을 하면 토큰인증을 위한 테이블이 생성된다.

그리고 유저를 위해 토큰을 직접 만들어야 한다. 
토큰이라는 것은 유저를 나타내는것이 아니라 유저와 연결되어 있는 것이다. 그렇기 때문에 토큰을 가지고 인증을 진행하다가 토큰이 탈취 되어도 그것을 안순간 토큰을 삭제하면된다. 토큰을 삭제 한다고 해서 유저에게 큰 일이 생기지 않는다. 재 로그인 정도?
토큰을 만들고 싶다면 이렇게..
```
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print token.key
```

유저 정보를 받아 토큰을 생성하거나 가져와서 토큰을 보여주거나 유저가 없을 경우 인증 에러를 보여주는 코드
```
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView


class AuthTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key
            }
            return Response(data)
        raise AuthenticationFailed()
```
다른 방법으로는 `AuthtokenSerializer`를 사용하는 방법이 있다. 하지만 이 시리얼라이즈는 토큰을 생성하는 로직이 없기 때문에 해당 로직은 수동으로 넣어 줘야 한다.
```
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key
        }
        return Response(data)
```
시리얼라이즈의 `is_valid()`안에 `raise`를 발생시키는 루틴이 있기 때문에 `raise_exception=True`로 켜주면 유효성 검사 실패시 인증에러에 관한 오류를 반환한다.

만약 사용자정의 `APIException()`을 사용하고 싶으면 `APIException`을 상속 받은 클래스를 만들어사용 하면 된다.
```
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service ...'
    default_code = 'service ...
```
자주 쓰는 에러는 rest-framework에 미리 선언되어 있는것이 많다.

모델과 모델끼리 다대일, 다대다 관계의 경우에 시리얼라이즈로 관계를 표현하고 싶을 경우 해당 시리얼라이즈를 모델에서 만들어진 필드 이름 혹은 역참조 이름으로 변수를 만들고 해당 시리얼라이즈를 받아서 `fields`에 넣어 주면 된다.
```
from rest_framework import serializers

from members.serializers import UserSerializer
from .models import SomeModel


class SomeModelSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SomeModel
        fields = (
            'pk',
            'title',

            'users',
        )
```