---
layout: post
title: "PowerShell로 엑셀 비밀번호 해제하기"
categories:
  - UiPath
tags:
  - UiPath
---

PowerShell을 쓰기 위해 `Invoke Power Shell Activity`를 사용한다.

Excel 비밀번호 저장 코드
* $LoadPath - 비밀번호를 해제할 엑셀파일 경로
* $Password - 현재 비밀번호

```powershell
"$excel = New-Object -ComObject Excel.Application" + vbNewLine +
"$excel.Visible = $false" + vbNewLine +
"$excel.DisplayAlerts = $false" + vbNewLine +
"$wb = $excel.Workbooks.Open($LoadPath, 0, $False, 1, $Password)" + vbNewLine +
"$wb.SaveAs($LoadPath,[Type]::Missing, '')" + vbNewLine +
"$excel.Quit()"
```

$wb.SaveAs의 ''에서 비밀번호를 제거 하여 저장 한다.

필요한 변수
![](/assets/uipath/Excel_RemovePassword_Powershell.png)
