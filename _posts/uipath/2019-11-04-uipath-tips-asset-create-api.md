---
layout: post
title: "Orchestrator Http Request로 Asset Create API 사용하기"
categories:
  - UiPath
tags:
  - UiPath
---

+ Activity : Orchestrator Http Request
    * ValueType에 따라 Value들의 Key를 변경 해줘야 한다.
    * Endpoint : `"odata/Assets"`
    * Method : `POST`
    * JsonPayload: 
    ```
      'Name': '<Name>',
      'ValueScope': 'Global or PerRobot',
      'ValueType': 'Text, Bool, Integer, or Credential',
      'StringValue': 'Value',
      'BoolValue': False,
      'IntValue':  0,
      'CredentialUsername': '<username>',
      'CredentialPassword': '<password>'
    ```