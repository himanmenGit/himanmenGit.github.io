---
layout: post
title: "Django Models 14 Proxy Custom Manager"
categories:
  - Django
tags:
  - Django
---

# Proxy Custom Manager

```
from django.db import models
from django.db.models import Manager


class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 커스텀 매니저
class NewManager(Manager):
    def get_queryset(self):
        print('NewManager get_queryset')
        return super().get_queryset()


# 커스텀 매니저를 직접 자신의 속성으로 갖는 MyPerson1
class MyPerson1(Person):
    secondary = NewManager()

    class Meta:
        proxy = True


# 커스텀 매니저를 속성으로 갖는 ABC Model
class ExtraManagerModel(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True


# 커스텀 매니저를 갖는 ABC 모델을 상속받은 MyPerson2
# (간접적으로 secondary라는 Manager를 갖게됨)
class MyPerson2(Person, ExtraManagerModel):
    class Meta:
        proxy = True

```

여기서는 `default_manager`가 기본값 입니다. `objects manager`는 상속되므로 계속 사용 할 수 있다.단지 기본값으로는 사용되지 않는다. 

 마지막으로 이 예제에서는 추가 매니저를 자식 클래스에 추가하려고 하지만 여전히 `AbstractBase`의 기본값을 사용한다고 가정. 자식 클래스에 새 매니저를 직접 추가 할 수는 없다. 기본 값을 무시 하므로 `AbstractBase class`의 모든 매니저를 명시적으로 포함해야 한다. 해결방법은 여분의 매니저를 다른 부모 클래스에 넣고 기본 값 다음에 상속해야 한다.
 
 ```
from inheritance.proxy_manager.models import *

MyPerson1.objects
# <django.db.models.manager.Manager at 0x7fc86f4a67b8>

MyPerson2.objects
# <django.db.models.manager.Manager at 0x7fc86f4a69b0>

MyPerson1.secondary
# <inheritance.proxy_manager.models.NewManager at 0x7fc86f4a6780>

MyPerson2.secondary
# <inheritance.proxy_manager.models.NewManager at 0x7fc86f4a69e8>

MyPerson1._default_manager
# <inheritance.proxy_manager.models.NewManager at 0x7fc86f4a6780>

MyPerson2._default_manager
# <django.db.models.manager.Manager at 0x7fc86f4a69b0>
 ```
 