---
layout: post
title: "DRM Excel작업 동영상 캡쳐시 DRM 관련 캡쳐 방지 관련"
categories:
  - UiPath
tags:
  - UiPath
---

RPA 프로젝트나 POC중 로봇이 동작하는 것을 동영상 프로그램으로 녹화 할 경우가 생긴다.

이떄 Excel에 DRM이 걸려 있으면 캡쳐 방지가 나타나 제대로 녹화가 되자 않는다. 이 때 녹화를 하기 위한 방법을 설명 한다.

***작업용 Excel파일의 DRM은 풀려 있어야 한다.***

이 방법의 핵심을 DRM이 풀려 있는 Excel파일에 작업을 할때 자동 저장을 사용 하지 않고 작업을 하여 DRM이 걸리지 않게 하는 것이다.
그리고 모든 작업이 끝났을 때 저장을 하여 스크린 캡쳐 방지를 최소화 한다.

![](/assets/uipath/DRM_Excel.png)

마지막에 엑셀을 저장하는것만 기억하면 된다.