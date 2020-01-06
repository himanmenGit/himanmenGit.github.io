---
layout: post
title: "PowerShell을 이용한 압축/압축풀기"
categories:
  - UiPath
tags:
  - UiPath
---

프로젝트 진행시 폴더를 압축 해야 할 경우가 생긴다. 
.Net 으로 압축 기능을 만들어 사용할 수 없을 경우에 Powershell을 사용하여 압축 및 압축풀기를 할 수 있다.

### 압축 하기

* Invoke Power Shell 액티비티를 사용한다.
![](/assets/uipath/invoke_powershell_zip_activity.png)

* Invoke Power Shell 액티비티의 속성. IsScript에 체크 한 다음 PowerShellVariables에 변수를 등록한다.
![](/assets/uipath/invoke_powershell_zip_activity_propertry.png)
![](/assets/uipath/invoke_powershell_zip_activity_variable_arg.png)

* 그리고 코드를 작성 한다.
```
"set-content $zip ([byte[]] @(80, 75, 5, 6 + (, 0 * 18))) -encoding byte" + vbNewLine +
"$shellFolder = (New-Object -Com Shell.Application).NameSpace($folder)" + vbNewLine + 
"$zipFolder = (New-Object -Com Shell.Application).NameSpace($zip)" + vbNewLine + 
"$zipFolder.CopyHere($shellFolder.Items())"
```
![](/assets/uipath/invoke_powershell_zip_activity_script.png)

해당 기능으로 압축을 할 때 압축이 되기 전에 프로세스가 종료 되면 압축이 실패 한다.
그러므로 해당 스크립트를 실행 하고 나서 Delay를 주거나 해당 파일이 제대로 생성되 었는지 판단하여 기다리게 하는 코드가 필요 하다.

ChangeType이나 NotifyFilters가 시스템 마다 다르게 동작 하는 경우도 있기 때문에 옵션을 잘 조절 해야 한다.
* 본인 PC - ChangeType:All, NotifyFilters:FileName,LastWrite 의경우 TMP파일을 남기며 파일이 압축된다. 압축 완료후 TMP파일을 해당 디렉토리에서 삭제하는 로직을 추가함.
```python
for file in Directory.GetFiles(in_str_압축결과파일경로, "*.TMP")
    delete file
```
![](/assets/uipath/invoke_powershell_file_write_complete.png)
* 프로젝트 PC - ChangeType:Changed, NotifyFilters:LastWrite 의 경우 압축이 완료 되면 정상적으로 동작한다.
![](/assets/uipath/invoke_powershell_file_write_complete2.png)

### 압축 풀기

* Invoke Power Shell 액티비티를 사용한다.
![](/assets/uipath/invoke_powershell_unzip_activity.png)

* Invoke Power Shell 액티비티의 속성. IsScript에 체크 한 다음 PowerShellVariables에 변수를 등록한다.
![](/assets/uipath/invoke_powershell_zip_activity_propertry.png)
![](/assets/uipath/invoke_powershell_unzip_activity_variable_arg.png)

* 그리고 코드를 작성 한다.
```
"$shell = New-Object -ComObject Shell.Application" + vbNewLine + 
"$zip = $shell.NameSpace($file)" + vbNewLine + 
"$dest = $shell.NameSpace($folder)" + vbNewLine + 
"$dest.CopyHere($zip.Items())"
```
![](/assets/uipath/invoke_powershell_unzip_activity_script.png)