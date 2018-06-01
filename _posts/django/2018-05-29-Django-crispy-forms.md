---
layout: post
title: "Django crispy-forms"
categories:
  - Django
tags:
  - Django
  - Package
---

# Django-crispy-forms
폼 레이아웃의 고급 기능들. 폼을 트위터의 부트스트랩 폼 엘리먼트와 스타일로 보여준다.
`django-floppyforms` 와 함께 쓰기 좋아서 빈번하게 함께 쓰인다.

장고 폼을 부트스트랩같은 스타일로 변환하여 보여준다. 상세 설정도 폼의 인스턴스 단위로 할 수 있다.

## 설치
```bash
pip install django-crispy-forms
```

## 설정
```python
CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = (
    ...
    'crispy_forms',
)
```
{% raw %}
## 사용
`html` 에서 사용
```html
# index.html
{% load crispy_forms_tags %}
<!DOCTYPE html>
<html>
  <head>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" />
  </head>
  <body>
    <div class="container">
      <div class="row">
        {% crispy form %}
      </div>
    </div>
  </body>
</html>
```
{% endraw  %}

`MainView`
```python
from django.views.generic import FormView

from main.forms import SimpleForm, CreditCardForm, CartForm

class MainView(FormView):
    template_name = 'index.html'
    form_class = SimpleForm
```

`forms.py` 에서 사용
```python
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

class SimpleForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember Me?")

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'login', css_class='btn-primary'))

class CartForm(forms.Form):
    item = forms.CharField()
    quantity = forms.IntegerField(label="Qty")
    price = forms.DecimalField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        'item',
        PrependedText('quantity', '#'),
        PrependedAppendedText('price', '$', '.00'),
        FormActions(Submit('login', 'login', css_class='btn-primary'))
    )
class CreditCardForm(froms.Form):
    fullname = forms.CharField(label="Full Name", required=True)
    card_number = forms.CharField(label="Card", required=True, max_length=16)
    expire = forms.DateField(label="Expire Date", input_formats=['%m/%y'])
    ccv = forms.IntegerField(label="ccv")
    notes = forms.CharField(label="Order Notes", widget=forms.Textarea())

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('fullname', css_class='input-sm'),
        Field('card_number', css_class='input-sm'),
        Field('expire', css_class='input-sm'),
        Field('ccv', css_class='input-sm'),
        Field('notes', rows=3),
        FormActions(Submit('purchase', 'purchase', css_class='bth-primary'))
    )    
```
