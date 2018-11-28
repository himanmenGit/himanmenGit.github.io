---
layout: post
title: "Django 템플릿에서 {% static %}을 커스텀 하여 정적파일 강제 새로고침 하기"
categories:
  - Django
tags:
  - Django
  - Template
  - Tip
---

# 작성 이유
본 포스팅은 작성자가 프로젝트를 진행하다 `css/js`파일이 수정후 배포하였을때 자동 새로고침이 되지 않아 만들어 본 기능이다.

거기에 기존에 사용한 `{% load static %}`이나 `{% static 'path' %}`등을 수정하지 않고 그대로 사용 할 경우에 사용하며

`static` 템플릿 태그에 다른 기능을 사용하지 않고 오직 `{% static 'path' %}`만 사용 할 경우에 사용 해야 문제가 생기지 않는다.

# 설명
장고 템플릿에서 정적 파일을 로드 할 경우 `{% load static %}`을 하여 `{% static 'path' %}` 의 형태로 사용한다. 
```javascript
<script type="text/javascript" src="{% static 'js/file.js' %}"></script>
```
그런데 여기서 문제는 배포시 마다 같은 파일 이름을 가진 `css`나 `js`파일이 브라우저 에서 캐싱되어
 
사용자가 강제적으로 브라우저의 캐시를 지워주지 않으면 배포후에 해당 파일들이 새로 고침이 되지 않는 현상이 발생한다.

이런경우 하나의 팁이 파일의 경로 뒤에 `?build=20181128`과 같은 쿼리 스트링을 적어 주면 

브라우저는 쿼리 스트링을 포함한 URL을 기준으로 캐시가 이루어지기 때문에 다른 파일로 인식이 된다.

이것을 이용하여 브라우저에서 강제로 정적파일의 캐시를 다시 생성할 수 있게 된다.

해당 포스팅에서는 `{% static %}`을 바꾸지 않고 위의 코드처럼 경로를 넣더라고 뒤에 쿼리스트링을 붙이는 방법을 제시한다.

{% raw  %}
```python
# project/app_name/templatetags/static.py
from django import template
from django.templatetags.static import StaticNode

register = template.Library()


class CustomStaticNode(StaticNode):
    # StaticNode를 상속 받아 StaticNode에서 만들어진 url에다가 해당 쿼리스트링을 넣는다
    # 배포시 뒤에 버전을 바꾸어 사용
    def url(self, context):
        path = super().url(context) + '?version=1.0.0'
        return path


@register.tag('static')
def do_static(parser, token):
    # StaticNode를 상속받은 CustomStaticNode객체를 사용하여 StaticNode의 handle_token을 사용
    node = CustomStaticNode.handle_token(parser, token)
    return node

```
이렇게 하면 `{% load static %}`과 `{% static 'path' %}`로 만들어 놓은 템플릿 코드를 수정 하지 않고 바로 적용이 가능하다.
{% endraw  %}

## `django-sass-processor`를 설치하여 `{% sass_src 'path' %}`를 사용할 경우

위와 동일하게 추가적인 템플릿 코드 수정없이 진행하기위해 사용하였다.
 
 {% raw  %}
```python
# project/app_name/templatetags/sass_tags.py
from django import template
from django.conf import settings

from sass_processor.templatetags.sass_tags import SassSrcNode

register = template.Library()


class CustomSassSrcNode(SassSrcNode):
    # SassSrcNode를 상속받아 path를 받아 쿼리스트링을 넣는다
    def render(self, context):
        result = super().render(context) + '?version=1.0.0'
        return result


# 마찬가지로 SassSrcNode를 상속받은 CustomSassSrcNode를 사용하여 태그를 사용한다.
@register.tag(name='sass_src')
def render_sass_src(parser, token):
    return CustomSassSrcNode.handle_token(parser, token)

```
{% endraw  %}