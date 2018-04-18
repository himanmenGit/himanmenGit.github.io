---
layout: post
title: "Django 내장 템플릿 필터"
categories:
  - Django
tags:
  - Django
---

# Built-in Template filter

{% raw %}
### add
* 변수에 값을 추가함.
* 두 값을 정수로 강제 변환. 정수로 변환이 되면 더하기가 됨.
```html
# value가 4면 6이 나옴
{{ value|add:"2" }}
# first가 [1,2,3] second가 [4,5,6] = [1,2,3,4,5,6]이 나옴
{{ first|add:second}}
```

### addslashes
* 따옴표 앞에 슬래시를 추가함.
```html
# "I'm using Django" 는 "I\'m using Django"
{{ value|addslashes }}
```

### capfirst
* 첫번째 문자를 대문자로 바꾼다. 문자가 아닌경우 효과가 없다.
```html
{{ value|capfirst }}
```

### center
* 주어진 폭의 필드에 중앙을 마춤
```html
# "     Django     "
"{{ value|center:"15" }}"
```

### cut
* 인수로 주어진값을 모두 제거
```html
# 'ab c d' -> 'abcd'
{{ value|cur:" " }}
```

### date
* 지정된 형식에 따라 날짜 형식을 지정
* `PHP`의 `date()` 함수와 비슷한 형식. 약간 다름
```html
# Wed 09 Jan 2008
{{ value|date:"D d M Y" }}
```

### default
* 값이 `False`이면 기본값으로 사용
```html
# value가 빈 문자열이면 nothing를 사용
{{ value|default:'nothing' }}
```

### default_if_none
* 값이 `None`인 경우 기본값을 사용
```html
# value가 None이면 nothing를 사용
{{ value|default_if_none:"nothing" }}
```

### dictsort
* 딕셔너리 목록을 가져와 인수에 주어진 키별로 정렬된 목록을 반환
```html
{{ value|dictsort:"name" }}
{{ value|dictsort:0 }}
```

### dictsortreversed
* dictsort와 기능은 같지만 역순으로 반환함.

### divisibleby
* 값을 인수로 나눌수 있는 경우 `True`를 반환
```html
# 값이 21이면 True
{{ value|divisibleby:"3"}}
```

### escape
* 문자열의 `HTML`을 이스케이프 한다.
* `<` 를 `&lt;` 로 바꿈.
```html
# escape가 꺼져 있을때 escape 필터를 사용하여 켤 수 있다.
{% autoescape off %}
  {{ title|escape }}
{% endautoescape %}
```

### escapejs
* `JavaScript` 문자열에서 사용할 문자를 이스케이프 처리함.
```html
{{ value|escapejs }}
```

### filesizeformat
* 인수없이 사용하면 부동 소수점 숫자를 하나의 소수점 이하 자릿수로 반올림 하지만 표시할 소수점 자릿수가 있는 경우에만 해당.
* 인수가 `-`면 표시할 소수점이 있으면 3자리 없으면 해당없음
* 인수가 부호없는 정수 이면 항상 자리수를 표시
* 기본값은 `-1`이다
```html
# 34.23234 -> 34.2
# 34.0000 -> 34
# 34.2600 -> 34.3
{{ value|floatformat }}
```

### force_escape
* `HTML` 이스케이프를 문자열에 적용한다.
```html
# <p> HTML 태그를 적용
{% autoescape off %}
  {{ body|linebreaks|force_escape }}
{% endautoescape %}
```

### get_digit
* 숫자를 받으면 요청 된 숫자를 반환
* 1은 오른쪽에서 첫번째 2는 오른쪽에서 두번째
```html
# 123456789 -> 8
{{ value|get_digit:"2" }}
```

### iriencode
* `IRI`를 `URL`에 포함하기에 적합한 문자열로 바꿈.
* `URL`애 `ASCII`문자가 포함된 문자열을 사용하려는 경우에 필요
```html
# ?test=1&me=2 -> ?text=1&amp;me=2
{{ value|ireiencode }}
```

### join
* `python`의 `join` 과 같이 문자열로 합칩니다.
```html
# ['a','b','c'] -> "a // b // c"
{{ value|join:" // " }}
```

### last
* 값의 마지막 항목을 반환.
```html
# ['a','b','c','d'] -> d
{{ value|last }}
```

### length
* 값의 길이를 반환.
```html
# abcd or ['a','b','c','d'] ->4
{{ value|length }}
```

### length_is
* 값의 길이가 해당 인수랑 같으면 `True` 아니면 `False`
```html
# ['a','b','c','d'] or abcd -> True
{{ value|length_is:"4" }}
```

### linebreaks
* 줄 바꿈을 적절한 `HTML`로 바꿈
```html
# joel\nis a slug. -> <p>joel<br /> is a slug</p>
{{ value|linebreaks }}
```

### linebreaksbr
* 모든 개행 문자를 `<br />`로 바꿈
```html
# joel\nis a slug. -> joel<br /> is a slug
{{ value|linebreaksbr }}
```

### linenumbers
* 줄번호가 있는 텍스트를 표시
```html
# one   -> 1.one
# two   -> 2.two
# three -> 3.three
{{ value|linenumbers }}
```


### ljust
* 주어진 필드에서 왼쪽 정렬
```html
# Django -> "Django      "
{{ value|ljust"10" }}
```

### lower
* 문자열을 소문자로 변환.
```html
# Totally LOVING this Album! -> totally loving this album!
{{ value|lower }}
```

### make_list
* 리스트로 만들어 줌.
```html
# "Joel" -> ['J', 'o', 'e', 'l']
# 123   -> ['1', '2', '3']
{{ value|make_list }}
```

### phone2numberic
* 전화번호를 숫자로 만들어 줌.
```html
# 800-COLLECT -> 800-2655328
{{ value|phone2numberic}}
```

### pluralize
* 값이 1이 아닐 경우 복수접미어 를 반환 기본값은 's'
```html
You have {{ num_walruses }} walrus{{ num_walruses|pluralize:"es" }}
```

### pprint
* `pprint.pprint()` 디버깅을 위한 것.

### random
* 지정된 리스트로 부터 임의 항목을 리턴함.
```html
# [1,2,3,4] -> 2
{{ value|random }}
```

### rjusts
* 필드에 대하여 오른쪽 정렬을 함
```html
# Django -> "     Django"
"{{ value|rjust:"10" }}"
```

### safe
* 문자열을 출력하기 전에 더 이상 `HTML` 이스케이프가 필요하지 않은것으로 표시
```html
{{ var|safe|escape }}
```

### safeseq
* 시퀀스의 각 요소에 안정 필터를 적용 `join`과 같이 사용하면 유용함.
```html
{{ some_list|safeseq|join:", " }}
```

### slice
* 리스트의 일부를 되돌려줌. 파이썬과 비슷하게 작동
```html
#  ['a', 'b', 'c'] -> ['a', 'b']
{{ some_list|slice:":2" }}
```

### slugify
* ASCII로 변환, 공백을 하이픈으로 변환. 영숫자, 밑줄 또는 하이픈이 아닌 문자를 제거, 소문자로 변환, 앞뒤 공백을 제거
```html
# "Joel is a slug" -> "joel-is-a-slug"
{{ value|slugify }}
```

### stringforamt
* 문자열 혀식 지정자 인수에 따라 변수를 형식화 함
```html
# 10 -> 1.000000E+01
{{ value|stringforamt:"E" }}
```

### striptags
* 모든 `[X]HTML` 태그를 삭제할수 있도록 한다.
```html
<b>Joel</b> <button>is</button> a <span>slug</span> -> "Joel is a slug"
{{ value|striptags  }}
```

### time
* 주어진 형식에 따라 시간을 포맷함.
```html
# datetime.datetime.now() -> "01:23"
{{ value|time:"H:i" }}
```

### timesince
* 해당 날짜 이후의 시간으로 날짜를 형식화
```html
# blog_date=2006/6/1 comment_date=2006/6/1 08:00 -> 08:00
{{ blog_date|timesince:comment_date }}
```

### timeuntil
* 현재 부터 주어진 날짜 또는 날짜 시간까지의 시간을 측정
```html
# 오늘이 2006/6/1 confrerence_Date=2006/6/29 -> 4주
{{ confrerence_Date|timeuntil:from_date }}
```

### title
* 단어를 대문자로 시작하고 나머지문자를 소문자로 만듬.
```html
# my FIRST post = My First Post
{{ value|title }}
```

### truncatechars
* 문자열이 지정된 인수보다 길면 자른다. 잘린문자열을 `...`로 표현
```html
# Joel is a slug -> Joel i...
{{ value|truncatechars:9 }}
```

### truncatechars_html
* `truncatechars`와 비슷하지만 `HTML` 태그를 인식함
```html
#<p> Joel is a slug</p> -> <p>Oel i..</p>
{{ value|truncatechars_html:9 }}
```

### truncatewords
* 특정 단어 수 뒤의 문자열을 자름.
```html
# Joel is a slug -> Joel is ...
{{ value|truncatewords: 2 }}
```

### truncatewords_html
* `truncatewords`와 비슷하지만 `HTML` 태그를 인식
```html
# <p>Joel is a slug</p> -> <p> Joel is ... </p>
{{ vallue|truncatewords_html:2 }}
```

### unordered_list
* 리스트의 형식에 따라 <ul>태그를 만듬.
```html
# ['States', ['Kanasa']]
# <li>States
#   <ul>
#     <li>Kansas</li>
#   </ul>
# </li>
{{ value|unordered_list }}
```

### upper
* 문자열을 대문자로 변환
```html
# Joel is a slug -> JOEL IS A SLUG
{{ value|upper }}
```

### urlencode
* `URL`에 사용할 이스케이프 처리 함.
```html
# https://www.example.org/foo?a=b&c=d
# -> https%3A//www.example.org/foo%3Fa%3Db%26c%3Dd
{{ value|urlencode }}
```

### urliize
* 일반 텍스트의 `URL` 및 이메일 주소를 클릭 가능한 링크로 변환
```html
{{ value|urlize }}
```

### urliizetrunc
* urlize와 같이 동작 하지만 주어진 인수보다 글자수가 크면 `URL`을 자른다. (...)
```html
# Check out www.djangoproject.com
# -> Check out <a href="http://www.djangoproject.com" rel="nofollow">www.djangopr...</a>
{{ value|urliizetrunc:15 }}
```

### wordcount
* 단어의 수를 반환
```html
# Joel is a slug -> 4
{{ value|wordcount }}
```

### wordwrap
* 지정된 길이로 단어를 줄바꿈 함.
```html
# Joel is a slug
# Joel
# is a
# slug
{{ value| wordwrap:5 }}
```

### yesno
* `True`, `False`, `None` 값을 문자열 `'yes', 'no', 'maybe'`에 매칭되는 문자로 반환
```html
# True -> yeah
{{ value|yesno:"yeah,no,maybe"}}
```

# Internationalization tags and filters
### i18n
* 번역가능한 텍스트를 지정할 수 있게함.
* `USE_I18N`을 `True`로 설정
```html
{% load i18n %}
```

### l10n
* 템플릿 값의 로컬라이징을 지원 함.
* `USE_L10N`을 `True` 하여 기본적으로 활성화 되도록 하는 경우가 많음.
```html
{% load l10n %}
```

### tz
* 템플릿의 시간대 변환을 제어
* `USE_TZ`를 `True`로 설정하여 로컬 시간의 변환을 기본적으로 발생 시킬 수도 있음.
```html
{% load tz %}
```

# Other Tags and filters libraries
* `Django`에는 `INSTALLED_APPS`에 명시적으로 표시하고 `{% load %}` 태그를 통해 활성해야 하는 몇 가지 다른 템플릿 태그 라이브러리가 있음.

### django.contrib.humanize
* 사람의 손길을 추가하는데 유용한 템플리

# static
### static
* `STATIC_ROOT`에 저장된 정적 파일에 연결
* `STATICFILES_STORAGE`에 지정된 저장공간의 `url()` 메소드를 사용하여 파일을 제공
* as를 사용하여 이름 사용 가능
```html
{% load static %}
<img src="{% static "images/h1.jpg" %}" alt="Hi" />
# 변수를 전달 받아 사용 가능
<link rel="stylesheet" href="{% static user_stylesheet %}" type="text/css" media="screen" />
```

### get_static_prefix
* 정적 템플릿이 삽입되는 정확한 위치와 방법을 제어 하기 위해 사용
```html
{% load static %}
<img src="{% get_static_prefix %}images/h1.jpg" alt="Hi!" />
```

### get_media_prefix
* `get_static_prefix`와 마찬가지로 사용
```html
{% load static %}
<body data-media-url="{% get_media_prefix %}">
```

{% endraw %}