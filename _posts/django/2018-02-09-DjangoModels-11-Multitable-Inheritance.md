---
layout: post
title: "Django Models 11 다중 테이블 상속"
categories:
  - Django
tags:
  - Django
---

# Multi-Table inheritance

장고가 지원하는 모델 상속의 두 번째 유형으로 계층 구조의 각 모델이 모두 하나의 모델 일 때 이다.
이전에 봤던 `Abstract base classes`과 정 반대 이다. 추상 기본 클래스에서는 추상 모델이 하나의 테이블이 되지 않았지만 `Multi-table inheritance`에서는 부모도 테이블을 가지며 개별적으로 쿼리하고 생성이 가능하다. 상속 관계는 자동으로 생성 된 `OneToOneField`를 통해 자식 모델과 각 부모간의 링크를 도입한다.

`Multi-table inheritance`를 하면 부모와 자식을 `OneToOneField`로 자동으로 연결 시켜 준다.
그래서 자식을 하나 만들 때 마다 부모의 `OneToOne`필드에 자식의 `pk`를 만들고 가리키게 된다.
문제는 속성을 접근 할 때마다 테이블을 거쳐 가는것인데 만약 여러 단계의 상속을 했다면 속도 상으로 매우 좋지 않다. 속성을 하나 탐색 할 때마다 상속된 테이블을 모두 거쳐 가기 때문에 매우 느리다. 대부분 한 두단계 정도만 상속을 하는것을 추천하다.

이 모델의 장점을 부모 모델에 대해 직접 쿼리가 가능 하다는 것이다. 자식 모델에 대한 공통된 정보를 가져오기에 편리하다.

```
from django.db import models

__all__ = (
    'Place',
    'Restaurant',
)


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.name} | {self.address}'


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f'Restaurant {self.name} | {self.address}'
```

레스토랑을 만들어 보자
```
#<Restaurant: Restaurant 맥도날드 | 신사역>
Restaurant.objects.create(name='맥도날드', address='신사역', serves_hot_dogs=True)
```
이렇게 만들어진 모델의 자동으로 생성된 `OneToOneField`는 이렇게 생겼다
```
place_ptr = models.OneToOneField(
    Place, on_delete=models.CASCADE,
    # 이 필드가 부모와의 링크를 나타내기 위해 존재 한다는걸 표현함
    parent_link=True,
)
```
`parent_link=True`인 `OneToOneField`를 직접 새로 만들면 자동으로 생성되는 위의 필드가 생기지 않는다.

### Meta and Multi-table inheritance
다중 테이블 상속 상황에서 자식 클래스가 부모의 `Meta`클래스에서 상속 받는 것은 의미가 없다. 모든 메타 옵션은 이미 상위 클래스에 적용되었고 다시 적용하면 모순된 행동 만 발생 시킨다.

따라서 자식모델은 부모의 메타 클래스에 액세스 할 수 없다. 그러나 자식이 부모로부터 동작을 상속 하는 몇가지 제한된 경우가 있다. `ordering`이나 `get_latest_by`특성을 지정하지 않으면 해당 특성은 부모로부터 상속 한다.

다중 테이블 상속은 암시적으로 `OneToOneField`를 사용하여 부모와 자식을 연결하기 때문에 부모에서 자식으로 이동 할 수 있다. 그러나 이는 `ForeignKey`, `ManyToManyField` 관계에 대한 기본 `related_name`값인 이름을 사용한다. 이러한 관계 유형을 부모모델이 자식 모클래스에 배치하는 경우 해당 필드 각각에 `related_query_name` 특성을 지정 해야 한다. 잊어버리면 장고는 `Reverse query name` 이 충돌하여 유효성 검사오류를 발생 시킨다.

`OneToOneField`는 `related_name`과 `related_query_name`이 같다. 그래서 만약 자식 모델에 `ForeignKey`나 `ManyToManyField`에 `related_query_name`이 없을 경우 해당 모델의 부모와 관계형 필드들이 가지고 있는 `related_query_name`이 충돌한다. 