---
layout: post
title: "django-filters와 DRF의 filters 같이 사용하기"
categories:
  - Restful
tags:
  - Restful
---

프로젝트 막바지에 프론트엔드/IOS에서 사용하는 맵의 범위를 위/경도로 보내 주면
해당 위/경도 안에 있는 모든 숙소를 응답 해주어야 하는 기능을 만들어야 했다.

처음에는 단순히 `Q` 오브젝트를 사용하여 숙소를 필터링 한후 데이터를 보내주었다.
기능은 잘 동작 하였지만 이후 `DRF`의 `filter`기능을 알게 되어 리팩토링을 하는 도중
기본 `filter-backend`로는 내가 원하는 사용자정의 필터링을 만드는것이 힘들다고 생각하여
`django-filter`라는 라이브러리를 사용했는데 결과는 만족 스러웠다.

하지만 이후 추가기능인 `ordering`을 추가하는 과정에서 문제가 발생했다.
문제는 `django-filter`와 `DRF`의 기본 `filters`를 같이 사용하는 것에 대한 방법을 잘 파악하지 못했다.

두시간 정도 삽질후 해결 하였는데 

`filter_backends`에 명시적으로 `django_filters.DjangoFilterBackend`와 `OrderingFilter`를 등록 해주어야 한다.
`OrderingFilter`를 `filter_backends`에 등록할 때 `filter`를 등록 한다고 생각 하여 많이 헷갈렸는데
`OrderingFilter`는 `BaseFilterBackend`를 상속 받아 `filter_backends`에 등록이 가능 한것 같다.

그렇게 원하는 기능을 두개 같이 추가 함!


### installation
```bash
$ pip install django-filter
```

### settings
```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    ...
}

INSTALLED_APPS = [
    ...
    'django_filters',

    ...
]
```

### Using

```python
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
...

# django_filters의 filters.FilterSet 을 상속 받아 사용
class GpsFilter(filters.FilterSet):
    ne_lat = filters.NumberFilter(name='latitude', lookup_expr='lte')
    ne_lng = filters.NumberFilter(name='longitude', lookup_expr='lte')
    sw_lat = filters.NumberFilter(name='latitude', lookup_expr='gte')
    sw_lng = filters.NumberFilter(name='longitude', lookup_expr='gte')

    class Meta:
        model = House
        fields = (
            'ne_lat',
            'ne_lng',
            'sw_lat',
            'sw_lng',
        )


class HouseListCreateAPIView(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    pagination_class = DefaultPagination
    
    # 사용자 정의 필터 클래스
    filter_class = GpsFilter
    
    # 필터 백엔드를 명시적으로 둘다 등록을 해주어야 한다.
    # 아니면 settings의 DEFAULT_FILTER_BACKENDS만을 사용 하는것으로 생각 됨.
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    # ordering할 field명
    ordering_fields = ('pk', 'name',)
    # 기본 ordering
    ordering = ('created_date',)

    ...
```