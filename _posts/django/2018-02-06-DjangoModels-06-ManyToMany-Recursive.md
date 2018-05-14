---
layout: post
title: "Django Models 6 ManyToMany 재귀참조"
categories:
  - Django
tags:
  - Django
---

# ManyToMany 중개 모델을 사용한 재귀모델

자기 자신을 `ManyToManyField`로 `self`를 가지는 형태의 모델

가장 일반 적인 모델인 페이스북를 예로 들어 보면 자신을 상대로 한명의 친구를 추가 하면 서로 친구인 관계가 된다. 한마디로 `나는 너의 친구 == 너는 나의 친구`
```python
from django.db import models

__all__ = (
    'FacebookUser',
)

	
class FacebookUser(models.Model):
    name = models.CharField(max_length=50)
    friends = models.ManyToManyField('self')
	
    # 친구의 목록을 보여줌
    def __str__(self):
        return '{name}의 친구({friend})'.format(
            name=self.name,
            friend=','.join(self.friends.all().values_list('name', flat=True))
        )
```
**Shell에서 여러명의 페북 유저를 만드는 방법 리스트컴프리헨션을 사용해보자**
```python
f1, f2, f3 = [FacebookUser.objects.create(name=name) for name in ['장동건', '손지창', '기무라']]

f1.friends.add(f2)

f1.friends.all() # 손지창
f2.friends.all() # 장동건
```
이렇게 하면 한명이 친구를 추가 하면 다른 한명은 자연스레 서로 친구의 관계가 형성된다.