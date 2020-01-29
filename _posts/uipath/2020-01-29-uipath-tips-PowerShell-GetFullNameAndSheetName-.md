---
layout: post
title: "PowerShell을 이용한 활성화된 엑셀의 경로와 시트 이름 가져오기"
categories:
  - UiPath
tags:
  - UiPath
---

Excel Application Scope로 연 엑셀이 아닌 이미 엑셀 응용프로그램이 로드된 엑셀의 정보를 가져 올때 사용하는 
PowerShell 스크립트.

```
"$app=[Runtime.InteropServices.Marshal]::GetActiveObject('Excel.Application').Workbooks.Application" + vbNewLine +
"$FilePath=$app.ActiveWorkbook.FullName" + vbNewLine +
"$SheetName=$app.ActiveWorkbook.ActiveSheet.Name"
```

FilePath는 전체 경로이고 ActiveSheetName.Name은 현재 열려 있는 엑셀의 활성화 된 엑셀 시트 이름이다.


![](/assets/uipath/powershell_get_active_excel_info.png)
![](/assets/uipath/powershell_get_active_excel_info_result.png)
