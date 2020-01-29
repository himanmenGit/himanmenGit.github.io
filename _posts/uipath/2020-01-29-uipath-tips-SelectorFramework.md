---
layout: post
title: "Selector의 프레임워크 종류 변경"
categories:
  - UiPath
tags:
  - UiPath
---

### 셀렉터 프레임워크 변경

Selector Indicate에서 F4를 누르면 기본 / AA(Active Accessibility)/ UIA(UI Automation) 으로 토글이 가능

* 기본값 : UiPath에서 자체 개발한 라이브러리입니다. 일반적으론 해당 라이브러리를 사용합니다.
* Active Accessibility(AA) : 기본 라이브러리에서 선택되지 않고, MFC, VB6 버전과 같이 오래 전 개발된 프로그램의 엘리먼트를 선택해야할 경우 사용합니다.
* UI Automation(UIA) : 기본 라이브러리에서 선택되지 않고, WPF와 같이 비교적 최근 도입된 UI 프레임워크 기반의 프로그램의 엘리먼트를 선택해야할 경우 사용합니다.

![](/assets/uipath/selector_framework.png)

출처: [또치의 삽질 보관함](https://ddochea.tistory.com/45)