---
layout: post
title: "Django Models 13 Proxy Model"
categories:
  - Django
tags:
  - Django
---

# Proxy Model

다중 테이블 상속(Multi-table inheritance)을 사용하면 모델의 각 자식 클래스에 대해 새 데이터베이스 테이블이 만들어 진다. 자식 클래스는 부모 클래스에는 없는 추가 데이터 필드를 저장할 장소가 필요 하기 때문에 일반적으로 원하는 동작이다.

하지만 때로는 파이썬 수준의 동작만을 변경 하고 싶을 경우도 있다. 기본 매니저를 변경하거나 메서드를 추가 하는 정도 인것.

예를 들어 사용자(유저) 모델을 만들었는데 관리자와 일반 유저의 행동이 다른 경우에 관리자 불리언필드를 하나 주고 그 값에 따라서 기능을 수행 할 수 있지만 클래스가 너무 커지므로 효율적으로 기능만 분리 가능 하게 하는것이 `Proxy Model`이다

테이블 상에는 변화는 없지만 파이썬에서 테이블을 다루는 모델(관리자, 스태프, 일반유저)을 여러개 사용하고 싶을 경우

원래 모델에 대한 프록시를 만드면 프록시 모델의 인스턴스를 생성, 삭제, 업데이트를 할 수 있으며 원래 모델을 사용하는것 처럼 모든 데이터가 저장된다. 차이점은 원본을 변경하지 않고 프록시의 기본 모델 순서 또는 기본 매니저와 같은 것을 변경 할 수 있다는 것.

`Meta Class`에 `Proxy=True`를 설정하여 사용 할 수 있다.
```python
from django.db import models

__all__ = (
    'User',
    'Admin',
    'Staff',
)


class User(models.Model):
    name = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Admin(User):
    class Meta:
        proxy = True

    def drop(self, user):
        user.delete()

    def __str__(self):
        return f'{self.name} (관리자)'


class Staff(User):
    class Meta:
        proxy = True

    def block(self, user):
        user.is_block = True
        user.save()

    def __str__(self):
        return f'{self.name} (스태프)'
```
쉘에서 보면
```python
u1, u2, u3 = [User.objects.create(name=name) for name in ['장동건', '손지창', '기무라']]
# ..models.User
u1.__class__

admin = Admin.objects.get(name='장동건')
# ..models.Admin
admin.__class__

staff = Staff.objects.get(name='손지창')
# ..models.Staff
staff.__class__

staff.block(u3)
# True
u3.is_block

admin.drop(ue)
# 장동건 손지창
User.objects.all()
```
이렇게 기능별로 나누어 사용하면 실수할 가능성을 많이 줄일수 있고 매니저를 따로 두어 관리 할 수 도 있다.
```python
from django.db.models.manager import Manager

class User(models.Model):
    ...
    is_staff = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)

...

class AdminManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class Admin(User):
    objects = AdminManager()
    ...
    

class StaffManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)
        
        
class Staff(User):
    objects = StaffManager()
    ...
```
이런식으로 만들면 `get_query_set`을 통해 매니저에서 기본적으로 가져오는 쿼리셋을 변경 할 수 있다. 기본적으로 전체 데이터를 가져 오지만 프록시 모델에 기본 매니저를 재정의 하여 필터링을 한것을 기본으로 가져 온다.
```python
u1.is_admin=True
u1.save()
u2.is_staff=True
u2.save()

# <QuerySet [<Admin: 장동건 (관리자)>]>
Admin.objects.all()
# <QuerySet [<Staff: 손지창 (스태프)>]>
Staff.objects.all()
# <QuerySet [<User: 장동건>, <User: 손지창>, <User: 기무라>]>
User.objects.all()
```
프록시 모델에서도 `Meta`속성의 `ordering` 같은것을 사용할수 있다.
매니저를 여러개 가지고 있을 수도 있다.

`User`객체에 쿼리를 해서 `Admin` 이나 `Staff`객체를 꺼내는 것은 불가능 하다. 이것은 기존 모델을 대체하는 것이 아닌 다른 형태로 쓰기 위해 있는 방법이다. 결국 같은테이블을 쓰는 다른 클래스가 된다는 것.

프록시 모델을 정확히 하나의 비 추상적 모델 클래스를 상속 해야 한다. 프록시 모델은 다른 데이터베이스 테이블의 행 사이에 연결을 제공하지 않으므로 여러 비 추상적 모델을 상속받을 수 없다. 실제로 존재하는 테이블의 모델은 하나만 상속 받을 수 있다. 그리고 만약 `Abstract base class`에 필드가 아닌 메소드만 있을 경우에는 상속을 받을 수 있다. 실제 모델을 상속받은 프록시 모델이 존재 할경우 그 프록시 모델을 다시 상속 받는 형태로도 가능하다.

프록시 모델에 모델 매니저를 지정하지 않으면 모델 부모로부터 매니저를 상속 받는다. 프록시 모델에서 매니저를 정의 하면 부모 클래스에 정의 된 매니저는 꼐속 사용할 수 있지만 기본값이 된다.

만약 프록시 모델에 기본 매너지를 바꾸지 않고 새 관리자를 추가 하려면 새 관리자를 포함하는 기본 클래스를 작성하고 기본 클래스 다음에 상속 한다.