---
layout: post
title: "Django sekizai"
categories:
  - Django
tags:
  - Django
  - Package
---

# Django sekizai
`css`, `js` 를 템플릿화 하여 `block` 으로 생성하여 `html`에 지정 할 수 있다.


## 설치
```bash
pip install django-sekizai
```

## 설정
```python
INSTALLED_APPS = (
    ...
    'sekizai',
)

TEMPLATES = [
    ...
    'OPTION': {
        'context_processors': [
            ...
            'sekizai.context_processors.sekizai',
        ]
    }
]
```

## 사용
{% raw  %}
`Sekizai`는 `render_block` 및 `addtoblock` 를 사용하여 코드조각을 처리함.
`{% render_block <name> %}` 를 사용하여 블록을 정의 하고

```html
{% addtoblock <name> [strip] %}
  ...
{% endaddtoblock %}
```
를 사용하여 해당 블록에 데이터를 추가 할 수 있다.
스트립 플래그가 설정되어 있으면 앞뒤 공백이 제거 된다,

```html
{% load sekizai_tags %}
<html>
<head>
  {% render_block "css" %}
</head>
<body>
  {% render_block "js" %}
</body>
</html>
{% addtoblock "css" %}
<link href="/media/css/stylesheet.css" media="screen" rel="stylesheet" type="text/css" />
{% endaddtoblock %}
{% addtoblock "js" %}
<script type="text/javascript">
alert("Hello django-sekizai");
</script>
{% endaddtoblock %}
```
으로 만들면 아래 처럼 렌더링 된다.
```html
<html>
<head>  
  <link href="/media/css/stylesheet.css" media="screen" rel="stylesheet" type="text/css" />
</head>
<body>
  <script type="text/javascript">
  alert("Hello django-sekizai");
  </script>
</body>
</html>
```

## 제한사항
`{% render_block %}` 태그는 종료 태그가 있는 템플릿 태그안에 두면 안된다
예를 들어 `{% block %} ... {% endblock %}` 이나 `{% if %} ... {% endif %}`
`{% render_block %}` 태그는 `include`된 템플릿에 있으면 안된다.
확장 템플릿에서 `{% addtoblock %}` 을 사용할 경우는 `{% block %} ... {% endblock %}` 안에 있어야 한다.
`{% addtoblock %}` 태그는 `only` 옵션이 포함된 `include` 한 템플릿에 사용하면 안된다.

## Sekizai data 처리
`{% render_block %}` 태그의 제한사항 때문에 `django-compressor` 와 같은 라이브러리에서는 `sekizai` 를 직접 사용할 수 없다. 이러한 이유로 `sekizai`는 버전 0.5에서 `render_block` 에 후 처리 기능을 추가 했다.

```python
def spaceless_post_processor(context, data, namespace):
    from django.utils.html import strip_spaces_between_tags
    return strip_spaces_between_tags(data)
```

이 프로세서를 사용하려면 `spaceless_post_processor` 의 위치를 지정 해주어야 한다.

```html
...
{% render_block "js" postprocessor "myapp.sekizai_processors.spaceless_post_precessor" %}
...
```
아니면 `{% addtoblock %}` 에 사전 처리를 할 수도 있다.
```html
{% addtoblock "css" preprocessor "myapp.sekizai_processors.spaceless_pre_processor" %}
```
{% endraw  %}