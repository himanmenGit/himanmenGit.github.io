---
layout: post
title: "Django Models 7 ManyToMany 비대칭 재귀 참조"
categories:
  - Django
tags:
  - Django
---

# 서로 대칭이 되지 않는 ManyToMany 모델

`ManyToManyField` 는 기본적으로 서로 대칭이 되는 관계 이다. 이전에 본 페이스북 친구를 추가 할 경우 서로 친구가 되는 관계가 일반적인 경우 이다.

만약 자기 자신에게 MTM을 경우 `<model_lowcase>_set`을 사용하지 않는다. 대신 `ManyToManyField`는 대칭이라고 가정 한다. 

그런데 일반적엔 대칭관계를 원하지 않을 경우 `symmetrical=False`를 설정한다. 그러면 장고가 역방향 관계에 대한 설명자를 추가하게 되어 `ManyToManyField`관계가 비대칭이 되도록 설계 할 수 있다.

즉 친구추가를 할 경우 서로 친구가 되는것이 아니라 친구를 추가 한 쪽에서만 친구의 관계가 되는 것.

```
from django.db import models

__all__ = (
    'InstargramUser',
)


class InstargramUser(models.Model):
    name = models.CharField(max_length=50)
    following = models.ManyToManyField(
        'self',
        # 대칭관계가 아님
        symmetrical=False,
        # 역참조시 사용할 이름
        related_name='followers',
    )

    def __str__(self):
        return self.name
```
```
u1, u2, u3 = [InstargramUser.objects.create(name=name) for name in ['장동건', '손지창', '기무라']]
u1.following.add(u2)
u1.following.add(u3)
u1.following.all() # 손지창, 기무라

u2.followers.all() # 장동건 역참조를 사용한 u2를 팔로우 하고 있는 인스타그램 유저 목록 쿼

```