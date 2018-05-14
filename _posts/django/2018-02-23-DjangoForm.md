---
layout: post
title: "Django Form"
categories:
  - Django
tags:
  - Django
---

# Django Form 기초

`Django`는 사이트 방문자로부터 입력을 받아 `Form`을 작성한 다음 입력을 처리하고 응답하는데 도움이 되는 다양한 도구와 라이브러리를 제공함.

폼 관리는 복잡하다. 그래서 `Django` 관리자를 사용하면, 다양한 유형의 여러 데이터 항목을 `Form`으로 표시하고 `HTML`로 렌더링 하며 편리한 인터페이스를 사용하여 편집하고 서버로 반환하여 유효성을 검사하고 정리 한 다음 저장하거나 나머지 처리를 전달 할 수 있다.

`Form`을 `Django`의 `Model`과 아주 밀접하게 동작을 하게 할 수 있다. 그래서 상당부분을 단순화하고 자동화를 할 수 있으며, 대부분의 프로그래머들이 작성한 코드보다 더 안전하다.

폼으로 받은 데이터가 실제 모델이 원하는 데이터와 다를 수 있다. 예를 들어 비밀번호 문자수 제한 이라던지, 그런것을 `Django Form`에서 알아서 해줄 수 있다.

폼은 3가지 파트가 있다
* 데이터를 렌더링할 준비
* HTML Form 을 만들고
* 클라이언트로 부터 제출 된 데이터를 수신하여 처리

모델이 어떤 하나의 논리적 개체를 나타내는 것처럼 폼도 비슷하다.
폼 자체에 대해서 표현방식을 결정한다. 모델 클래스의 필드가 데이터 베이스 필드에 매칭 되는 것과 비슷한 방식으로 폼 클래스의 필드는 HTML 폼 <input> 요소에 매핑 된다.

폼의 필드는 그것 자체가 클래스다. 우리가 데이터베이스 컬럼을 만들때도 필드 안에 클래스 인스턴스를 썼는데 폼도 동일하다.

장고에서 `Form`을 렌더링 할꺼면 `view`에 `Form`을 가지고 있어야 한다.
폼 클래스로 만든 인스턴스를 컨텍스트로 전달한 다음에 그 컨텐스트로 전달된 값을 HTML markup으로 렌더링 하면 된다.

폼 클래스를 만들어 보자.

```python
from django import forms

class NameForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=100, label_suffix='')
```
`your_nanme` 이라는 필드가 있는 폼 클래스를 정의 했다. 사람이 알아 보기 쉽게 적용 했다.
`label` 같은 경우 렌더링이 될 때 `<label>`로 나타 낸다. 그리고 필드의 `max_length`는 `HTML form`에 지정된다. `html5`에서는 기본적으로 `max_length`가 제약사항에 걸리기 때문에 이것을 지키지 않은 경우 제출 자체가 안된다. 정확히는 `input` 자체에 걸리기 때문에 입력 자체가 안된다. 만약 버전이 낮은 브라우저로 해당 `max_length`를 넘겨서 제출 하게 되면 폼 자체에서 유효성 검사 오류가 자동으로 일어난다.

그리고 `Form`클래스는 `is_valid`가 존재 하는데, 모든 필드에 대한 유효성 검사 루틴을 실행한다.
모든 필드에 유효한 데이터가 들어 있으면 `True`가 리턴되고 해당 폼에 `cleaned_data`라는 속성이 추가 되고 폼에 들어있는 데이터가 `cleaned_data`로 이돟한다. 만약 모두 유효하지 못한 데이터가 있을 경우 `False`가 리턴되고 그 중 유효한 데이터만이 `cleaned_data`로 이동한다.

뷰에서 일반적으로 사용 하는 방법.

```python
from django.shortcuts import render
form django.http import HttpResponseRedirect

from .forms import NameForm

def get_name(request):
    if request.method == 'POST':
    # request.POST를 Form클래스에 전달하면
    # request.POST에 있는 데이터를 Form객체에 채운다
    # 유효성 검증을 할 수 있는 상태로 만들어줌
    # 그래서 이것을 바운딩 된 폼 binded_form 이라고 부른다.
    form = NameForm(request.POST)
    if form.is_valid():
    	thanks = form.cleanded_data['thanks']
    	if thanks:
            return HttpResponseRedirect(thanks)
        else:
            form.add_error('<input name>', '<message>')
    else:
        form = NameForm()
    
    return render(request, 'name.html', {'form':form})
```

{% raw %}
```html
<form action="" method="POST">
	{% csrf_token %}
        {% for field in form %}
        <div>
            {{ field.label_tag }}
            {{ field }}
            {% for error in field.errors %}
            <p>{{ error }}</p>
            {% endfor %}
        </div>
        {% endfor %}
	<div>
	    <button type="submit"></button>
	</div>
</form>
```
{% endraw %}
이 뷰에 GET요청이 오면 빈 폼 인스턴스를 만들어 렌더링 할 템플릿 컨텍스르에 넘겨준다.
이것은 해당 페이지를 처음 들어 왔을때 아무 것도 없는 빈 폼이 만들어 져야 하기 때문이다.
그런데 POST요청이 올 경우 폼에 데이터를 바인딩 하여 다시 만든다. 그리고 `is_valid()`를 호출하여 유효성 검사 통과 여부에 따라 어떤 폼이 들어 갈지 판단 하여 컨텍스트에 전달하여 템플릿으로 렌더링 한다. 그리고 유효성 검사를 통과 한 데이터는 `form.cleaned_data`로 접근하여 가져 올 수 있다. 그리고 에러를 넣어주고 싶을 경우 `form.add_error`를 사용하면 된다.

아니면 폼 클래스 내에서 폼 필드에 대해 사용자 정의 유효성 검사를 해줄수 있다.
```python
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()
class NameForm(forms.Form):
    ...
    
    def clean_<field_name>(self):
    	username = self.cleaned_data['username']
    	if User.objects.filter(username=username).exists():
    	    raise ValidationError('이미 사용중인 아이디 입니다.')
    	return username
```

