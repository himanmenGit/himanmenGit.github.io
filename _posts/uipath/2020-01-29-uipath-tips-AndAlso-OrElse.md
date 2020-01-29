---
layout: post
title: "조건문의 AndAlso 와 OrElse 사용법"
categories:
  - UiPath
tags:
  - UiPath
---

조건문 사용시 AndAlso와 OrElse의 사용법을 알아 보자

* AndAlso : 왼쪽 조건이 True일 경우에만 오른쪽 조건을 검사함.
    * 왼쪽 조건을 인스턴스가  생성 되어있는지 확인 할 때 사용
    * str_문자열 isnot Nothing AndAlso str_문자열.Equal("비교 문자")
* orElse : 왼쪽 조건이 False일 경우에만 오른쪽 조건을 검사함.(?)
    * str_문자열 is Nothing OrElse str_문자열.Equal("비교 문자")

![](/assets/uipath/AndAlso&OrElse.png)