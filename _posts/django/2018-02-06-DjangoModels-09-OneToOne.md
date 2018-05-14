---
layout: post
title: "Django Models 9 OneToOne"
categories:
  - Django
tags:
  - Django
---
# 일 대 일 관계 모델 (One-to-one Relationships)

기존의 데이터는 그대로 두고 확장할 때 사용 할 수 있다.
첫번째 인자로 모델 관련 클래스가 필요하다.
예를 들어 `place`에 대한 DB를 구축 했다면 DB에는 주소, 전화번호 등과 같은 표준적인 데이터만 만들 수 있다. 그런 다음 레스토랑 DB를 구축하고 레스토랑은 `place`를 가지게 되는것 이다. 한장소에 여러 레스토랑이 있으면 안된다는 가정을 하고 해당 레스토랑은 어떤 레스토랑이며 어느 장소에 있는지를 일 대 일 관계로 연결 시켜 준다.

재귀 관계 모델도 사용가능 하다.
 
기본적인 일대일 관계를 장소와 레스토랑 그리고 웨이터로 표현하면 이렇게 된다.
```python
from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.name} the place'


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.place.name} the restaurant'


class Waiter(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} the watier at {self.restaurant.place.address}'

```
객체를 만들때 장소에 붙어 있는 레스토랑을 만들고 싶은경우 `ForeignKey`와 흡사 하게 만든다
```python
p1 = Place.objects.create(name='Demon Dogs', address='944 W. Fullerton')
p2 = Place.objects.create(name='Ace Hardware', address='1013 N. Ashland')

r = Restaurant.objects.create(
    place=p1,
    serves_hot_dogs=True,
    serves_pizza=False,
)
```
그리고 레스토랑과 장소의 관계를 기본적으로 접근 하는 방법을 보자.
```python
# 레스토랑에서 장소 접근 가능
# <Place: Demon Dogs the place>
r.place

# 반대로 장소에서 레스토랑 역 참조 가능
# 이 경우 참조하는 객체가 하나 이기 때문에 <class_name_lowercase>_set이 아니라 
# 그냥 <class_name_lowercase>를 쓴다
# <Restaurant: Demon Dogs the restaurant>
p1.restaurant
```
그리고 실제 데이터베이스에 있는 데이터를 `OneToOne`모델로 참조 해야 한다.


### hasattr()
속성이 있는지 확인 할수 있는 함수
```python
# True
hasattr(p1, restaurant')
# False
hasattr(p2, restaurant')
```
 