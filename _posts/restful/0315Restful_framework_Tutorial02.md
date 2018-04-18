### Serializer 클래스 만들기
직렬화 하고 싶은 필드를 직접 입력 할 수도 있다.
`Create`와 `update`라는 메소드가 들어 가야 한다. 이 메소드들은 시리얼라이저는 파이썬 객체를 직렬화 할때도 쓰지만 JSON데이터가 들어 왔을때 그 데이터를 이용해 다시 파이썬 객체로 만들때 사용한다.
외부 데이터를 사용해서 장고에 있는 데이터 베이스 내용을 바꾸거나 추가 하고 싶을때도 시리얼라이즈를 사용한다. `Create`를 이용하여 특정 모델에 받은 데이터를 이용해 생성 해주거나 `update`를 통하여 특정 인스턴스를 와 받은 데이터를 통하여 해당 인스턴스의 데이터를 수정한다.

```
class SomeSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializes.CharField(required=False, allow_blank=True)
    ...
    
    
    def create(self, validated_data):
        return SomeModel.objects.create(**validated_data)
        
        
    def update(self, instance, validated_Data):
        instance.title = validated_data.get('title', instance.title)
        ...
        instance.save()
        return instance
```

하지만 배우는 쪽에서는 ` ModelSerializer`를 많이 사용한다.

### ModelSerializer
`serializer`클래스보다 간단하게 모델의 정보를 직렬화 할수 있다.
단순히 `Seirializer`의 단축 버전이며 필드를 자동으로 인식한다. 그리고 `create()`메서드와 `update()`메서드가 이미 구현되어 있다.
```
class SomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeModel
        fields = ...
```

### SomeSerializer를 사용하는 View만들기
이전에는 `request`에서 데이터를 다룰때 `request.POST`로 전달된 데이터를 다루거나 `request.GET`으로 전달된 데이터를 다뤘는데 `rest_framework` 에서는 `request.data`로만 데아터를 다룬다. 이렇게 사용하는것이 훨씬 편하다.
그리거 `Response`도 `HttpResponse`를 상속받은 `TemplateRespinse` 타입이며, 렌더링 되지 않은 콘텐츠를 불러와 클라이언트에게 ㅇ리턴할 콘텐츠 형태로 변환한다.

#### API뷰 감싸기
REST 프레임워크는 API 뷰를 작성하는데 사용할 수 있는 두가지 래퍼를 제공.
* @api_view 데코레이터를 함수 기반 뷰에서 사용할 수 있다.
* APIView 클래스는 클래스 기반 뷰에서 사용 할 수 있다.
우리는 클래스 기반뷰 에서 사용하는 것만 알아 보자.
```
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SomeSerializer
from .models import SomeModel


class SomeList(APIView):
    def get(self, request):
        somemodels = SomeModel.objects.all()
        serializer = SomeSerializer(somemodels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```
```
# urls.py
urlpatterns = [
    path('sonelist/', SomeList.as_view(), name='some-list'),
]

```
형태는 `ModelForm`과 비슷하게 생겼다. `SomeSerializer`를 `form`이라고 생각하면 된다. 
