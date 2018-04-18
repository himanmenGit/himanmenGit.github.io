# 뷰셋과 라우터

### 뷰셋

뷰셋은 뷰들을 합치고 URL들을 합친 것을 말한다.
```
# views/viewsets.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from ..permissions import IsOwnerOrReadOnly
from ..serializers import SomeModelSerializer
from ..models import SomeModel


class SomeModelViewSet(viewsets.ModelViewSet):
    queryset = SomeModel.objects.all()
    serializer_class = SomeModelSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def highlight(self, request, *args, **kwargs):
        somemodel = self.get_object()
        return Response(somemodel.highlighted)
```
`viewsets.ModelViewSet`은 모든 `mixins` 모델을 상속 받기만 한다. 하지만 `get`에 대한 요청이 애매해진다. 해결방법은 뷰에대한 함수를 정해주는데 요청한 종류에 따라 뷰를 분리 시켜 각각 적용 시켜 준다.
```
# urls/viewsets.py
from django.urls import path
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

from ..apis.viewsets import SomeModelViewSet

somemodel_list = SomeModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
somemodel_detail = SomeModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

somemodel_highlight = SomeModelViewSet.as_view({
    'get': 'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = [
    path('', somemodel_list, name='somemodel-list'),
    path('<int:pk>/', somemodel_detail, name='somemodel-detail'),
    path('<int:pk>/highlight/', somemodel_highlight, name='somemodel-highlight')
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

### 라우터
`View`클래스 대신 `ViewSet`클래스를 사용했기 때문에 `URL`도 설정할 필요가 없다. `Router`클래스를 사용하면 뷰 코드와 뷰, `URL`이 관례적으로 자동 연결된다. 단지 뷰를 라우터에 적절히 등록 시켜주기만 하면된다. 
```
# routers.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..apis.viewsets import SomeModelViewSet

router = DefaultRouter()
router.register(r'', SomeModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```

모든 url 요청 서빙
```
    ....
    path('viewsets/', include('SomeApp.urls.viewsets')),
    path('routers/', include('SomeApp.urls.routers')),
```

뷰셋은 유용한 추상화이다. API 전반에 걸쳐 일관적인 URL을 구현 할 수 있고 코드양은 최소한으로 유지 할수 있어서 URL설정에 낭비될 비용을 API상호 작용과 표현 자체에 쏟을 수 있다.

뷰셋은 생산성이 증가하나 명확함이 좀 약해진다 
보완법으로는 주석을 잘 달아야 한다!