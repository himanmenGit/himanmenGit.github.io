---
layout: post
title: "UiPath Orchestrator의 데이터베이스 패스워드 변경"
categories:
  - UiPath
tags:
  - UiPath
---

프로젝트를 진행하다보면 주기적으로 데이터베이스의 비밀번호를 변경해야 할 경우가 생긴다.

이 때 Orchestrator DB의 비밀번호가 변경 되면 어떻게 이를 반영하는지 알아 보자.

간단하다. Orchestrator설치 폴더의 web.config파일에 해당 DB의 SQL 인증 정보를 변경 해 주면 된다. 

![](/assets/uipath/password_change.png)