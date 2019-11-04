---
layout: post
title: "Command line 으로 로봇을 실행 시키기."
categories:
  - UiPath
tags:
  - UiPath
---

* Xaml로 실행
    * 같은 디렉토리 내에 Project.json이 같이 존재 해야함
    * `<UiRobot Path>-f "<Xaml File Path>"` 형태로 사용
    * `UiRobot.exe -f "C:\RPA\Process\Main.xaml"`

![](/assets/uipath/command-line-robot-excute-xaml.png)
    
+ nupkg로 실행
    * `<UiRobot Path>-f "<Xaml File Path>"` 형태로 사용
    * `UiRobot.exe -f "C:\RPA\Process\Main.xaml"`

![](/assets/uipath/command-line-robot-excute-nuget.png)
    
+ 프로세스 이름으로 실행
    * 프로세스 이름에서 Envirionment 이름은 제외한다.
    * `<UiRobot.exe Path> -p <Process Name_Env이름 제외>`
    * `UiRobot.exe -p Main`

![](/assets/uipath/command-line-robot-excute-process.png)
