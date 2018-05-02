---
layout: post
title: "강사님 수업속도 제어 서비스"
categories:
  - Project
tags:
  - Project
---

# 강사님 속도 조절 서비스

기간 - 2018-03-23 ~ 2018-03-24

인원 - 백엔드 스쿨 수강생 2명 (배포 도우미 - 강사님)

역할 - 로그인, 채팅, 투표, SMS 전송

### 주제 선정 이유

패스트 캠퍼스 웹 프로그래밍 스쿨 강의를 하시는 강사님의 수업 속도가 매우 빨라 수강생들이 힘들어함.

### 주요 기능

Django를 사용하여 페이스북 로그인, 멀티채팅, 투표 기능을 넣고 Bluetooth Speaker를 이용하여 수업 중 종소리 혹은 빠른 속도를 조절하기 위한 효과음을 출력하는 웹 애플리케이션을 제작.

하려고 했으나 이용에 제한이 있어 많은 기능을 수정함. 첫 기획은 투표를 통해 서버에서 보내주는 신호를 내 노트북이 받아 Bluetooth Speaker로 보내주고 싶었으나 그러면 다음 스쿨 기수에서는 사용이 불가. 그래서 Bluetooth Speaker를 강의 중 잠깐 배운 SMS 전송 시스템 coolSMS로 교체 후 작업.

그래서 나온 결과물은 Django와 써보고 싶었던 web-socket 패키지인 channel을 사용하여 실시간 멀티 채팅 구현 그리고 coolsms 을 이용하여 수업 중 강사님께 원하는 문구를 적어(50자 제한) SMS를 전송하는 웹 애플리케이션이다.


AWS를 이용하여 배포하려고 했으나 시간 부족과 channel-red is 설정 문제로 인해 실패
강사님이 개인 서버에 배포를 해주셔서 해커톤 시간에 발표 진행

다행히 반응이 좋아 스쿨(5개 팀 중) 1등.

투표 기능은 만들지 못했음.

프로젝트 종료 때 SMS 서비스는 정해진 문구만 보내도록 하였음. 이후 문구를 적어서 보낼 수 있도록 수정(50자 제한, 쿨타임 30분)

### 느낀 점
		
역시 협업은 어렵다는 것을 가장 먼저 느꼈고 협업을 하려면 많은 대화를 해야 한다는
것을 깨달음.

허술한 기획으로 프로젝트에 큰 지장을 줄 뻔했으나 진행 직전에 기획 수정함. 
기획은 꼼꼼하고 철저하게!

웹 소켓(django-channel) 적용하는 것이 큰 어려움이 없을 것이라는 매우 큰 착각을 함. 상당히 곤욕을 치렀고 Tutorial 문서 최신 버전을 찾는 것에 시간을 많이 허비함. 결국, 시간이 모자라 기능 넣기에 급급. 최신 튜토리얼을 찾아서 만들기는 했지만 정확한 작동 방식과 장고 웹 소켓 기반 지식을 제대로 습득하지 못함.

### 향후 개선 점

나의 AWS로 배포해보기.
Django-channel을 좀 더 깊게 알아보기
사용자 로그인이 페이스북만 되는 것을 Django-User도 가능하도록 수정
지금은 사용자가 채팅방에 로그인 시 채팅창에 검은색 텍스트로 접속 알림이 뜨는데 해당 알림을 좀 더 눈에 잘 띄도록 수정
사용자 아이디의 옆에 프로필 이미지 넣어 보기

### Github

https://github.com/himanmenGit/Hackathon

### View
![Speed1](/assets/project/speed/speed_01.png)
![Speed2](/assets/project/speed/speed_02.png)
![Speed3](/assets/project/speed/speed_03.png)
![Speed4](/assets/project/speed/speed_04.png)
![Speed4](/assets/project/speed/speed_05.png)

### 사용 skills

* Python 3.6
* Django 2.0
* Django channel 2.0.2
* coolsms-python-sdk 2.0.3
* Facebook
* AWS Elastic Beanstalk
* Docker
* Sentry
* Database 
    * Local(sqlite3)
    * Production&Dev(postgresql)
* Git

### 특징 및 기능

* 페이스북 로그인
* 멀티 채팅 (url을 통한 채팅룸 구현)
* 채팅 접속시 채팅창에 접속 알림
* sms 전송 서비스
