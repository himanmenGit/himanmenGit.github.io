# 인증과 권한
지금 까지 만든 API는 누구라도 편집, 삭제 할 수 있다. 고급 기능을 추가하고 싶다.
* 모델 인스턴스를 만든 사람과 연관이 있다.
* 인증 받은 사용자만 모델 인스턴스를 만들 수 있다.(데이터 베이스에 있는 유저)	
* 해당 모델 인스턴스를 만든 사람만 이를 편집하거나 삭제 할 수 있다.
* 인증 받지 않은 사용자는 '읽기 전용'으로만 사용 가능하다.

## 우선 유저 모델을 만들고 유저모델을 `SomeModel`에 추가하자.
```
# app
./manage.py startapp members

# members/models.py

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

# settings.py
8INSTALLED_APP = [
    ...
    'members',
]
AUTH_USER_MODEL = 'members.User'

# app
# db.sqlite3 지우고
# mighrations 들 지우고
./manage.py makemigrations
./manage.py migrate
```
SomeModel에 `owner`등록 
```
from django.conf import settings

owner = models.ForeignKey(settings.AUTH_USE_MODEL, related_name='somemodels', on_delete=models.CasCase
```

이제 사용자를 만들었으니 사용자를 보여주는 API도 추가 `members` 앱에 `serializers.py`추가
```
from django.contrib.auth import get_user_model
from rest_framework import serializers

from SomeApp.models import SomeModel

User = get_user_model()


class UserSErializer(serializers.ModelSerializer):
    somemodels = serializers.PrimaryKeyRelatedField(
        queryset=SomeModel.objects.all(),
        many=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'somemodel',)
```

그리고 유저에 대한 `generic View`를 만들어 준다.
```
from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import UserSerializer

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```
뷰에 대한 `ursl`를 연결 시켜 주자 `urls.py`를 만들고 연결
```
from django.urls import path

from .apis import UserList, UserDetail

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
```

지금까지 `somemodel`을 만들어도 해당 모델을 만든 사용자와 아무 관계도 맺지 않았다.
사용자는 직렬화된 표현에 나타나지 않았고, 요청하는 측에서 지정하는 속성 이었을 뿐이다.
지금 만약 `somemodel`을 API를 통해서 만들려고 하면 `NOT NULL constraint failed` 에러가 날 것이다. `owner_id`가 `NULL`이 아니기 떄문이고, `SomeModelSerializer`에 `fields`에 `owner`에 대한 정보가 없기 때문이다. `is_valid()`에서는 통과 했지만 `save()`호출시 `onwer`에 대한 정보가 없기 때문에 에러가 발생했다.
이를 해결 하기 위해 `perform__create()`를 써야 한다. 해당 함수는 `is_valid()`가 통과되고 나서 실행되는 함수로 이 함수를 `SomeModelList`에서 오버라이드 하여 추가 작업을 하고 저장하는 루틴으로 만들자.
```
class SomeModelList(..
    queryset = ...
    ...
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```
`owner`에 대한 정보를 넘어온 요청에 대한 사용자로 처리 하도록 한다. 하지만 만약 인증되어 있지 않은 유저로 해당 API를 실행할 경우 `AnonymousUser`라는 확인되지 않은 유저가 왔다고 에러가 난다.
일단 `SomeModelSerializer`에 `owner`에 대한 시리얼라이저를 읽기전용속성으로 만들어서 읽을수 있게하자.
```
class SomeModelSerializer(...
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        ...
        fields = (
            ...
            'owner',
         )
```
그리고 장고 어드민에서 SomeModel을 하나만들고 슈퍼유저를 해당 SomeModel과 연결 시켜 보자 그리고 GET API를 하면 유저가 같이 나오는 것을 볼 수 있다.

그리고 이제 인증 받은 사용자만 `SomeModel`을 생성/업데이트/삭제 해 보자,
특정 뷰에 대한 제한을 걸 수 있는 권한 클래스 중 하나인 `IsAuthenticatedOrReadOnly`를 넣자. 이것은 인증 받은 요청에 읽기와 쓰기 권한을 부여하고 인증 받지 않은 요청에 대해서는 읽기 권한만 부여 한다
`SomeModel List`에 다음 내용을 추가 하자
```
from rest_framework import permissions

permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
```

## django-rest-framework Authentication
기본적으로 두가지 인증 방식을 제공한다
`BasicAUthentication` 과 `SessionAuthentication`이다.
```
# settings.py
REST_FRAMEWORF = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAUthentication',
        'rest_framework.authentication.SessionAUthentication',
     )
}
```
장고 내에 자동적으로 적용되는 것들로 브라우저에서 유저 로그인을 한후 SomeModel을 하나 만들면 해당 유저에 대한 세션값으로 인해 SomeModel이 만들어 진다. 하지만 이것은 테스트용으로 사용하고 RestFul API 개발에는 쓰지 못한다. 세션과 쿠키는 브라우저에만 사용하는데 아이폰/안드로이드/프론트엔드에는 애매한 상황이 되기 때문이다. 그래서 획일화를 시켜서 인증 하는 방식인 `TokenAuthentication`을 사용한다.

> `BasicAUthentication`은 Http에 기본 인증 스킴으로 base64를 이용하여 인코딩된 사용자 ID/비밀번호 쌍의 인증 정보를 전달한다.
```
Authorization: Basic <base64로 인코딩된 username:password>
```

`TokenAuthenticataion`은 요청이 왔을때 특정 토큰 테이블을 사용하여 토큰을 요청하는 새로운 뷰를 만들어 사용하는 방식이다.
클라이언트가 HTTP `Authorization` Header에 Token을 담아서 보내면 해당 토큰을 분석해서 request.user를 할당.

`TokenAuthentication`
* 특정 유저가 토큰을 요청
* 서버는 해당 유저의 인증에 성공하면 토큰을 생성, 반환
* 유저는 받은 토큰을 자신의 저장소에 보관하고 매 요청마다 해당 토큰을 Header에 담아서보냄
* 서버는 받은 요청에 토큰과 관련된 Header가 있는지 검사후 request.user 할당

토큰을 쓰는 이유는 토큰에다가 특정 권한을 담을수 있다. 토큰에 일부 권한만 담아 발급하여 유저가 쓸수 있는 권한을 제약시킬 수도 있고, 만약 유저의 토큰들이 유출 되었을 경우 해당 토큰만 폐기하고 유저가 다시 접속 할 경우 다시 로그인만 하면 되기 때문에 보안상 좋다. 그리고 토큰은 사용자들이 억지로 임의의 기간마다 접속을 하게 할 수도 있다. 토큰에 인증 기간을 넣어 해당 기간안에 토큰을 탈취 당해도 기간이 지나면 토큰이 삭제되 무용지물이 된다.

이것은 기본값이 아니기 때문에 따로 설정 해주어야 한다. 

## 커스텀 권한 만들기
 객체의 소유자에게만 쓰기를 허용하고 다른 사용자는 읽을수 있기만 하는 권한을 만들어 보자
SomeApp 안에 `permissions.py`파일을 만들고 다음 내용을 입력
```
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
```

## StaitcHTMLRenderer
뷰에서 처리를 한후 응답을 할때 `HTML` 형식으로 리턴해주는 렌더러 해당 렌더러에 데이터를 넣으면 그 데이터로 이루어진 `HTML`을 불러준다. 파이썬 객체나 JSON이 아닌 HTML 문자열 자체를 반환해야 한다.

## 페이징 기능 추가하기 pagination
가장 쉬운 방법은 `settings.py`에 해당 코드를 넣는것이다
```
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
}
```
하지만 이것은 모든 API요청에 대해 적용되는 것으로 추천하지 않는 방법이고, 
추천되는 방법은 각 뷰마다 다른 페이징 기능을 적용 하는 것이다.
`pagination.py`를 만들고 
```
# pagination.py
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
```
한후 뷰에 적용
```
class SomeModelList(....
    ...
    pagination_class = StandardResultsSetPagination
```
이렇게 하면 요청시 3개씩 묶어서 오게 된다. 하지만 유저가 `page_size` 파라미터를 통해 `max_page_size`이상을 불러 올 경우 `max_page_size`로 고정되어 반환한다.