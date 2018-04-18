---
layout: post
title: "Django Field lookups"
categories:
  - Django
tags:
  - Django
---

### SQL LIte
---
* i 가 붙은 대소문자의 구분있고 없고가 SQL lite에는 지원하지 않음.
<br>

# Field lookups
---
* Field lookups는 SQL문의 WHERE절의 요점을 지정하는 방법.
* `QuerySet`메소드인 `filter()`, `exclude()`, `get()`등에 키워드 인자로 지정 한다.
<br>

### exact
---
* 정확하게 일치하는 값을 검색.
* `None`값을 넣게 되면 SQL의 `IS NULL` 구문을 사용하는 것과 같다.
```
# WHERE id = 14;
Entry.objects.get(id__exact=14) 
# WHERE id IS NULL;
Entry.objects.get(id__exact=None) 
```
<br>

### iexact
---
* 대소문자의 구분없이 정확하게 일치하는 값을 검색.
* `None`값을 넣게 되면 SQL의 `IS NULL`구문을 사용 하는 것과 같다.
```
# WHERE name ILIKE 'beatles blog';
Blog.objects.get(name__iexact='beatles blog')
# WHERE name IS NULL;
Blog.objects.get(name__iexact=None)
```
<br>

### contains
* 대소문자를 구분하고 문자열을 포함하고 있는 것을 검색.
```
# WHERE headline LIKE '%Lennon%';
Entry.objects.get(headline__contains='Lennon')
```
<br>

### icontains
---
* 대소문자를 구분하지 않고 문자열을 포함하고 있는 것을 검색.
```
# WHERE headline ILIKE '%Lennon%';
Entry.objects.get(headline__icontains='Lennon')
```
<br>

### in
---
* 주어진 iterable한 객체(리스트, 튜플, 쿼리셋)에 포함되어 있는지 검색.
```
# WHERE id IN (1,3,4);
Entry.objects.filter(id__in=[1,3,4])
```
* 쿼리셋을 사용하여 동적으로도 검색이 가능하다.
```
# WHERE blog.id IN (SELECT id FROM ... WHERE NAME LIKE='%Cheddar%')
inner_qs = Blog.objects.filter(name__contains='%Cheddar%')
entries = Entry.objects.filter(blog__in=inner_qs)
```
* `values()` 나 `values_list()`를 쓸 `__in`에 쓸 경우 결과 값은 하나의 필드만을 반환 해야 한다.
```
inner_qs = Blog.objects.filter(name__contains='Ch').values('name')
entries = Entry.objects.filter(blog__name__in=inner_qs)
```
* 만약 두개의 필드로 반환하는 `values()`를 할 경우 TypeError를 raise를 시킬 것이다.
```
# Bad code! Will raise a TypeError.
inner_qs = Blog.objects.filter(name__contains='Ch').values('name', 'id')
entries = Entry.objects.filter(blog__name__in=inner_qs)
```
* 중첩된 쿼리를 사용 할 때는 데이터베이스의 성능 특성을 이해하고 써야 한다. 일부 데이터베이스의 경우 중첩 쿼리를 잘 처리 하지 못한다. 그래서 `__in`에 대한 list 목록을 미리 추출하여 두번째 쿼리에 해당 list를 사용 하는것이 더 좋다.
```
values = Blog.objects.filter(name__contains='Cheddar').values_list('pk', flat=True)
entries = Entry.objects.filter(blog__in=list(values))
```
* 두번째 쿼리에서 `list()`를 사용하여 첫번째 쿼리를 강제로 실행. 중첩 쿼리를 실행하지 않게 한다.(???) - in을 실행하면서 Entry를 계속 검색하는데 거기서 values 쿼리가 중복하여 실행된다. 그것을 방지.
<br>

### gt, gte
---
* `gt`  : ~보다 큰.
* `gte` : ~보다 크거나 같은.
```
# WHERE id > 4;
Entry.objects.filter(id__gt=4)
# WHERE id >= 4;
Entry.objects.filter(id__gte=4)
```
<br>

### lt, lte
---
* `lt`  : ~보다 작은.
* `lte` : ~보다 작거나 같은.
```
# WHERE id < 4;
Entry.objects.filter(id__lt=4)
# WHERE id <= 4;
Entry.objects.filter(id__lte=4)
```
<br>

### startswith, istartswith
* `startswith` : 대소문자를 구분하여 시작하는 문자열.
* `istartswith`: 대소문자를 구분하지 않고 시작하는 문자열.
```
# WHERE headline LIKE 'Lennon%';
Entry.objects.filter(headline__startswith='Lennon')
# WHERE headline ILIKE 'Lennon%';
Entry.objects.filter(headline__istartswith='Lennon')
```

<br>

### endswith, iendswith
---
* `endswith` : 대소문자를 구분하여 끝나는 문자열.
* `iendswith`: 대소문자를 구분하지 않고 끝나는 문자열.
```
# WHERE headline LIKE '%Lennon';
Entry.objects.filter(headline__endswith='Lennon')
# WHERE headline ILIKE '%Lennon';
Entry.objects.filter(headline__iendswith='Lennon')
```
<br>

### range
---
* 범위를 안에 있는지 검색.
```
start_date = date(2005, 1, 1)
end_date = date(2005, 3, 31)
# WHERE pub_date BETWEEN '2005-01-01' and '2005-03-31';
Entry.objects.filter(pub_date__range(start_date, end_date))
```
* SQL에서 BETWEEN을 날짜, 숫자, 문자에서 사용하는 것처럼 range도 사용 가능하다.
* 날짜가 있는 `DateTimeField`를 필터링 하는 경우 마지막 날의 항목은 포함하지 않는다. 왜냐하면 주어진 날짜의 오전 0시로 경계가 설정되기 때문.
```
WHERE pub_date BETWEEN '2005-01-01 00:00::00' and '2005-03-31 00:00:00';
```
* 일반적으로 dates와 datetimes를 섞어쓰면 안된다.
<br>

### date
---
* `datetime` 필드의 경우 값을 날짜로 변환한다. 추가 체인이 가능하고, `date`값을 사용 한다.
```
Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))
Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
``` 

### year
---
* `date` 및 `datetime`의 필드에서 년도가 정확히 일치하는 것을 검색한다. 추가 체인 필드 검색이 가능하고 정수를 나타낸다.
```
# WHERE pub_date BETWEEN '2005-01-01' AND '2005-12-31';
Entry.objects.filter(pub_date__year=2005)
# WHERE pub_date >= '2005-01-01';
Entry.objects.filter(pub_date__year__gte=2005)
```
<br>

### month
---
* `date` 및 `datetime`의 필드에서 달이 정확히 일치하는 것을 검색한다. 추가 체인 필드 검색이 가능하고 정수1 부터 12까지 나타낸다.
```
# WHERE EXTRACT('month' FROM pub_date) = '12';
Entry.objects.filter(pub_date__month=12)
# WHERE EXTRACT('month' FROM pub_date) >= '6';
Entry.objects.filter(pub_date__month__gte=6)
```
<br>

### day
---
* `date` 및 `datetime`의 필드에서 일이 정확히 일치하는 것을 검색한다. 추가 체인 필드 검색이 가능하고, 정수를 나타낸다.
```
# WHERE EXTRACT('day' FORM pub_date) = '3';
Entry.objects.filter(pub_date__day=3)
# WHERE EXTRACT('day' FORM pub_date) >= '3';
Entry.objects.filter(pub_date__day__gte=3)
```
<br>

### week
---
* `date` 및 `datetime`의 필드에서 ISO-8601의 기준에 따라 주 번호(1-52 또는 53)을 반환한다. 즉 월요일에 시작하는 주 및 첫번째 주는 목요일에 시작한다.
```
Entry.objects.filter(pub_date__week=52)
Entry.objects.filter(pub_date__week__gte=32, pub_date__week__lte=38)
```
<br>

### week_day
---
* `date` 및 `datetime` 필드에서 요일과 정확하게 일치 하는 것을 검색한다. 추가 체인 필드 검색이 가능하다. 정수1 부터 7까지 나타낸다.
```
Entry.objects.filter(pub_date__week_day=2)
Entry.objects.filter(pub_date__week_day__gte=2)
```
* 연도와 월에 상관없이 1(일요일)과 7(토요일)사이에서 색인된다.
<br>

### quarter
---
* `date` 및 `datetime` 필드에서 분기가 정확하게 일치 하는 것을 검색한다. 추가 체인 필드 검색이 가능하며, 1년의 1/4인 1에서 4까지 나타낸다.
```
# 2분기 검색
Entry.objects.filter(pub_date__quarter=2)
```
<br>

### time
---
* `datetime`필드의 경우 값을 시간으로 변경하여 검색. 추가 체인 필드 검색이 가능하고, `datetime.time`값을 사용한다.
```
Entry.objects.filter(pub_date__time=datetime.time(14, 30))
Entry.objects.filter(pub_date__time__between=(datetime.time(8), datetime.time(17)))
```
<br>

### hour
---
* `datetime` 및 `time` 필드에서 시간이 정확하게 일치하는 것을 검색한다. 추가 체인 필드 검색이 가능하며, 0에서 23사이를 나타낸다.
```
# WHERE EXTRACT('hour' FROM timestamp) = '23';
Event.objects.filter(timestamp__hour23)
# WHERE EXTRACT('hour' FROM time) = '5';
Event.objects.filter(time_hour=5)
# WHERE EXTRACT('hour' FROM timestamp) >= '12';
Event.objects.filter(timestamp__hour__gte=12)
```
<br>

### minute
---
* `datetime` 및 `time` 필드에서 분이 정확하게 일치하는 것을 검색한다. 추가 체인 필드 검색이 가능하며, 0에서 59사이를 나타낸다.
```
# WHERE EXTRACT('minute' FROM timestamp) = '29';
Event.objects.filter(timestamp__minute=29)
# WHERE EXTRACT('minute' FROM time) = '46';
Event.objects.filter(time__minute=46)
# WHERE EXTRACT('minute' FROM timestamp) >= '29';
Event.objects.filter(timestamp__minute__gte=29)
```
<br>

### second
---
* `datetime` 및 `time` 필드에서 초가 정확하게 일치하는 것을 검색한다. 추가 체인 필드 검색이 가능하며, 0에서 59사이를 나타낸다.
```
# WHERE EXTRACT('second' FROM timestamp) = '31';
Event.objects.filter(timestamp__second=31)
# WHERE EXTRACT('second' FROM time) = '2';
Event.objects.filter(time__second=2)
# WHERE EXTRACT('second' FROM timestamp) >= '31';
Event.objects.filter(timestamp__second__gte=31)
```
<br>

### isnull
---
* `IS NULL` 과 `IS NOT NULL`에 대한 `True`, `False`값을 검색한다.
```
# WHERE pub_date IS NULL;
Entry.objects.filter(pub_date__isnull=True)
```
<br>

### regex, iregex
---
* `regex`  : 대소문자를 구분하여 정규식을 검색.
* `iregex` : 대소문자를 구분하지 않고 정규식을 검색.
```
# WHERE title REGEXP '^(An?|The) +';
Entry.objects.get(title__regex=r'^(An|The) +')
# WHERE title REGEXP '(?i)^(an?|the) +'l;
Entry.objects.get(title__iregex=r'^(an?|the) +'
```
* 정규식을 전달하기 위해 `r`을 붙이는게 좋다.
<br>
