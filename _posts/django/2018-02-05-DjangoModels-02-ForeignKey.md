---
layout: post
title: "Django Models 2 ForeignKey"
categories:
  - Django
tags:
  - Django
---

## 관계 (Relationships)
관계형 데이터베이스의 힘은 테이블을 서로 연관시키는데 있다. 장고는 다 대일, 다 대다, 일대일 데이터 베이스 관계의 세 가지 가장 일반 적인 유형을 정의 할수 있는 방법을 제공 한다.

속도는 키-벨류형 데이터베이스가 빠르지만 서로관의 관계를 표현하기에 적절하지 못하며 속도에 최적화 되어 있다. 반면에 관계형 데이터 베이스는 저장 용량을 아끼는데 최적화 되어 있다. 


### 다 대일 (Many-to-one relationships)
다 대일 관계를 표현하려면 장고 모델의 `django.db.models.ForeignKey`를 사용 하면 된다.
`ForeignKey`는 위치 인수가 필요하다. 모델이 관련된 클래스 이다.
만약 자동차와 제조회사가 있는 경우 제조업체가 여러 자동차를 생산하지만 각 자동차에는 하나의 제조 업체가 있는 경우를 만들어 보면
```python
from django.db import models


class Manufacturer(models.Model):
    name = models.CharField('제조사 명', max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name='제조사'
    )
    name = models.CharField('모델명', max_length=60)

    def __str__(self):
        return f'{self.manufacturer.name} {self.name}'
```
```
samsung = Manufacturer.objects.create(name='아우디')
sm3 = Car.objects.create(manufacturer=samsung, name='sm3')

# 자동차 에서 제조사를 가져 올 경우
print(sm3.manufacrurer.name) # 아우디
# 제조사에서 자동차를 가져 올 경우
print(samsung.car_set.first().name) # sm3
```