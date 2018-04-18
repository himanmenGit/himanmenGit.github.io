# Django RESTful framework Tutorial 01

* python dict는 JSON Serialize 변환이 가능하다. 하지만 query_set은 안된다.
* Serialization(직렬화) - 데이터 스토리지 문맥에서 데이터 구조나 오브젝트 상태를 동일하거나 다른 컴퓨터 환경에 저장 하거나 나중에 재구성할 수 잇는 포맷으로 변환하는 과정.
> 파이썬 객체를 어딘가로 전송할 수 있는 방법이 없다. 특정한 형태로 데이터를 변환해서 저장하거나 전송해서 상대가 받아서 다시 쓸수 있는 데이터로 만들수 있어야 한다. 데이터를 저장하거나 전송하기 위해서 특정 형태(전송이 가능한형태)로 바꿔주는 것.
* json은 가장 일반적이고 대부분의 언어에서 파싱하여 데이터를 복원하는데 큰 문제가 없기 때문에 많이 사용한다.

### 설치
```
pip install djangorestframework
```
`INSTALLED_APPS`에 등록
```
...
'rest_framework',
```

전송하고 싶은 데이터의 모델을 직렬화 시켜주는 모듈을 만들어야 한다. 직렬화를 하고 싶은 모델이 있는 앱에 `serializers.py`라는 모듈을 만들고 해당 모델을 직렬화 시키켜주는 코드를 작성하자.
```
from rest_framework import serializers
from .models import SomeModel


class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeModel
        fields = '__all__'
```
`ModelSerializer`는 `rest_framework` 에서 지원 해주는 특정모델을 전송에 필요한 형식으로 바꿀수 있도록 제공해 주는것으로 이것을 사용하여 `SomeModel`의 모든 필드를 사용 하겠다고 선언함.
그러면 해당 시리얼라이저를 통해 인스턴스나 쿼리셋을 넣게 되면 모든 필드에대한 값이 자동적으로 직렬화가 되게 된다.

그리고 이 시리얼라이저를 사용할 수 있는 부분이 제한되어 있다. 사용하기 위해서는 rest_framework에서 제공하는 `APIView`를 사용해야 하며, 이 뷰는 클래스 기반이다. 그리고 함수기반 뷰는 사용 할 수 없다. 
사용방법은 데이터를 받는 방식의 함수를 선언해주면 된다.
```
from rest_framework.response import Response
from rest_framework.views import APIView
from ...serializers import SomeModelSerializer
from ...models import SomeModel

class SomeView(APIView):
    def get(self, request):
	    somemodels = SomeModel.objects.all()
	    serializer = SomeModelSerializer(somemodels, many=true)
	    return Response(serializer.data)
    def post(self, request):
        ...
```
`somemodels`의 쿼리셋을 시리얼라이저에 전달하여 모든 쿼리셋에대한 모든 필드를 직렬화 시킨 시리얼라이저를 생성시키고 데이터꺼내서 rest_framework의 Response를 사용하여 반환한다.

이렇게 만들어진 뷰를 urls에 연결 해야 하는데 클래시 기반 뷰는 클래스 기반 자체가 실행할 수 있는 함수가 아니다. 그래서 클래스 기반 뷰의 기본을 상속받은 뷰는 `as_view()`라는 함수를 가지는데, 이 함수를 이용하여 해당 클래스뷰에 대한 동작을 만들수 있는 함수가 반환한다.
```
form .veiws import SomeView

urlpatterns = [
    path('some/', SomeView.as_view(), name='some-view')
]
```