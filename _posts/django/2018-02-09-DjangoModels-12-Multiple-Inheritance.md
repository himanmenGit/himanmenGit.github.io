---
layout: post
title: "Django Models 12 다중 상속"
categories:
  - Django
tags:
  - Django
---

# 다중 상속 (Multiple inheritance)

**다중 상속을 지원 하지만 많이 사용하지 말아라.**

파이썬의 서브 클래싱과 마찬가지로 장고 모델이 여러 부모 모델로부터 상속 받을 수도 있다. 만약 여러개의 부모 클래스를 가지면 왼쪽에서 부터 이름을 찾는다. 그래서 가장 기본이되는 (덮어 씌우려는 클래스)는 가장 오른쪽에 위치 해야 한다. 여러 부모가 있을 경우 첫 번째 부모(가장 왼쪽)의 메타 클래스가 적용된다.

하지만 일반적으로 여러 부모로 부터 상속하지 않아도 된다. 왜냐하면 `Mixin`이라고 하는 다중상속을 해도 상관없는 속성을 가진 클래스를 사용 하면 되기 때문이다.

### Mixin
`Mixin`은 클래스에 추가적인 속성이나 메소드를 제공하는것을 말함. 자체의 인스턴스 속성을 정의 하지 않으며 `__init__`생성자를 호출하도록 요구하지 않는다.

`Mixin`자체로는 아무런 일도 하지 못한다. 단순 메서드만 있거나 해당 메서도드 자식에 어떤속성이 있을 것이라는 가정하에 만드는 경우가 많다.

그런데 장고 믹스인은 상속받은 모든 클래스에 특정 추가 필드나 메서드를 추가 할 수 있다. 그리고 상속 계층을 가능한 간단하고 직관적으로 유지하여 특정 정보가 어디에서 왔는지 알아내려고 노력하지 않아도 되도록 해야 한다.

공통 `ID` 기본 키 필드가 있는 여러 모델을 상속하면 오류가 발생한다. 다중 상속을 적절하게 사용하려면 부모 모델에서 명시적으로 `AutoField`를 사용하여 오류를 막을수 있다.
하지만 해당 사용법은 관리하기가 힘드므로 사용하지 않기를 권한다.
```
from django.db import models


class Article(moedls.Model):
    article_id = models.AuthField(primary_key=True)
    ...
    
    
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    ...
    
    
class BookReview(Book, Article):
    pass
```
아니면 공통 조상을 사용하여 자동 필드를 유지한다. 이렇게 하려면 자동으로 생성되고 자식에서 상속되는 필드 사이의 충돌을 피하기 위해 각 부모 모델에서 공통 조상을 명시적으로 `OneToOneField`를 사용해야 한다.
```
from django.db import models


class Piece(models.Model):
    pass


class Article(Piece):
    artist_piece = models.OneToOneField(
        Piece,
        on_delete=models.CASCADE,
        parent_link=True
    )


class Book(Piece):
    book_piece = models.OneToOneField(
        Piece,
        on_delete=models.CASCADE,
        parent_link=True
    )


class BookReview(Book, Article):
    pass
```
이렇게 만들면 다이아 몬드형 상속 구조가 나타난다.
만약 `BookReivew`를 하나 만들게 되면 연결되어진 모든 모델의 테이블에 데이터를 만들어지게 된다.

### 필드 네임의 숨김은 허용 되지 않는다.
일반적인 파이썬 클래스 상속에서는 자식 클래스가 부모 클래스의 모든 특성을 재정의 할 수 있다.
하지만 장고에서는 일반적으로 모델 필드에서는 상속을 받았을때 해당 필드를 재정의 할 수 없다.
왜냐하면 해당 필드는 데이터베이스의 컬럼이름이고 `OneToOneField`에서는 동일 한 필드명을 사용할수 없기 때문이다.

하지만 `Abstract base model`에서 상송됙 모델 필드에는 적용되지 않는다. 이 모델을 테이블로 존재 하지 않고 단순 데이터만 가지고 있기 때문에 필드에 대한 정의를 바꿀수도 있고 `None`을 사용하여 없앨수도 있다.

이런 상속에 대한 제한은 `Field`인스턴스 인 속성에만 해당한다. 원하는 겨웅 일반 파이썬 속성을 재정의 할 수 있다. 