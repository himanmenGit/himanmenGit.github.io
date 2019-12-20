---
layout: post
title: "UiPath Task 기능 사용하기."
categories:
  - UiPath
tags:
  - UiPath
---

UiPath가 2019.10~ 버전으로 업그레이드 되면서 오케스트레이터 Task라는 기능이 생겼습니다.
![](/assets/uipath/Task_OrchestratorCloud.png)

이 기능은 프로세스가 동작 하다가 오케스트레이터에서 유저의 입력 받기 전까지 동작을 중지 하다가 입력을 받으면
다시 동작을 진행 하는 기능 입니다.

***이 기능을 사용하기 위해서는 오케스트레이터와 필수적으로 연결이 필요 합니다.***
![](/assets/uipath/Orchestrator_Connect.png)

또한 이 기능을 사용하기 위해서는 템플릿의 `오케스트레이션 프로세스` 를 사용 해야 합니다.
![](/assets/uipath/Task_Template.png) 

그리고 관련 기능 액티비티를 사용하기 위해서는 `UiPath.FormActivityLibrary`패키지가 필요 합니다. 설치 합시다.
![](/assets/uipath/Task_Package.png)

사용 코드는 이렇게 쓰면 됩니다.
![](/assets/uipath/Task_Script.png)

Form Designer은 아래 처럼 설정 해 주었습니다.
![](/assets/uipath/Task_Form.png)

이후 실행하고 진행하면 
* `Create Form Task`에서 입력 Form을 만들고 요청후 `Wait for Form Task And Resume`에서 기다립니다.
* 오케스트레이터에서 입력하면 해당 입력을 기다리다 반환받아 입력 데이터를 사용 할 수 있습니다.

실행 및 일시정지
![](/assets/uipath/Task_RunStop.png)

오케스트레이터 확인
![](/assets/uipath/Task_OrchestratorTask.png)

오케스트레이터 Form 입력
![](/assets/uipath/Task_OrchestratorTaskInput.png)

오케스트레이터 Form 입력 완료
![](/assets/uipath/Task_OrchestratorTaskResult.png)

일시 정지 해제 및 결과
![](/assets/uipath/Task_Result.png)

해당 결과 데이터를 가지고 이후 작업을 진행 하면 됩니다.