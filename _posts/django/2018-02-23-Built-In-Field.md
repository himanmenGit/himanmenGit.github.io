---
layout: post
title: "Django 내장 필드"
categories:
  - Django
tags:
  - Django
---

# Form fields
### class field(\*\*kwargs)
* 폼 클래스를 만들 때 가장 중요한 것은 폼의 필드를 정의 하는 것 이다.

### Field.clear(value)
* 각 `Field` 인스너스에는 `clean()` 메서드가 있다.
* 이는 단일 인수를 사용하여 `django.forms.ValidationError` 를 발생 시키거나 클린 값을 반환한다.
```
f = forms.EmailField()
f.clean('foo@example.com')
# foo@example.com
f.clean('Invalud email address')
# ValidationError:[' Enter a valid email address.']
```

# Core Field arguments
* 각 `Field` 클래스 생성자는 아래 인수들을 가지고 있다.
* 일부 `Field` 클래스는 필드 별 인수를 추가로 가져 오지만 항상 다음 사항을 따라야 한다.

### required
#### Field.required
* 기본적으로 각 `Field` 클래스는 값이 필요 하다고 가정.
* `None`또는 빈문자열 중 하나를 전달하면 `clean()`은 `ValidationError`을 발생.
* 기본 값 은 `required=True`
```
from django import forms
f = forms.CharField()
f.clean('foo')
# foo
f.clean('')
# ValidationError:['This field is required.']
f.clean(None)
# ValidationError:['This field is required.']
f.clean(' ')
# ' '
f.clean(0)
# 0
f.clean(True)
# True
```
```
f = forms.CharField(required=False)
f.clean('foo')
# foo
f.clean('')
# ''
f.clean(None)
# ''
f.clean(0)
# 0
```
* `required=False`를 하고 빈값을 `clean()`하면 표준화 된 빈값을 반환
* 다른 필드의 경우 `None`이 올 수도 있다.

### Label
#### Field.Label
* `label`인수를 사용하여 레이블을 `Form`에 표시 될때 적용할 수 있다.
```
from django import forms
class CommentForm(forms.Form):
    name = forms.CharField(label='이름')
    url = forms.URLField(label='웹사이트', required=False)
    comment = forms.CharField()
f = CommentForm(auto_id=False)
print(f)
```
```html
<tr><th>이름:</th><td><input type="text" name="name" required/> </td></tr>
<tr><th>웹사이트:</th><td><input type="text" name="url" /> </td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" required/> </td></tr>
```
### label_suffix
#### Field.label_suffix
* `label_suffix`를 사용하면 각 필드의 `label`값 뒤에 오는 접미사 `:`등을 재정의 할 수 있다.
```
class ContactForm(forms.Form):
    age = forms.IntegerField()
    nationality = forms.CharField()
    captcha_answer = forms.IntegerField(label='2 + 2', label_suffix=' =')
f = ContactForm(label_suffix='?')
print(f.as_p())
```
```html
<p><label for="id_age">Age?</label><input id="id_age" name="age" type="number" required /></p>
<p><label for="id_nationality">Nationality?</label><input id="id_nationality" name="nationality" type="text" required /></p>
<p><label for="id_captcha_answer">2 + 2 =</label><input id="id_captcha_answer" name="captcha_answer" type="number" required /></p>
```

### initial
#### Field.initial
* 각 필드에 대하여 기본 값을 제공 할 수 있다.
* `value='initial'`
```
from django import forms
class CommentForm(forms.Form):
    name = forms.CharField(initial='이름')
    url = forms.URLField(initial='http://')
    comment = forms.CharField()
    day = forms.DateField(initial=datetime.date.today)
f = CommentForm(auto_id=False)
# or
default_data = {'name':'이름', 'url':'http://'}
f = CommentForm(default_data, auto_id=False)
print(f)
```

  ```html
  <tr><th>Name:</th><td><input type="text" name="name" value="이름" required /></td></tr>
  <tr><th>Url:</th><td><input type="text" name="url" value="http://" required /></td></tr>
  <tr><th>Comment:</th><td><input type="text" name="comment" required /></td></tr>

  <tr><th>Day:</th><td><input type="text" name="day" value="2/24/2018" required /></td></tr>
  ```
* 딕셔너리로 전달 할 수도 있지만 안하는게 좋다. 유효성 검사가 시작되어서 HTML에 유효성 검사 오류가 포함된다.
* 딕셔너리로 전달시 값을 지정 하지 않고 빈값을 넣으면 유효성 검사가 실패함.

### widget
#### Field.widget
* 위젯 인수를 사용하여 필드를 렌더링 할 떄 사용할 위젯 클래스를 지정 할 수 있다.
```
from django import forms
class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField(widget=forms.Textarea)
```

### help_text
#### Field.help_text
* `help_text`를 사용하여 필드에 설명 텍스트를 지정 할 수 있다.
* `HTML` 이스케이프 처리 되지 않는다.
```
from django import forms
class HelpTextContactForm(forms.Form):
    subject = forms.CharField(max_length=100, help_text='100 characters max.')
    message = forms.CharField()
    sender = forms.EmailField(help_text='A valid email address, please.')
    cc_myself = forms.BooleanField(required=False)
f = HelpTextContactForm(auto_id=False)
print(f.as_table())
print(f.as_ul())
```

  ```HTML
  <!-- as_table() -->
  <tr><th>Subject:</th><td><input type="text" name="subject" maxlength="100" required /><br /><span class="helptext">최대 100문자</span></td></tr>
  <tr><th>Message:</th><td><input type="text" name="message" required /></td></tr>
  <tr><th>Sender:</th><td><input type="email" name="sender" required /><br /><span class="helptext">이메일 주소를 확인해 주세요</span></td></tr>
  <tr><th>Cc myself:</th><td><input type="checkbox" name="cc_myself" /></td></tr>

  <!-- as_ul() -->
  <li>Subject: <input type="text" name="subject" maxlength="100" required /> <span class="helptext">최대 100문자</span></li>
  <li>Message: <input type="text" name="message" required /></li>
  <li>Sender: <input type="email" name="sender" required /> <span class="helptext">이메일 주소를 확인해 주세요</span></li>
  <li>Cc myself: <input type="checkbox" name="cc_myself" /></li>

  <!-- as_p -->
  <p>Subject: <input type="text" name="subject" maxlength="100" required /> <span class="helptext">최대 100문자</span></p>
  <p>Message: <input type="text" name="message" required /></p>
  <p>Sender: <input type="email" name="sender" required /> <span class="helptext">이메일 주소를 확인해 주세요</span></p>
  <p>Cc myself: <input type="checkbox" name="cc_myself" /></p>
  ```

### error_messages
#### Field.error_messages
* `error_messages` 인수를 사용하여 필드에서 발생 하는 기본 메시지를 대체 가능.
* 덮어 쓰려는 오류 메시지와 일치하는 키 딕셔너리를 전달.
```
from django import forms
generic = forms.CharField()
generic.clean('')
# ValidationError:['This field is required.']
name = forms.CharField(error_messages={'required': '이름을 입력해 주세요'})
name.clean('')
# ValidationError: ['이름을 입력해 주세요']
```

### validators
#### Field.validators
* 필드에 대한 유효성 검사 함수 목록을 제공

### localize
#### Field.localize
* `Form`의 데이터 입력의 현지화를 가능하게 한다.

### disabled
#### Field.disabled
* `disabled` 부울 인수를 `True`로 설정하면 비활성화된 `HTML`특성을 사용하는 `Form`필드가 비활성화 되어 사용자가 편집 할 수 없다.
* 사용자가 제출 한 필드의 값을 조작하더라도 폼의 초기 데이터 값에 비해 무시 된다.

### 필드 데이터가 변경 되었는지 확인
### has_chaged()
#### Field.has_changed()
* 필드 값이 초기 값에서 변경 되었는지 확인하는데 사용 `True` 또는 `False` 반환.

### 내장 필드 클래스
* 위젯을 지정 하지 않은 경우 사용되는 기본 위젯을 설명
* 빈 값을 제공 할 때 반환되는 값도 지정.
> 모든 필드 서브 클래스는 기본적으로 `required=True`

### BooleanField
#### class BooleanField(\*\*kwargs)
* 기본 위젯 : `CheckboxInput`
* 빈 값    : `False`
* 표준화   : `True` or `False`
* 필드의 `required=True`이면 값이 `True`인지 확인
* 에러메시지키 : required

### CharField
#### class CharField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : `empty_value`로 준것
* 표준화   : 문자열
* `max_length` 또는 `min_length`가 제공되면 유혀성을 검사. 이니면 모든 입력이 유효
* 에러메시지키 : required, max_length, min_length

#### min_length, max_length
* 문자열이 최소또는 최대 인지 확인

#### strip
* `True`(기본값) 이면 앞뒤 공백을 제거

#### empty_value
* `empty`를 나타내는데 사용하는 값 기본값은 빈 문자열.

### ChoiceField
#### class ChoiceField(\*\*kwargs)
* 기본 위젯 : `Select`
* 빈 값    : 빈문자열
* 표준화   : 문자열
* 지정된 값이 `choices`목록에 있는지 확인
* 에러메시지키 : required, invalid_choice
invalid_choice 오류 메시지에는 %{value)s가 포함될 수 있으며, 이값은 선택한 `choice`로 바뀐다.

#### choices
* 2튜플의 반복 가능한 목록 또는 반복가능 한것을 호출 하는 것.

### TypedChoiceField
#### class TypedChoiceField(\*\*kwargs)
* `ChoiceField`와 동일하지만 `coerce`와 `empty_value`를 추가 인수로 가진다.
* 기본 위젯 : `Select`
* 빈 값    : `empty_value`로 준것
* 표준화   : `coerce`인수에서 제공한 유형의 값
* `choices`와 `coerced`에 있는지 확인
* 에러메시지키 : required, invalid_choice

#### coerce
* 하나의 인수를 취하여 강제 변환 된 값을 반환하는 함수.

#### empty_value
* `empty`를 나타내는데 사용할 값. 빈 문자열이 기본이고 선택사항은 없음.

### DateField
#### class DateField(\*\*kwargs)
* 기본 위젯 : `DateInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `datetime.date`
* 지정된 값이 `datetime.date, datetime.datetime`또는 특정 날짜 형식으로 지정된 문자열인지 확인
* 에러메시지키 : required, invalid

#### input_format
* 문자열을 유효한 `datetime.date`객체로 변환하려고 시도하는데 사용되는 형식 목록.

### DateTimeField
#### class DateTimeField(\*\*kwargs)
* 기본 위젯 : `DateTimeInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `datetime.datetime`
* 지정된 값이 `datetime.datetime, datetime.date`또는 특정 날짜 형식으로 지정된 문자열인지 확인
* 에러메시지키 : required, invalid

#### input_format
* 문자열을 유효한 `datetime.datetime`객체로 변환하려고 시도하는데 사용되는 형식 목록.

### DecimalField
#### class DecimalField(\*\*kwargs)
* 기본 위젯 : `Field.localize`가 `False`인 경우 `NumberInput` 그렇지 않으면 `TextInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `decimal`
* 지정된 값이 10진수 인지 검증. 앞뒤 공백은 무시
* 에러메시지키 : required, invalid, max_value, min_value, max_digits, max_decimal_places, max_whole_digits

* `max_value` 와 `min_value`의 오류메시지에는 `%(limit_value)s`가 포함될 수 있다.
* 마찬가지로 `max_digits, max_decimal_places, max_whole_digits` 오류 메시지에는 `%(max)s`가 포함 될 수 있다.

#### max_value, min_value
* 필드에서 허용되는 값의 범위를 제어 `decimal.Decial`값으로 지정 해야 함

#### max_digits
* 값에 사용할 수 있는 최대 자리수 (소수점 앞자리와 소수점 이하 자리, 앞의 0은 무시)

#### decimal_places
* 소수점 이하 자릿수의 최대 수는 허용

### DurationField
#### class DurationField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `timedelta`
* 지정된 값이 `timedelta`로 변환될 수 있는 문자열 인지 확인.
* 에러메시지키 : required, invalid

### EmailField
#### class EmailField(\*\*kwargs)
* 기본 위젯 : `EmailInput`
* 빈 값    : 빈 문자열
* 표준화   : 문자열
* 적당히 복잡한 정규 표현식을 사용하여 지정된 값이 유효한 메일 주소인지 확인.
* 에러메시지키 : required, invalid
* `max_length, min_length`를 선택인수로 사용 가능

### FileField
#### class FileField(\*\*kwargs)
* 기본 위젯 : `ClearableFileInput`
* 빈 값    : `None`
* 표준화   : 파일 내용과 파일 이름을 단일 객체로 래핑하는 `UploadedFile`객체
* 비어 있지 않은 파일 데이터가 양식에 바인드 되었는지 검증 할수 있다.
* 에러메시지키 : required, invalid, missing, empty, max_length

* 유효성 검사를위해 `max_length, allow_empty_file`이 있다. 파일이름의 길이를 체크, 파일 내용이 비어있는지 체크.
* 폼에서 `FileField`를 사용하는 경우 파일 데이터를 폼에 바인딩 해야 한다.

### FilePathField
#### class FilePathFIeld(\*\*kwargs)
* 기본 위젯 : `Select`
* 빈 값    : `None`
* 표준화   : 문자열
* 선택한 `choice`가 `choices`목록에  있는지 확인
* 에러메시지키 : required, invalid_choice
* 이 필드는 특정 디렉토리의 파일에서 선택을 허용. 5개의 추가인수가 필요. 경로만 필요.

#### path
* 표시할 디렉토리의 절대 경로. 이 디렉토리가 있어야 한다.

#### recursive
* `False`인 경우 경로의 내용만 선택항목으로 제공
* `True`인 경우 모든 하위 항목이 선택항목으로 제공

#### match
* 정규식 패턴. 이 표현식과 이름이 일치하는 파일만 선택 항목으로 사용할 수 있다.

#### allow_files
* 선택 옵션. `True`또는`False` 기본값은 `True` 지정된 위치의 파일을 포함 할지 여부를 결정 한다. `this`또는 `allow_folders`가 `True`여야만 한다.

#### allow_folders
* 선택 옵션. `True`또는 `False` 기본값은 `False` 지정된 위치의 폴더를 포함 할지 여부를 결정 한다. `this` 또는 `allow_files`가 `True`여야만 한다.

#### FloatField
### class FloatField(\*\*kwargs)
* 기본 위젯 : `Field.localize`가 `False`인 경우 `NumberInput` 아니면, `TextInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `float`
* 지정된 값이 `float`인지 확인. 파이썬의 `float()`함수처럼 앞뒤의 공백을 허용.
* 에러메시지키 : required, invalid, max_value, min_value
* 검증에 `max_value, min_value`를 선택옵션으로 받고, 이는 필드의 허용 범위를 확인한다.

#### ImageField
### class ImageFIeld(\*\*kwargs)
* 기본 위젯 : `ClearableFileInput`
* 빈 값    : `None`
* 표준화   : 파일 내용과 파일 이름을 단일 객체로 래핑하는 `UploadedFile`객체
* 파일데이터가 폼에 바인드 되었는지 확인하고, 파일이 `Pillo`가 이해하는 이미지 형식인지 확인한다.
* 에러메시지키 : required, invalid, missing, empty, invalid_image
* `ImageField`를 사용하려면 `Pillow` 를 설치 해야 한다.
* `Form`에 `ImageField`를 사용할 경우 데이터를 `Form`에 바인딩 해야 한다.

#### IntegerField
### class IntegerField(\*\*kwargs)
* 기본 위젯 : `Field.localize`가 `False`면 `NumberInput` 아니면, `TextInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `integer`
* `integer`인지 확인. 파이썬의 `int()` 함수처럼 앞뒤의 공백을 허용.
* 에러메시지키 : required, invalid, max_value, min_value
* `max_value` 와 `min_value`오류 메시지에는 `%(limit_value)s`가 포함될수 있다.
* 유효성 검사를 위해 두개의 선택 인수를 가짐.

#### min_value, max_value
* 필드의 범위를 제한한다.

### GenericIPAddressField
#### class GenericIPAddressFIeld(\*\*kwargs)
* `IPv4`또는 `IPv6`가 포함된 필드.
* 기본 위젯 : `TextInput`
* 빈 값    : 빈문자열
* 표준화   : 문자열.
* 유효한 IP주소 인지 확인한다.
* 에러메시지키 : required, invalid

#### protocol
* 지정된 프로토콜에 대한 유효 입력을 제한. 허용되는 값은 모두 `IPv4`또는 `IPv6`이고 대소문자 구별하지 않는다.

#### unpack_ipv4
`::ffff:192.0.2.1` 과 같이 `IPv4` 매핑된 주소의 압축을 푼다. 이 옵셥을 사용하면 주소가 `192.0.2.1`로 압축해제 됩니다. 기본값은 사용 불가. 프로토콜이 `both`로 설정된 경우에만 사용 가능.

#### MultipleChoiceField
### class MultipleChoiceField(\*\*kwargs)
* 기본 위젯 : `SelectMultiple`
* 빈 값    : 빈 리스트
* 표준화   : 문자열 리스트
* 지정된 값 리스트에 있는 모든 값이 선택 리스트에 있는지 확인.
* 에러메시지키 : required, invalid_choice, invalid_list
* `invaliid_choice`에러 메시지에는 %(value)s가 포함될수 있으며, 이값은 선택적으로 바뀐다.


### TypeMultipleCHoiceField
#### class TypeMultipleCHoiceField(\*\*kwargs)
* `MultipleChoiceField`처럼 동작하지만 두개의 특별한 인수 `coerce, empty_value`를 가진다.
* 기본 위젯 : `SelectMultiple`
* 빈 값    : `empty_value`로 넣은 것.
* 표준화   : `coerce` 인수로 넘겨진 값 리스트.
* 지정된 값 리스트에 있는 모든 값이 선택 리스트에 있는지 확인하고 강제적용 가능.
* 에러메시지키 : required, invalid_choice
* `invaliid_choice`에러 메시지에는 %(value)s가 포함될수 있으며, 이값은 선택적으로 바뀐다.
* `TypedChoiceField`와 같이 `coerce`와 `empty_value`를 사용한다.

### NullBooleanField
#### class NullBooleanField(\*\*kwargs)
* 기본 위젯 : `NullBooleanSelect`
* 빈 값    : `None`
* 표준화   : 파이썬의 `True`, `False`, `None`
* 지정된 값 리스트에 있는 모든 값이 선택 리스트에 있는지 확인.
* 유효성 검사가 없다. 즉 `ValidationError`을 발생시키지 않는다.

### RegexField
#### class RegexField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : 빈 문자열
* 표준화   : 문자열
* 지정된 값이 특정 정규 표현식과 일치하는지 확인.
* 에러메시지키 : required, invalid
* 두개의 필수 인수를 가짐

#### regex
* 정규 표현식은 문자열 또는 컴파일된 정규표현식 객체로 표현됨.
* 또한 `CharField`와 마찬가지로 `max_value`, `min_length`, `strip`을 가짐.

#### strip
* 기본값은 `False`이고 이 옵션을 사용하면 정규식 유효성 검사 전에 스트리핑 된다.

### SlugField
#### class SlugField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : 빈 문자열
* 표준화   : 문자열
* 지정된 값에 문자, 숫자, 언더스코어, 하이픈만 포함되는지 확인.
* 에러메시지키 : required, invalid
* 이 필드는 폼에서 모델 `SlugField`를 나타내는데 사용.

#### allow_unicode
* 필드에 `ASCII`문자 이외에 유니코드 문자를 허용하도록 하는 것.
* 기본값은 `False`

#### TimeField
#### class TimeField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : `None`
* 표준화   : 파이썬의 `datetime.time`
* 지정된 값이 `datetime.time`형식인지 특정 시간형식으로 형식화된 문자열인지 확인.
* 에러메시지키 : required, invalid

#### input_formats
* 문자열을 유효한 `datetime.time`객체로 변환 시도하는데 사용되는 형식 목록


### URLField
#### class URLField(\*\*kwargs)
* 기본 위젯 : `URLInput`
* 빈 값    : 빈 문자열
* 표준화   : 문자열
* 지정된 값이 유효한 `URL`인지 확인.
* 에러메시지키 : required, invalid

#### max_length, min_length
* `CharField`의 `max_length`,`min_length`와 같다.

### UUIDField
#### class UUIDField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : 빈 문자열
* 표준화   : `UUID` 객체
* 에러메시지키 : required, invalid
* 이 필드는 `UUID` 생성자에 대한 16진수 인수로 허용되는 모든 문자열 형식을 허용한다.

### 약간 복잡한 내장 필드 클래스는
### ComboField
#### class ComboField(\*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : 빈 문자열
* 표준화   : 문자열
* `ComboField`의 인수로 지정된 각필드에 대해 지정된 값의 유효성을 확인
* 에러메시지키 : required, invalid

#### fields
* 필드값의 유효성을 검사 하는데 사용해야하는 필드 리스트
```
from django.forms import ComboField
f = ComboField(fields=[CharField(max_lenfth=20), EmailField()])
f.clean('test@example.com')
# test@example.com
f.clean('longemailaddress@example.com')
# ValidationError: ['Ensure this value has at most 20 charachters (it has 28).']
```

### MultiValueField
#### class MultiValueField(fields=(), \*\*kwargs)
* 기본 위젯 : `TextInput`
* 빈 값    : 빈 문자열
* 표준화   : 하위 클래스에서 `compress` 함수로 반환 한 유형
* `MultiValueField`의 인수로 지정된 각필드에 대해 지정된 값의 유효성을 확인
* 에러메시지키 : required, invalid, incomplete
* 하나의 값을 생성하는 여러 필드의 논리를 집계(?)
* 이 필드는 추상적이며 서브클래싱을 해야 한다. 단일 값 필드와 달리 `MultiValueField`의 하위 클래스는 `clean()`을 구현하지 말고 `compress()`를 구현해야 한다.

#### fields
* 하나의 값으로 결합된 필드의 튜플. 첫번째 값은 첫번째 필드, 두번째 값은 두번 째 필드에서 지워지고, 모두 지워지면 빈 값 목록이 다음 필드에 `compress()`에 의한 단일값으로 결합됨.

### require_all_fields
* 기본값은 `True`이며, 이 경우 필드에 값이 제공되지 않으면, 유효성 검사오류가 발생 한다.
* `False`로 할 경우 `Field.required`를 개별적으로 적용이 가능함. `required field`에 제공된 값이 없으면 유효성 검증 오류 발생
* `MultiValueField`의 하위클래스에서 기본 불완전 오류메세지를 정의 하거나 각 필드마다 다른 메시지를 정의 할 수 있다.

```
from django.core.validators import RegexValidator

class PhoneField(MultiValueField):
  def __init__(self, \*\*kwargs):
    # Define one message for all fields.
    error_messages = {
        'incomplete': 'Enter a country calling code and a phone number.'
    }
    # or define a different message for each field.
    fields = (
        CharField(
            error_messages={'incomplete':'Enter a country calling code.'},
            validators=[
                RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code'),
            ],
        ),
        CharField(
            error_messages={'incomplete': 'Enter a phone number.'},
            validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
        ),
        CharField(
            validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension')],
            required=False,
        ),
    )
    super().__init__(
        error_message=error_message, fields=fields,
        require_all_fields=False, **kwargs
    )
```

#### widget
* `django.forms.MultiWidge`의 서브 클래스여야 하고, 기본값은 `TextInput`이다. 지금의 경우 별로 유용하지 않다.

#### compress(data_list)
* 유효한 값 리스트를 가져와서 해당 값의 압축된 버전을 단일 값으로 반환.
* 예를 들어 `SplitDateTimeField`는 시간필드와 날짜필드를 `datetime`객체로 결합하는 하위 클래스다.
* 이 메소드는 서브 클래스에서 구현 되어야 한다.

### SplitDateTimeField
#### class SplitDateTimeField(\*\*kwargs)
* 기본 위젯 : `SplitDateTimeWidget`
* 빈 값    : `None`
* 표준화   : 파이썬의 `datetime.datetime`객체
* `MultiValueField`의 인수로 지정된 각필드에 대해 지정된 값의 유효성을 확인
* 에러메시지키 : required, invalid, incomplete

#### input_date_formats
* 문자열을 유효한 `datetime.date`객체로 변환하기위해 사용하는 형식 목록
* `input_date_formats`의 인수가 재공되지 않으면, `DataField`의 기본 입력 형식이 사용됨.

#### input_time_foramts
* 문자열을 유효한 `datetime.time`객체로 변환하기위해 사용하는 형식 목록
* `input_time_formats`의 인수가 재공되지 않으면, `TimeField`의 기본 입력 형식이 사용됨.

### relationships을 처리 하는 필드
* `ModelChoiceField`와 `ModelMultipleChoiceField` 필드는 모델 간의 관계를 나타낼 수 있다.
* 두 필드 모두 필드에 대한 선택 사항을 만드는데 사용하는 단일 `queryset` 매개 변수가 필요하다.
* 폼 유효성 검사시 이 필드는 하나의 모델 객체 (`ModelChoiceField`의 경우) 또는 여러 모델 객체 ('ModelMultipleChoiceField'의 경우)를 폼의 cleaned_date 딕셔너리에 위치한다.
* 더 복잡한 사용의 경우 폼 필드를 선언할 때 `query=None`를 지정한다음 폼의 `__init__()`메소드에서 `qureyset`을 채울수 있다.
```
class FooMultipleChoiceForm(forms.Form):
    foo_select = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foo_select'].queryset = ...
```

### ModelChoiceField
#### class ModelChoiceField(\*\*kwargs)
* 기본 위젯 : `Select`
* 빈 값    : `None`
* 표준화   : 모델 객체
* 지정된 `id`가 `queryset`에 존재 하는지 확인
* 에러메시지키 : required, invalid_choice
* `foreignKey`를 나타내는데 적합한 단일 모델 객체를 선택 가능. 100개가 넘는 항목에는 사용하지 말것. 효율이 떨어짐

#### queryset
* 필드의 선택사항이 파생되고 사용자의 선택을 확인하는데 사용되는 모델 객체의 `QuerySet`. 폼이 렌더링 될 때 평가 된다.

#### empty_label
* 기본적으로 `ModelChoiceField`에서 사용하는 `<select>` 위젯은 리스트의 가장위에 빈 선택 항목을 가진다.
* `empty_label`속성을 사용하여 이 레이블의 텍스트를 변경하거나 `empty_label`을 `None`으로 설정하여 빈 레이블을 완전히 비활성화 시킬수 있다.
```
# A custom empty label
field1 = forms.ModelChoiceField(quertset=..., empty_label="(Nothing)")

# No empty label
field2 = forms.ModelChoiceField(queryset=..., empty_label=None)
```

#### to_field_name
* 이 옵션 인수는 필드의 위젯에서 선택값으로 사용할 필드를 지정하는데 사용.
* 모델의 유니크 필드 인지 확인. 아니면 선택한 값이 두개 이상의 객체와 일치 가능.
* 기본적으로 `None`으로 설정 각 객체의 기본키가 사용
```
# No custom to_field_name
field1 = forms.ModelChoiceField(queryset=...)
```
```HTML
<select id="id_field1" name="field1">
  <option value="obj1.pk">Object1</option>
  <option value="obj2.pk">Object2</option>
  ...
</select>
```
그리고
```
# to_field_name provided
field2 = forms.ModelChoiceField(queryset=..., to_field_name="name")
```
```HTML
<select id="id_field12" name="field12">
  <option value="obj1.name">Object1</option>
  <option value="obj2.name">Object2</option>
  ...
</select>
```
* 모델의 `__str__()`메서드가 호출되어 필드의 선택에 사용할 객체의 문자열 표현을 생성.
* 커스텀 표현을 제공하려면 `ModelChoiceField`를 서브 클래스화 하여 `label_from_instance`를 대체하라.
* 이 메서드는 모델 객체를 수신하고 모델 객체를 나타내는 데 적합한 문자열을 반환해야 한다.
```
from djnago.forms import ModelChoiceField
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
      return "My Object #%i" % obj.id
```

### ModelMultipleChoiceField
#### class ModelMultipleChoiceField
* 기본 위젯 : `SelectMultiple`
* 빈 값    : 빈 쿼리셋 (`self.queryset.none()`)
* 표준화   : 모델 인스턴스의 쿼리셋
* 지정된 값 목록의 모든 ID 쿼리셋에 있는지 확인.
* 에러메시지키 : required, invalid_choice, invalid_pk_value
* `invalid_choice` 메시지에는 `%(value)s`가 포함될 수 있으면 `invalid_pk_value`메시지에는 `%(pk)s`가 포함될 수 있다.
* 다 대다 관계를 나타내는 데 적합한 하나 이상의 모델 객체를 선택할 수 있다.
* `ModelChoiceField`와 마찬가지로 `label_from_instance`를 사용하여 객체표현을 커스텀할수 있다.

#### queryset
* `ModelChoiceField.queryset`과 같음

#### to_field_name
* `ModelChoiceField.to_field_name`과 같음

### 사용자 정의 필드 만들기
* 내잘된 `Field`클래스가 필요한 것에 맞지 않으면 사용자 정의 `Field`를 만들 수 있다.
* `django.forms.Field`의 하위 클래스를 만들고 `clean()`메소드를 구현하고 `__init__()`가 핵심인수 (`required, label, initial, widget, help_text`)를 허용 하는것.
* `get_bound_field()`를 재정의 하여 필드에 접근 하는 방법을 커스머 할 수도 있다.
