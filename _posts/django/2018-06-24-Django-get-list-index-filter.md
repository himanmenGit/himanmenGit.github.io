---
layout: post
title: "Django 템플릿에 리스트 오브젝트의 인덱스 사용하기"
categories:
  - Django
tags:
  - Django
  - Template
  - Tags
---

정말 오랜만에 다시 쓰는 포스팅 이다. 
다시 열심히 포스팅 해야 겠다.. 잔디가 다 죽었다..

{% raw  %}
# Django CustomTag
장고에서 템플릿 뷰로 딕셔너리를 가진 리스트 컨텍스트를 넘겨 주었을 때,
해당 리스트를 `for in`문을 통해 순회할때 인덱스를 넣어서 가져 오고 싶었다.
그래서 혹시나 하는 마음에
 
```html
{% for temp in templist %}
    {% include 'temp.html' with temp=templist.forloop.counter0 %}    
{% endfor %} 
```
따위로 가져 오려고 해보았지만 실패! 물론 객체를 바로 때려 넣어 ( `temp=temp` ) 사용 할 수 있지만
해당 템플릿에 제한사항이 존재하여 저런식으로 작업을 해야 했다. 
그래서 사용한 것이 사용자 정의 템플릿 태그를 사용하는 것이었다.

# 설정
```python
# temp/tag/custom_tags.py
from django import template
register = template.Library()

@register.filter
def get_at_index(object_list, index):
    return object_list[index]
```

# 사용
```html
{% load custom_tags %}

{% for temp in temp_list %}
    {% include `temp.html` with info=temp|get_at_index:forloop.counter0 %}
{% endfor %}
```

이렇게 사용 하면 된다.
참고로 `forloop.counter`는 1부터 시작하고 `forloop.counter0`은 0부터 시작한다.

{% endraw  %}