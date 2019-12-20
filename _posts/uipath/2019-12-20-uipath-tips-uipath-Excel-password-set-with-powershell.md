---
layout: post
title: "PowerShell로 엑셀 비밀번호 설정하기"
categories:
  - UiPath
tags:
  - UiPath
---

UiPath 기본 라이브러리에는 엑셀 파일에 비밀번호를 지정하는 기능은 없다.
이를 PowerShell을 이용하여 엑셀에 비밀번호를 지정해보자.

PowerShell을 쓰기 위해 `Invoke Power Shell Activity`를 사용한다.

Excel 비밀번호 저장 코드
* $LoadPath - 비밀번호를 설정할 엑셀파일 경로
* $SavePath - 비밀번호가 설정된 엑셀파일이 복사될 경로
* $Password - 비밀번호
* 해당 파일에 바로 비밀번호를 걸경우 경로를 같이 사용 한다.

```
$excel = New-Object -ComObject Excel.Application
$wb = $excel.Workbooks.Open($LoadPath)
$wb.SaveAs($SavePath,[Type]::Missing, $Password)
$excel.Quit()
```

코드를 실행 한 후 파일들
![](/assets/uipath/Excel_Files.png)

Temp_enc.xlsx 파일을 실행하면
![](/assets/uipath/Excel_PasswordFile.png)

IsScript에 체크 하고 PowerShell에서 사용할 변수들에 데이터를 할당 함.
![](/assets/uipath/Excel_SetPassword_Powershell.png)

삽입한 코드
![](/assets/uipath/Excel_SetPassword_Powershell_Code.png)
