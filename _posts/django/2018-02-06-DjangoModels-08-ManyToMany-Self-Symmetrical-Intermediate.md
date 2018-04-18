---
layout: post
title: "Django Models 8 ManyToMany 비대징 재귀참조 중개모델"
categories:
  - Django
tags:
  - Django
---

# 대칭 관계가 아닌데 중개 모델을 사용하는 경우

자기 자신을 포함하는 `ManyToManyField`가 존재 하고 친구의 관계가 대칭이 아닐경우 그리고 이때 관계 테이블에서 `block`기능이 있을 경우에 대해 알아 보자

일단 `self`로 자신모델을 다 대다 필드로 가져야 하며 `symmentrical=False`로 비대칭을 적용한다. 그리고 서로 관계에 대해서 `block`할수 잇는 추가 적인 필드를 사용해야 하기 때문에 `through=`로 중개 모델을 사용한다. 그리고 중개 모델은 유저의 외래키를 가지며 현재 유저간의 관계유형을 표현할수 있는 필드를 하나 만든다

하지만 같은 모델에 대해 `ForeignKey`를 두개 쓰고 있기 때문에 역 참조시 어떤 모델을 참조해야 하는지에대한 부분이 불분명 해진다. 그래서 마이그레이션을 할 수 없다. 이 것을 해결하기 위해 `Relation`모델에 있는 각 `ForeignKey`들에 `related_name`을 지정 해 주어야 한다.


```
from django.db import models


class TwitterUser(models.Model):
    """
    내가 A를 follow 함
        나는 A의 follower
        A는 나의 followee
    A와 내가 서로 follow함
        나와 A는 friend
    Block기능이 있어야 함
    """
    name = models.CharField(max_length=50)

    relations = models.ManyToManyField(
        'self',
        # 비대칭 적용
        symmetrical=False,
        # 중개 모델 적용
        through='Relation',
        # 역참조를 없앰
        related_name='+'
    )


class Relation(models.Model):
    """
    유저간의 관계를 정의 하는 중개 모델
    """
    RELATION_TYPE_FOLLOWING = 'f'
    RELATION_TYPE_BLOCK = 'b'
    CHOICES_TYPE = (
        (RELATION_TYPE_FOLLOWING, '팔로잉'),
        (RELATION_TYPE_BLOCK, '차단'),
    )
    from_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        # 자신이 from_user인 경우의 Relation목록을 가져오고 싶은 경우
        related_name='relations_by_from_user',
    )
    to_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        # 자신이 to_user인 경우의 Relation목록을 가져오고 싶은 경우
        related_name='relations_by_to_user',
    )
    # 서로의 관계를 표현하기 위한 필드
    type = models.CharField(max_length=1, choices=CHOICES_TYPE)
```
이제 서로 관계를 생성해보자
```
u1, u2, u3, u4 = [TwitterUser.objects.create(name=name) for name in ['장동건', '손지창', '기무라', '타쿠야']]
# u1.relations.add(u2) # X 이건 실행 안됨.
# 중개 모델에서는 중개 테이블의 인스턴스를 직접 만들어야 함.

# u1이 u2를 follow한다.
 Relation.objects.create(from_user=u1, to_user=u2, type='f') 
 
# 혹은 from_user의 인스턴스에서 Relation을 역참조하여 바로 만들수 있다.
u1.relations_by_from_user.create(to_user=u3, type='f')
```
**u1이 팔로우 한 유저 목록을 받아옴**
```
u1.relations.all()
```
그런데 문제가 하나 있다. 이렇게 가져오면 `u1`과 관계된 유저 목록에서 상대방을 `follow`했는지 `block`했는지 구분 할 수가 없다. 그럴 경우 `TwiiterUser`모델에서 필터를 걸수 없다. 그래서 `Relations`모델에서 인스턴스를 가져와 필터링을 해야 한다

**u1이 from_user인 Relations를 모두 가져옴**
```
u1.relations_by_from_user.all()

```
**그중에 follow인 Relations와 block인 Relations를 가져옴**
```
# follow
u1.relations_by_from_user.filter(type='f')
# block
u1.relations_by_from_user.filter(type='b')
```
**u1이 follow하고 있는 유저 pk리스트**
```
u1.relations_by_from_user.filter(type='f').values_list('to_user', flat=True)
```
**이렇게도 사용할 수 있다.**
```
Relation.objects.filter(from_user=u1, type='f').values_list('to_user', flat=True)
```
이렇게 u1이 팔로우 하고 있는 유저 pk리스트를 가져 와서 유저를 쿼리필터를 통해 찾아 낼 수 있다.
```
u1_following_pk_list = u1.relations_by_from_user.filter(type='f').values_list('to_user', flat=True)
# <손지창>
TwitterUser.objects.filter(pk__in=u1_following_pk_list)
```
> `values`는 해당 쿼리셋에서 각각을 키/값 딕셔너리로 바꾸어 반환한다. 그리고 `values_list`는 딕셔너리가 아닌 리스트형태로 값들을 튜플로 만들어 리스트에 담아 반환한다. 여기에 원하는 필드만 지정하여 `values_list('pk')` 가져 올 수 있다. 그리고 `flat`은 가져오는 필드들을 주어진 요소가 하나라는 가정하에 튜플을 리스트에 담는것이 아닌 하나의 리스트에 요소들을 그냥 담아 주는 것이다.

```
# <Query Set[{'id':1, 'name':'장동건'}, {'id':2 ...
TwitterUser.objects.values()

# <Query Set[(1, '장동건'), (2, '손지창'), ...
TwitterUser.objects.values_list()

# <Query Set[(1, ), (2, ), ...
TwitterUser.objects.values_list('pk')

# <Query Set[1, 2, 3, 4]>
TwitterUser.objects.values_list('pk', flat=True)
```

이렇게 만들어진 쿼리문들을 이용하여 필요한 정보를 가져오는 프로퍼티를 만들 수 있다
```
class TwitterUser(models.Model):
    ....
    @property
    def following(self):
        """
        내가 follow하고 있는 TwitterUser목록을 가져옴
        """
        following_relations = self.relations_by_from_user.filter(
            type=Relation.RELATION_TYPE_FOLLOWING,
        )
        # 위에서 정제한 쿼리셋에서 'pk'값만 리스트로 가져옴( 내가 팔로잉하는 유저의 pk리스트)
        following_pk_list = following_relations.values_list('to_user', flat=True)

        # TwitterUser테이블에서 pk가 following_pk_list에 포함되는 User목록을
        # following_users변수로 할당
        following_users = TwitterUser.objects.filter(pk__in=following_pk_list)
        return following_users
```
이렇게 만들어진 프로퍼티를 사용하면 내가 팔로잉 하고 있는 유저의 목록을 가져 올 수 있다.
```
u1 = TwitterUser.objects.get(pk=1)
# 손지창 기무라
u1.following
```
나를 `follow` 하고 있는 유저 목록을 가져 오는 것
```
class TwitterUser(models.Model):
    ....
    @property
    def followers(self):
        follower_pk_list = self.relations_by_to_user.filter(
            type=Relation.RELATION_TYPE_FOLLOWING).values_list('from_user', flat=True)
        return TwitterUser.objects.filter(pk__in=follower_pk_list)
```
그리고 유저가 `to_user`를 팔로우 하는 함수를 만들어 보자
```
class TwitterUser(models.Model):
    ....
    def follow(self, to_user):
        """
        to_user 에 주어진 TwitterUser를 follow함
        """
        self.relations_by_from_user.create(
            to_user=to_user,
            type=Relation.RELATION_TYPE_FOLLOWING,
        )
```
사용은
```
u1.follow(to_user=u3)
```
유저를 `block`하고 싶다면
```
class TwitterUser(models.Model):
    ....
    def block(self, to_user):
        """
        to_user 에 주어진 TwitterUser를 block함
        """
        self.relations_by_from_user.create(
            to_user=to_user,
            type=Relation.RELATION_TYPE_BLOCK,
        )
```
```
u1.block(uo_user=u4)
```

유저가 `block`한 다른 유저 목록을 가져옴
```
class TwitterUser(models.Model):
    ....
    @property
    def block_users(self):
        """
        내가 block하고 있는 TwitterUser목록을 가져옴
        """
        blocking_pk_list = self.relations_by_from_user.filter(
            type=Relation.RELATION_TYPE_BLOCK).values_list('to_user', flat=True)
        return TwitterUser.objects.filter(pk__in=blocking_pk_list)
```
이렇게 하면 하나의 문제가 생기는데 내가 `follow`한 사람을 `block`시키면 두가지 상태를 모두 가지는 유저가 생기게 된다. `block`에 유저가 들어가면 `follow`관계가 없어져야 한다. 이것을 데이터 베이스 차원에서 제한을 걸어 줄 수 있다.
그리고 해당 관계의 생성 시간을 넣어 보자
```
class Relation(models.Model):
    ....
    created_date = models.DateTImeField(auto_now_add=True)
    class Meta:
        # from_user와 to_user의 값이 이미 있을 경우
        # DB에 중복 데이터 저장을 막음
        # ex) from_user가 1, to_user가 3인 데이터가 이미 있다면
        #       두 항목의 값이 모두 같은 또 다른 데이터가 존재 할 수 없음.
        unique_together = (
            ('from_user', 'to_user'),
        )
```
`unique_together`로 관계되는 컬럼의 중복을 막을수 있다.
그리고 `makemigrations`를 하면 무언가를 물어 볼텐데 이 것은 `created_date`가 새로 만들어 지면서 기존에 있던 `row`들에 새로만드는 필드에 대한 데이터를 어떻게 넣을 것인지 물어 보는 것이다. 기본적으로 `created_date`에는 `default`값이 없기 때문에 그렇다. 질문의 1번은 현재 넣을 값을 사용자가 직접 지정 하는 것이고 2번은 필드 속성에 `default`값을 넣어서 다시 `makemigrations`을 하는 것이다. 지금 별 데이터가 없으니 1번을 선택 하자.

그러면 또 질문이 나오는데 이것은 기존 `row`에 대해 어떤 값을 넣을지 물어 보는데 `default`값은 `timezone.now`이다. 다른 것을 넣고 싶으면 `datetime`도 사용 가능하다. 딱히 변할게 없으니 그냥 엔터를 쳐서 기본값으로 세팅 하자. 

이후 `migrate`를 하면 오류가 날 수도 있는데 이는 이미 `Relations`에 중복으로 맺어진 관계가 있기 때문이다. `ORM`으로 모든 `Relations`를 지우고 다시 `migrate`해보자. 그러면 잘 될 것이다.

그리고 같은 유저에 대해 `follow`와 `block`을 하려면 에러가 날 것이다.
# auto_now_add, auto_now
```
# 처음으로 객체가 만들어 지는 순간에만 현재 시간을 기록
created_date = models.DateTImeField(auto_now_add=True)
# 객체가 업데이트 될 때마다 시간을 재 기
modified_date = models.DateTImeField(auto_now=True)
```

마지막으로 내가 임의의 유저를 `follow`하고 있는지 임의의 유저가 나를 `follow`하고 있는지 확인하는 함수를 만들어 보자
```
class Relations:
    ....
    def is_followee(self, to_user):
        """
        내가 to_user를 follow하고 있는지 여부를 True/False로 리턴
        """
        return self.following.filter(pk=to_user.pk).exists()

    def is_follower(self, from_user):
        """
        from_user가 나를 follow하고 있는지 여부를 True/False로 리턴
        """
        return self.followers.filter(pk=from_user).exists()
```

### add(), create(), set(), clear()
`add()`는 `MTM`필드에 내용을 추가 하는 것이고
`create()`는 생성하는 것.
`set()`은 모두 지우고 다시 넣는것 
위 세개는 다 대다 중개 모델을 사용할 경우 사용 할 수 없는 것들이다.

`clear()`는 모두 지우는 것
이것은 사용할 수 있다.