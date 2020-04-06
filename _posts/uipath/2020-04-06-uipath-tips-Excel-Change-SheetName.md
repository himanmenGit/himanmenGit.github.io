---
layout: post
title: "PowerShell로 엑셀 시트이름 변경 하기"
categories:
  - UiPath
tags:
  - UiPath
---

PowerShell을 쓰기 위해 `Invoke Power Shell Activity`를 사용한다.

Excel 비밀번호 저장 코드
* $LoadPath - 비밀번호를 해제할 엑셀파일 경로
* $Password - 현재 비밀번호
* $SheetIndex - 변경할 시트 번호
* $OldSheetName - 변경할 시트 이름
* $NewSheetName - 새 시트 이름

변경할 시트를 Index(1부터 시작) 혹은 시트이름으로 찾아서 시트이름을 변경할 수 있다.

```powershell
"$excel = New-Object -ComObject Excel.Application" + vbNewLine +
"$excel.Visible = $false" + vbNewLine +
"$excel.DisplayAlerts = $false" + vbNewLine +
"$wb = $excel.Workbooks.Open($LoadPath, 0, $False, 1, $Password)" + vbNewLine +

"$ws = $wb.worksheets.item($SheetIndex)" + vbNewLine +
또는
"$ws = $wb.worksheets.item($OldSheetName)" + vbNewLine +

"$ws.name = $NewSheetName" + vbNewLine +
"$wb.SaveAs($LoadPath,[Type]::Missing, '')" + vbNewLine +
"$excel.Quit()"
```

필요한 변수
![](/assets/uipath/Excel_ChangeSheetName.png)

* 위 InputArgument에서 SheetIndex의 값이 Int32인것을 유의하고, OldSheetName으로 찾아 변경 하고 싶을 경우 String으로 받아야 한다.
