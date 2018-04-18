---
layout: post
title: "Django 내장 템플릿 태그"
categories:
  - Django
tags:
  - Django
---

# Built-in Template tags

{% raw %}
### autoescape
* 템플릿 변수에 대해 `escape`처리를 해주는 태그
* 악의적 사용에 대비하여 사용
```
{% autoescape on %}
    {{ body }}
{% endautoescape %}
```

### block
* 하위 템플릿으로 해당 `block`에 덮어 쓸수 있도록 하는 태그

### comment
* 해당 템플릿 코드에 대한 주석
```
{% comment 'Optinal note' %}
...
{% endcomment %}
```

### csrf_token
* `Request`위조에 대비하여 `CSRF` 보호에 사용

### cycle
* 루프에서 많이 사용
* 해당 필터가 사용 될 때마다 등록된 인수에 한번씩 접근하고 모든 인수를 사용하면 처음으로 돌아 간다.
* 인수와 변수를 쓸 수 있고, 혼합이 가능하며 as를 통해 인수에 접근하지 않고 사이클의 현재 값을 참조 할 수 있다.
* `resetcycle` 태그를 사용하여 첫번째 인수에서 다시 시작하도록 할 수 있다.
```
{% for o in some_list %}
    <tr class="{% cycle 'row1' 'row2' %}">
        ...
    </tr>
{% endfor %}
```

### debug
* 전체 로드의 디버깅 정보를 출력

### extends
* 템플릿을 확장하기 위한 태그
* 문자열일 경우 부모 템플릿의 이름으로 사용하고, 객체일 경우 그 객체를 부모 템플릿으로 사용.
* 항상 첫줄에 위치
* 부모에서 정의한 `block`만 재정의 할 수 있다.
```
{% extends 'base.html' %}
{% extends variabls %}
```

### filter
* 하나 이상의 필터를 통해 블록의 내용을 필터링 할 수 있다. 여러 필터 지정가능 필터에 인수를 지정 가능.
```
{% filter force_escape|lower %}
HTML-escaped, all lowercase.
{% endfilter %}
```

### firstof
* `False`가 아닌 첫번째 인수를 전달함
* 모두 `False`일 경우 문자열을 대체값으로 전달
* 자동으로 `escape`한다.
* `as`를 사용해 변수에 저장 할 수 있다.
```
{% firstof var1 var2 var3 'fallback value' %}
{% firstof var1 var2 var3 as value %}
```

### for
* 파이썬의 `for`문과 같다.
* `reversed`를 통해 역순으로 순회 가능하다.
* 중첩 리스트의 경우 `unpack`을 통해 접근 가능
* `forloop`의 경우 루프내에 사용 가능한 여러 변수를 설정.
```
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
```

### for...empty
* for 태그내에 지정된 객체가 없거나 비어있을때 `{% empty %}`룰 수헹
* athlete가 비었을 경우 {% empty %}`룰 수헹
```
{% for athlete in athlete_list %}
  <li>{{ athlete.name }}</li>
{% empty %}
  <li>Sorry, no athletes in this list.</li>
{% endfor %}
```

### if
* 조건문이다
* `operator`에는 `==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `not in`, `is`, `is not` 등이 있다.
* `filter`를 사용할수도 있다
* 연산자 우선 순위에 따라 그룹이 결정 된다.
```
{% if somvar == 'x' %}
  This appears of varialbe somvevar equals the string  "X"
{% endif %}
```

### ifchanges
* `for`루프 내에 사용한다.
* 변수가 지정되지 않으면, content의 내용이 변경되었을 때 True
* 변수가 지정되면, 지정된 변수값이 변경 되었을 경우 True
```
{% for date in days %}
  {% ifchanged %}{{ date|date:"F" }}{% endifchanged %}
  ...
  {% else %}
  ...
  {% endifchanged %}

  {% ifchanged date %}
  ...
  {% endifchanged %}
{% endfor %}
```
### include
* 템플릿을 불러와 현재의 위치에 템플릿을 포함시킨다.
* 문자열로 불러올 수도 있다. 루트 디렉토리에 따른 상대적인 위치로 할 수도 있다.
* 변수에 이름을 넣어 불러 올 수도 있다.
* 키워드 인자를 사용해 컨텍스트를 전달 할 수 있다
* 제공 되는 변수만 사용 하겠다는 표시로 `only`라는 옵션을 주자.
```
{% include 'name_snippet.html' with person='Jane' greeting='Hello' only}
```
* 서로 각자 완전한 독릭적인 렌더링 프로세스를 가져야 한다.
* 확장 템플릿으로 블록을 덮어 쓸 수 없다.

### load
* 커스텀 템플릿 태그세트를 로드한다.
* `from` 을 통해 선택적 로드 가능.
* 여러개 등록 가능
```
{% load somelibrary package.otherlibrary}
{% load foo bar from somelibrary %}
```
### lorem
* 임의의 문자열을 생성한다
* count : 단란 또는 단어 수
* method : 단어 w, 단락 p, 일반텍스트 b default : b
* random : 일반적인 단락을 사용하지 않음.
```
{% lorem [count] [method] [random] %}
```

### now
* 주어진 형식을 사용하여 현재 날짜 및 시간 표시
* as 사용하여 변수에 저장 가능
```
It is {% now "jS F Y H:i as now_time %"}
```

### regroup
* 모든 객체의 목록을 재 그룹.
```
{% regroup cities by country as country_list %}
<ul>
{% for country, local_cities in country_list %}
  <li>{{ country }}
  <ul>
      {% for city in local_cities %}
        <li>{{ city.name }}: {{ city.population }}</li>
      {% endfor %}
  </ul>
  </li>
{% endfor %}
</ul>
```

### resetcycle
* `{% cycle %}`에 대해 순서를 초기화 함.
* `as` 인자를 사용하여 이름을 지정 할 수 있다.
```
{% for coach in coach_list %}
  <H1>{{ coach.name }}</H1>
  {% for athlete in coach.athlete_set.all %}
    <p class="{% cycle 'odd' 'even' %}">{{ athlete.name }}</p>
  {% endfor %}
  {% resetcycle %}
{% endfor %}
```

### spaceless
* HTML 태그 사이의 공백을 제거. 탭과 개행 포함
* 태그 사이의 간격만 제거 되며 태그와 택스트 사이의 간격은 제거 되지 않음.
```
{% spaceless %}
  <p>
    <a href="foo/">Foo</a>
  <p>
{% endspaceless %}
<p><a href="foo/">Foo</a></p>
```

### templatetag
* 템플릿 태그를 작성하는 데 사용되는 구문문자 중 하나를 출력.
```
{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}
```

### url
* 주어진 뷰와 매개변수가 일치하는 절대 경로를 반환. 특수 문자는 `iri_to_uri()` 를 사용하여 인코딩됨.
* 키워드 인자 사용 가능하며 위치인자와 키워드 인자를 같이 사용하지 말자.
* as 로 변수에 등록 가능
```
{% url 'some-url-name' arg1=v1 arg2=v2 %}
# /clients/client/123/
path('client/<int:id>/', app_views.client, name='app-views-client')
path('clients/', include('project_name.app_name.urls'))
{% url 'app-views-client' client.id %}
# 네임 스페이스로 할 경우
{% url 'myapp:view-name' %}
```

### verbatim
* 지정한 블록 내에서는 템플릿 엔진을 통한 렌더링을 하지 않는다.
* 자바 스크립트에서 `{{ }}` 를 사용하기 위함.
```
{% verbatim myblock %}
  Avoid template rendering via the {% verbatim %}{% endverbatim %} block.
{% endverbatim %}
```

### widthratio
* 주어진 값과 최대 값의 비율을 계산한 다음 주어진 값에 비율을 적용함.
```
# this_value 175 max_value 200 max_width 100 = 87.5
<img src="bar.png" alt="Bar" height="10" width="{% widthratio this_value max_value max_width %}" />
```

### with
* 복잡한 변수에 이름을 주어 사용하게 함
* `endwith` 안에서만 사용가능하고 여러개 가능
```
{% with total=business.employees.count %}
  {{ total }} employee {{ total|pluralize }}
{% endwith %}
```
{% endraw  %}