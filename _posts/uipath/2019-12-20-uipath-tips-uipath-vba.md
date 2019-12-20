---
layout: post
title: "UiPath Excel매크로 처리를 위한 VBA팁 "
categories:
  - UiPath
tags:
  - UiPath
---

엑셀 매크로를 사용하기 위해 외부에서 VBA코드를 사용하는 팁

메모장에 아래 코드를 저장하고 Invoke VBA Activity를 사용하여 매크로 코드를 실행 한다.
Invoke VBA Activity는 Excel Application Scope 내에 있어야 한다.

### 엑셀 Cell들의 가로사이즈 자동 설정

Invoke VBA 사용법
![](/assets/uipath/VBA_AutoFit.png)

코드가 적혀 있는 파일
![](/assets/uipath/VBA_Code.png)

```vb
Sub AllColumnsAutoFit()
	Cells.Select
	Cells.EntireColumn.Autofit
End Sub
```