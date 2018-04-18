---
layout: post
title: "Django Models 5 ManyToMany 중개모델"
categories:
  - Django
tags:
  - Django
---

### 다 대다 관계에 있는 추가 필드 (Extra fields on many-to-many relationships)

유저가 글에 좋아요를 표시 하는데 단순히 좋아요만 표시 하는 것이 아닌 좋아요 한 시간정보 까지 저장 하고 싶을 경우 장고는 다 대다 관계를 관리하는 데 사용될 모델을 지정 할 수 있다. 이것을 중개 모델이라고 부른다. 중개 모델은 `throuthTo`인수를 사용하여 중개자 역활을 하는 모델을 가리키는 `ManyToManyField`오 연결된다.


중개 모델을 설정할 때, 다 대다 관계에 관여하는 모델에 `foreign key`를 명시적으로 지정한다. 이 명시적 선언은 두 모델이 관련되는 방식을 정의 한다.

중개 모델을 사용할 경우 몇가지 제한 사항이 있다.
* 중개 모델에는 소스 모델에 대한 외래 키가 하나만 포함되어야 한다. 같은 모델에 대한 `foreign key`가 오직 한개 여야 한다. 어떤 모델인지 확인하기 어렵기 때문이다. 만약 부득이 하게 같은 모델을 하나의 모델에서 `foreign key`로 명시 할 경우 `ManyToManyField.through_fields`를 사용해야 한다. 이는 관여된 모델의 이름을 명시적으로 지정 하는 것으로 장고 내부에서 자동으로 만들어 지는 참조 이름을 명시하여 해당 같은 모델을 구분할 수 있게 한다.
만약 둘 이상의 같은 `foreign key`가 있고 `through_fields`가 지정되지 않은 경우 유효성 검증 오류가 발생한다. 

소스 모델은 `MTM`이 정의된 곳을 말한다.
대상 모델은 연결된 다른 모델을 말한다.
```
class Post(models.Model):
    title = models.CharField(max_length=50)
    like_users = models.ManyToManyField(
        'User',
        through='PostLike',
    )

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_date = models.DateTimeField(
        auto_now_add=True,
    )	
```
일반적인 `MTM`필드의 새로 생성된 테이블과 동일한 모습에 `created_date` 필드만 하나 추가 되었을 뿐이다.
그리고 `Post`에 대한 `User`의 `PostLike`관계를 맺고 싶다면 일반적인 `MTM`필드에서 사용하는
`add`를 사용하는 형태로는 불가능 하다 이런 경우 중개 모델을 직접 만들어 줘야 한다. 
```
post.like_users.add(user) # X 불가능
PostLike.objects.create(post=pose, user=user) # O 이렇게 사용해야 한다.

# post에 좋아요를 누른 사람
post.like_users.all()

# 유저가 좋아요를 누른 post
user.post_set.all()
```

그런데 `user`가 가지고 있는 `post`를 가져 올 때 `post_set`이라는 명령어가 말이 좀이상하다고 생각되면 `related_name`으로 역방향 이름을 재정의 할 수 있다. 
```
class Post(...
    ....
    related_name='like_posts',
```
```
user.like_posts.all()
```