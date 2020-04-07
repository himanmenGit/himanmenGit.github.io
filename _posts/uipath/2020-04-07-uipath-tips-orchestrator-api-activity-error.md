---
layout: post
title: "Orchestrator의 기능을 사용하는 액티비티 에러 대처"
categories:
  - UiPath
tags:
  - UiPath
---

## 이 문서는 지속적으로 업데이트 되는 문서 입니다.

Orchestrator의 기능을 사용하는 액티비티들이 동작시 예외를 던질 경우 해결 방법에 대해 알아 보자

Orchestrator의 기능을 사용하는 액티비티들

* API
    * Orchestrator API 호출
    
* Asset
    * Get Asset
    * Get Credential
    * Set Asset
    * set Credential
    
* 알림
    * Raise Alert
    
* 작업
    * Get Jobs
    * Start Job
        * Operation returned an invalid status code 'Forbidden'
            * Orchestrator의 User Robot Role 에서 `Job Create View`, `Process View` 를 켜 준다
    * Stop Job
    
* 큐
    * Add Queue Item
    * Add Transaction Item
    * Bulk Add Queue Items
    * Delete Queue Items
    * Get Queue Items
    * Get Transaction Item
    * Postpone Transaction item
    * Set Transaction Progress
    * Set Transaction Status
    * Wait Queue Item
    
* 프로세스
    * Shiuld Stop  
