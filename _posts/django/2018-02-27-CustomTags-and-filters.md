---
layout: post
title: "Django 사용자 정의 태그와 필터"
categories:
  - Django
tags:
  - Django
---

# django Custom tags and filters

{% raw %}
기본 템플릿들에서 다루지 않는 기능이 필요할 경우 사용자 정의 태그와 필터를 정의하여 템플릿 엔진을 확장 한 다음 `{% load %}` 태그를 사용하여 템플릿에서 사용할 수 있도록 만들 수 있다.
{% endraw %}

사용자 정의 템플릿 태그와 필터를 정의하는 가장 일반적인 위치는 해당 장고 앱 내에 하는것이 좋고, 기존 앱과 관련이 있다면 해당 앱에 묶는 것이 좋다. 그렇지 않으면 새로운 앱을 추가 할 수 없다. 장고 앱이 `INSTALLED_APPS`에 추가하면 해당 위치에 정의된 모든 태그가 자동으로 템플릿 내에서 로드 된다.

각 앱에는 `models.py` `views.py`와 같은 깊이에 `templatetags`라는 디렉터리가 있어야 한다. 아직 존재 하지 않으면 생성하고 **파이썬 패키지**로 만들어 `__init__.py`를 만들어야 한다. 
템플릿 모듈을 만들면 런서버를 재시작해야 적용 된다.

사용가능한 태그 라이브러리가 되려면 모듈에 `register` 라는 모듈 수준의 변수가 있어야 한다. 이 변수는 모든 태그와 필터가 등록된 `template.Library`인스턴스이다. 따라서 모듈의 최상단에 해당 코드를 넣자.

아니면 `Django Templates`의 `libraries` 인수를 통해 템플릿 태그 모듈을 등록 할 수 있다. 템플릿 태그를 로드 할 때 템플릿 태그 모듈 이름과 다른 라벨을 사용하려는 경우 유용하다. 또한 응용 프로그램을 설치하지 않고도 태그를 등록 할 수 있다.

커스텀 필터는 단지 파이썬 함수 일 뿐이다. 하나 또는 두개의 인수를 취한다. 변수의 값은 반드시 문자열일 필요 는 없다. 인수는 기본값을 가질수도 있고 모듀 생략 할 수도 있다.
장고 템플릿의 불편한점은 여러개의 인수를 한번에 받지 못한다. 하나의 인수만 받아 처리 하는 경우가 많다 다른 템플릿을 사용하는 경우도 있다.

그리고 예외 처리를 제공하지않고 모든 예외는 서버 오류로 표기된다.]
```
from django import template

register = template.Library()


@register.filter(name='ellipsis_line')
def ellipsis_line(value, arg):
    lines = value.splitlines()
    if len(lines) > arg:
        return '\n'.join(lines[:arg] + ['...'])
    return value
```

```
# HTML
{{ some.text|ellipsis_line:5|linebreaksbr }}
```