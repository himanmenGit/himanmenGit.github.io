---
layout: post
title: "UiPath WebAPI Activity를 이용하여 Json 문자열을 역직렬화 할 때 숫자가 0으로 시작하면 8진수로 관리 된다."
categories:
  - UiPath
tags:
  - UiPath
---

아래와 같은 Json 문자열을 UiPath 내에서 Dictionary<String, Object>로 변경 할 때 Int_0과 같이 숫자타입의 값이 0으로 시작하게 되면
결과 값이 8진수로 읽어진 값의 10진수로 나타난다.

```json
{
  'Name': '수민',
  'Age': '102',
  'Sex': '남자',
  'Type': 'Human',
  'Int_0': 0123,
  'Int_1': 1234,
  'Str_0': '0123',
}
```
* 테스트 코드
![](/assets/uipath/json_to_dic_sequence.png)

* 출력 결과
![](/assets/uipath/json_to_dic_result.png)

위 출력 결과의 Int_0을 보면 0123이 8진수로 취급되어 10진수 83으로 바뀐 것을 볼수 있다.

0으로 시작되는 숫자를 사용해야 할 경우 문자열로 사용하도록 하자.

