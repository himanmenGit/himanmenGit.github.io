---
layout: post
title: "Exception.Source가 제대로 나오지 않는 버그."
categories:
  - UiPath
tags:
  - UiPath
---

여러 `Activity`들을 `Try/Catch`로 감싸고 예외가 발생하면 어떤 `Activity`에서 예외가 발생했는지 알고 싶을 때
`Exception.Source`를 사용 하는데, 이 때 출력이 제대로 나오지 않는 버그(?)가 있으며, 이를 우회하여 제대로 출력을 
할수 있게 해보자. 

1. 문제점 확인

* 워크 플로우
![](/assets/uipath/exception_source_bug.png)

* 로그 출력
![](/assets/uipath/exception_source_bug_result.png)

위 출력에서 `exception.source` 가 `UiPath.UiAutomation.Activities`로 나오는것을 확인 할 수 있다.
하지만 우리는 `Type into - 메모장`이라는 것을 알려고 로깅을 했다.

2. 문제점 해결

이 문제를 해결 하기 위해서는 비즈니스 코드(Type into)들을 다른 워크 플로우에 넣어서 해당 워크 플로우를 `Invoke Workflow`로 호출하여야 한다.
그러면 `Try/Catch`에서 `exception.soruce`가 정상적으로 작동 할 것이다.

* 비즈니스 로직 워크플로우
![](/assets/uipath/exception_source_inner.png)

* 로깅 워크플로우
![](/assets/uipath/exception_source_outter.png)

* 로그 출력
![](/assets/uipath/exception_source_result.png)

위 출력에서 `exception.source`가 `Type into - 메모장` 이라는 문구를 출력하는 것을 확인 할 수 있다.