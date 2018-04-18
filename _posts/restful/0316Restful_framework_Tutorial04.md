# mixin 사용하기
혼자서는 아무것도 하지 못하는 클래스 이지만 다른곳에 상속을 시켜서 추가 기능을 구현 하는 기능.
```
from rest_framework import mixins, generics

from ..serializers import SomeSerializer
from ..models import SomeModel


class SomeList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = SomeModel.objects.all()
    serializer_class = SomeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class SomeDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = SomeModel.objects.all()
    serializer_class = SomeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```
urls는 `api_view`와 동일한 `mixins.py`를 만들고 모듈 위치만 변경 해주면 된다.
```
from ..apis.mixins import *

urlpatterns = [
...
]
```
어떤 쿼리셋을 쓸지와 어떤 시리얼라이저를 쓸지를 정해 주고 `get`, `post`를 상속받은 `mixins` 클래스에 있는 기능을 사용. 이 `mixins`들은 `GenericAPIView`를 쓴다는 전제 하에 사용한다. 
쿼리셋과 시리얼라이저 클래스를 지정하는 것이 `GenericAPIView`에 있는 쿼리셋과 시리얼라이저클래스를 셋팅해놓고 믹스인 클래스들을 사용 하는 것이다.

# generic 사용 하기
`mixins`보다 더 추상화된 `generic`은 이미 안에서 `get`, `post` 등을 구현 해놓았기 때문에 쿼리셋과 시리얼라이저 클래스만 정해주면 모든 기본 행위들에 대한 요청을 알아서 처리 해준다.
```
from rest_framework import generics

from ..serializers import SomeSerializer
from ..models import SomeModel


class SomeList(generics.ListCreateAPIView):
    queryset = SomeModel.objects.all()
    serializer_class = SomeSerializer


class SomeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SomeModel.objects.all()
    serializer_class = SomeSerializer

```
```
from ..apis.generic import *

urlpatterns = [
...
]
```
엄청나게 간단 해졌다!