---
layout: post
title: "Django Models 3 ForeignKey 재귀참조"
categories:
  - Django
tags:
  - Django
---

# ForeignKey Recursive

또한 재귀관계와 아직 정의되지 않은 모델과의 관계를 만들 수 도 있다. 
재귀관계란 자기 자신과 다 대일 관계를 갖는 객체 관계를 말한다. 예를들어 `Person`이 선생님 일수도 있고 학생일수도 있을 경우를 만들어 보자 `'self'`를 사용하여 만들 수 있다.
```
class Person(models.Model):
    name = models.CharField(max_length=60)
    teacher = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
```
```
lhy = Person.objects.create(name='이한영')
himanmen = Person.objects.create(name='박수민1', teacher=lhy)
himanmen2 = Person.objects.create(name='박수민2', teacher=lhy)
```
이런 경우 선생님은 선생님 자신을 가지는 형태를 취한다. 그리고 선생님과 관계된 학생들(Person)을 가져 올때는 역 참조를 사용할 수 있다.
```
lhy.person_set.all()
```

그리고 코드가 정의 되는 시점에 관계하는 클래스가 해당 클래스 보다 뒤에 정의 될 경우 해당 클래스 이름을 문자열로 감싸서 참조 할 수 있다.

그리고 다 대다, 다 대일 관계의 경우에 관계를 만들기 위해 만들어지는 인스턴스에는 단순히 올바른 객체만 넣어도 관계가 형성된다. 테이블에 데이터가 들어 간다.

그리고 `on_delete=models.SET_NULL`은 해당 인스턴스가 삭제 될 경우 연결된 객체를 어떻게 할 것인지에 대한 부분이다. 이전의 `on_delete=models.SET_CASCADE`의 경우 인스턴스가 지워질 경우 관계된 인스턴스 또한 삭제 되는 옵션이고 `SET_NULL` 의 경우 단순히 `NULL`로 채워 지게 된다.