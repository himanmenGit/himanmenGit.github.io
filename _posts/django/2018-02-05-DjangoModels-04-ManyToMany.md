---
layout: post
title: "Django Models 4 ManyToMany"
categories:
  - Django
tags:
  - Django
---

### 다 대다 (ManyToMany relationships)

서로 여러개의 관계를 가지는 형태. A모델이 B모델을 가질 수 있고 B모델도 A모델을 여러개 가질 수 있는 것.
`many-to-many`관계를 정의 하려면 `ManyToManyField`를 사용한다. 다른 필드 와 마찬가지로 모델의 클래스 속성으로 포함하여 사용 한다.
그리고 다 대다 관계도 재귀관계를 만들 수 있다.

예를 들면 어떤 글의 좋아요를 누르게 되면 해당 글에 어떤 사람이 좋아요를 눌렀는지 가지고 그 사람은 여러 글에 좋아요를 할 수 있다.
피자는 여러 종류의 토핑을 가질 수 있다.
토핑은 여러 종류의 피자에 올라 갈 수 있다.
일반적인 다 대다 관계를 처리할 경우 `ManyToManyField`만 있으면 된다. 
그리고 `MTM`의 이름은 관련 모델 객체 세트를 설명하는 복수형으로 제안되지만 필수는 아니다.
`MTM`필드가 어디에 있는지는 중요하지 않지만 두 모델중 하나에만 있어야 한다.
어느 쪽이 주가 되는 의미인지에 따라 주가되는 모델에 필드를 정의 하는게 좋다.
```
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name
```

```
masterPizza = Pizza.objects.get(name='마스터피자')
masterPizza.toppings.all()
# 치즈, 피망, 불고기, 파인애플...
cheeseTopping = Topping.objects.get(name='치즈')
cheeseTopping.pizza_set.all()
# 치즈피자, 하와이안피자, 불고기피자...
```
이렇게 생성한 테이블중 다 대다 관계를 표한하는 테이블이 새로 생성되는데 여기는 3개의 필드가 존재 한다. `id`필드 `pizza_id`, `topping_id` 각각 `Row`의 `pk`, 피자의 `pk`, 토핑의 `pk` 다른 모델의 인스턴스의 `pk`값만으로 서로의 관계를 연결 하고 있다.

이렇게 단순한 관계일 경우는 일반적인 `ManyToManyField`로 끝나지만 만약 두 모델간의 관계에 데이터를 연결해야 할 경우가 생길 수도 있다.

이런 경우에는 중계 테이블을 만들어 `ManyToManyField`를 만들어서 사용 해야 한다.