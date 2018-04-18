# django Models 02

## 관계 (Relationships)
관계형 데이터베이스의 힘은 테이블을 서로 연관시키는데 있다. 장고는 다 대일, 다 대다, 일대일 데이터 베이스 관계의 세 가지 가장 일반 적인 유형을 정의 할수 있는 방법을 제공 한다.

속도는 키-벨류형 데이터베이스가 빠르지만 서로관의 관계를 표현하기에 적절하지 못하며 속도에 최적화 되어 있다. 반면에 관계형 데이터 베이스는 저장 용량을 아끼는데 최적화 되어 있다. 


### 다 대일 (Many-to-one relationships)
다 대일 관계를 표현하려면 장고 모델의 `django.db.models.ForeignKey`를 사용 하면 된다.
`ForeignKey`는 위치 인수가 필요하다. 모델이 관련된 클래스 이다.
만약 자동차와 제조회사가 있는 경우 제조업체가 여러 자동차를 생산하지만 각 자동차에는 하나의 제조 업체가 있는 경우를 만들어 보면
```
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

### 다 대다 (ManyToMany relationships)
서로 여러개의 관계를 가지는 형태. A모델이 B모델을 가질 수 있고 B모델도 A모델을 여러개 가질 수 있는 것.
`many-to-many`관계를 정의 하려면 `ManyToManyField`를 사용한다. 다른 필드 와 마찬가지로 모델의 클래스 속성으로 포함하여 사용 한다.
그리고 다 대다 관계도 재귀관계를 만들 수 있다.

예를 들면 어떤 글의 좋아요를 누르게 되면 해당 글에 어떤 사람이 좋아요를 눌렀는지 가지고 그 사람은 여러 글에 좋아요를 할 수 있다.
피자는 여러 종류의 토핑을 가질 수 있다.
토핑은 여러 종류의 피자에 올라 갈 수 있다.
일반적인 다 대다 관계를 처리할 경우 `ManyToManyField`만 있으면 된다. 
그리고 `MTM`의 이름은 관련 모델 객체 세트를 설명하는 복수형으로 제안되지만 필수는 아니다.
`MTM`필드가 어디에 있는지는 중요하지 않지만 두 모델중 하나에만 있어야 한다.
어느 쪽이 주가 되는 의미인지에 따라 주가되는 모델에 필드를 정의 하는게 좋다.
```
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name
```

```
masterPizza = Pizza.objects.get(name='마스터피자')
masterPizza.toppings.all()
# 치즈, 피망, 불고기, 파인애플...
cheeseTopping = Topping.objects.get(name='치즈')
cheeseTopping.pizza_set.all()
# 치즈피자, 하와이안피자, 불고기피자...
```
이렇게 생성한 테이블중 다 대다 관계를 표한하는 테이블이 새로 생성되는데 여기는 3개의 필드가 존재 한다. `id`필드 `pizza_id`, `topping_id` 각각 `Row`의 `pk`, 피자의 `pk`, 토핑의 `pk` 다른 모델의 인스턴스의 `pk`값만으로 서로의 관계를 연결 하고 있다.

이렇게 단순한 관계일 경우는 일반적인 `ManyToManyField`로 끝나지만 만약 두 모델간의 관계에 데이터를 연결해야 할 경우가 생길 수도 있다.

이런 경우에는 중계 테이블을 만들어 `ManyToManyField`를 만들어서 사용 해야 한다.

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
