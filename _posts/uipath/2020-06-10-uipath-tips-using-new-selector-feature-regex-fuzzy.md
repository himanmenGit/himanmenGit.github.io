---
layout: post
title: "Selector에 Regex, Fuzzy 사용하기"
categories:
  - UiPath
tags:
  - UiPath
---

UiPath 19.10이후에 Selector의 고급 구성을 위해 `Regular expression(정규 표현식)` 과 `Fuzzy(유사성)`를 사용 할수 있습니다.

## 1. Regular expression

* Selector에서 RegEx 검색 기능을 사용 하면 한번 검색으로 여러 요소를 식별 할 수 있습니다.
* 프로세스의 이름을 식별하는 곳에는 사용 할 수 없습니다.

* 사용방법

```
matching:<tag_name>='regex' # tag_name값으로 설정된 대상을 regex로 지정 한다.
<tag_name>='<regex_command>' # tag_name을 식별하는데 RegEx문법을 사용 한다.
```

![](/assets/uipath/Selector_Regex0.png)

위 그림에서 Selector의 마지막에 `^(Hello_)`로 시작하는 부분을 보면 `matching:<name>='regex'`로 `name`태그를 RegEx문법을 사용 하겠다고 명시 해놓았습니다.

그리고 `name`태그의 값은 `^(Hello_)` 로시작하며 이후는 `이메일 형식`을 검색하는 표현식을 작성 하였습니다.

결과는 `Hello_sm.park@time-gate.com`와 같이 `Hello_`로 시작하면 뒤가 `이메일 형식`인 Selector를 찾아 냅니다.

## 2. Fuzzy

* 입력과 정확히 일치 하는것이 아닌 패턴을 기반으로 문자열을 찾을 수 있습니다.
* 자동화 프로세스중 일부가 변경되기 쉬운 경우 여러가지 속성에 따라 요소를 식별하고 Selector를 검증을 유연하게 할 수 있습니다.
* 많은 요소가 발견되면 첫번 째 요소를 선택 합니다.
* 프로세스의 이름을 식별하는 곳에는 사용 할 수 없습니다.


* 사용방법

```
matching:<tag_name>='fuzzy' # tag_name값으로 설정된 대상을 fuzzy로 지정 한다.
fuzzylevel:<tag_name>=<numerical_value> # tag_name을 식별하는데 유사정도를 0~1사이로 지정한다. 유사성이 높은것이 1
```

![](/assets/uipath/Selector_Fuzzy0.png)

위 그림은 `name`부분을 `.com`이 없이 `Hello_sm.park@time-gate`라고 지정하여 Selector를 찾을수 없는것을 알 수 있습니다.

![](/assets/uipath/Selector_Fuzzy1.png)

그래서 `name`을 `fuzzy`검색으로 지정하고 유사성을 `0.8`로 주니 Selector를 찾는 것을 확인 할 수 있습니다.

![](/assets/uipath/Selector_Fuzzy2.png)

또한 `name`을 `Hellosmpark@time-gate`로 중간에 `_`와 `.`을 없애도 Selector를 찾는것을 알 수 있습니다

![](/assets/uipath/Selector_Fuzzy3.png)

하지만 `fuzzylevel`을 `0.9`로 높이니 유사성이 모자라 다시 Selector를 찾지 못하는것을 확인할 수 있습니다.