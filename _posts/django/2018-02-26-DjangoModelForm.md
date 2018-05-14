---
layout: post
title: "Django Model Form"
categories:
  - Django
tags:
  - Django
---

# Django Model Form

모델 클래스가 데이터베이스 구조를 파이썬 객체로 가지고 있고 어떤위젯을 쓸지 미리 정의가 되어 있다. 어떠한 필드 들이 어떤 위젯에 어떤 인풋의 위젯으로 보일지 이미 다 정의 되어 있기때문에
모델 클래스만 있으면 그것들을 가져 다 쓸수 있다 그것이 `ModelForm`이다.

class ModelForm
데이터베이스 기반 앱을 만드는경우 장고 모델과 밀접하게 매핑되는 폼을 사용할 수 있음.
만약 모델을 이미 보유하고 있고 해당 모델의 폼을 만들고 싶으면 이미 모델에서 필드를 정의 했기 때문에 폼에 필드 타입을 정의 하는것을 불 필요 하다.

```python
class ArticleForm(ModelFrom):
    class Meta:
        model = Article
        fields = ['<field>', ...]

# 빈 폼을 만듬
form = ArticleForm()

# 바운딩된 폼을 만듬
article = Article.objects.get(pk=1)
form = ArticleForm(instance=article)
```
그리고 템플릿에서 사용 할 경우

{% raw %}
```html
{% for field in form %}
<label for="{{ field.id_for_label }}">{{ field.label }}</label>
        {{ field }}
        {% if field.errors %}
        <ul>
            {% for error in field.errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
        {% endif %}
{% endfor %}
```
{% endraw %}
이런식으로 사용하면 된다.

### 폼 파일 객체
파일은 HTML 폼에서 특별한 경우. 파일은 2진 데이터 또는 다른 데이터는 텍스트 데이터로 간주된다.
HTTP는 텍스트 프로토콜 이기 때문에 2진 데이터를 다루기 위해서 특별한 요구 사항이 있다.
**enctype** 속성
이 속성은 Content-Type HTTP 헤더의 값을 지정할 수 있게 해준다. 서버에 데이터가 무슨 종류 인지 전달 하기 때문에 이 헤더는 매우 중요. 기본값으로는 application/x-www-form-urlencoded 이다.
만약 파일을 보내고 싶으면 
`method`는 POST로 지정. 왜냐면 파일 콘텐츠는 폼을 이용하여 URL 매개변수로 보낼수 없다.
`enctype`는 mutipart/form-data 라고 지정 해야 한다. 왜냐면 데이터는 여러조각으로 나눠지고 각 파일 조각에 같이 보내질 폼 바디 텍스트가 추가되기 때문.
내부적으로는 HTTP 요청을 보낼때 특정 텍스트 사이에 인코딩한 2진데이터를 넣고 해당 텍스트를 파일로 인식하게 한다.
```html
<form method="post" enctype="multipart/form-data">
  <iuput type="file" name="myFile">
  <button>Send the file</button>
</form>
```
그런데 파일을 보내도 폼을 처리하는 뷰의 `request.POST`에는 파일데이터가 오지 않는다. 파일은 `request.FILES`로 온다. 그래서 바운딩된 폼을 만들때 둘 다 넣어 줘야 한다.
```python
form = ArticleForm(request.POST, request.FILES)
```

모델 폼을 쓰게 되면 특별한 처리없이 어느정도 폼을 구현 할 수 있다. 만약 더 커스터마이징을 하고 싶다면 자바스크립트 라이브러리를 사용해야 한다.

만약 모델폼을 사용하면서 해당 폼의 필드에 `class` 속성을 지정 하고 싶을때는 이렇게 하면된다.
```python
class ArticleForm(ModelFrom):
   	...
   	     
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'name-control'
                }
            )
        }
```

그리고 모델폼의 `Validation`은 `Form`의 `Validation`과 비슷하다. 그런데 그 `Validation`에 해당 필드가 가지고 있는 제약조건을 모델필드로 생성된 폼에서 자동으로 해준다.
예를들어 `unique=True` 라던가 `max_length=20` 이런 제약조건을 알아서 유효성 검사를 해준다. 그리고 HTML단에서 검증 할 수 없는것은 장고의 뷰 단에서 `is_valid()`를 통과할때 검증이 된다,

그리고 모델 폼은 `save()`메서드가 특이 한데, 폼에 바인딩된 데이터 를 이용해서 데이터베이스 갹체를 만든다. 모델폼 클래스는 키워드 인수로 인스턴스를 가질수 있다. 그리고 만약 인스턴스가 주어졌을때 `save()`를 하면 인스턴스가 업데이트 된다.
```python
instance = get_object_or_404(<InstanceClass>, <filter>)
if request.method == 'POST':
    form = ArticleForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        form.save()
else:
    form = ArticleForm(instance=instance)
```
모델폼을 쓰면 기존 데이터를 추가하거나 수정하는 작업을 쉽게 해결 할 수 있다.