---
layout: post
title: "APScheduler Missed! 발생시 대처 방안"
categories:
  - Other
tags:
  - Other
---

# APScheduler 사용시 Missed! 발생 시 대처 방안

## 문제 발생
사내에서 특정한 주기로 `Celery Task`를 수행하기 위한 스케쥴러로 `APScheduler`을 사용하는 중이었다.

그런데 어느날 새로운 기능 업데이트 후 `Celery Task`가 동작하지 않아 문제가 발생 하였다.

## 문제 확인 및 원인 파악
`Celery Task`가 수행하고 나서 처리 되어아 햘 내용들이 반영 되지 않은것을 확인.

새로운 기능 업데이트 후 발생하였다고 생각하여 로직을 다시 체크 -> 별 이상 없는것으로 확인.

워커에 접속하여 해당 시간에 `Celery Task` 수행 여부 확인 `grep "2022-01-23 00:00" log.log` -> 수행로그 없음.

관리자 페이지에 접속하여 `APScheduler Job Execution` 확인 -> Missed! 확인
![](/assets/other/apscheduler_missed.png)
특이 사항은 `duration`이 1.01초 이상이면 무조건 `Missed!`가 발생하는 것을 확인함.

`Missed!`는 서버의 성능이 낮거나 동시에 수행되는 프로세스가 많은경우 스케쥴러가 해당 스케쥴을 실행하지 못하고 그냥 넘어 가는 경우가 있다고 함.

우리는 동일한 시간에 다수의 스케쥴이 동시에 실행되는 것들이 있었음.

그리고 이 외에 Missed!를 찾아보니 예전 스케쥴들에도 같은 상황이 발생 하던것을 확인 함.

## 해결
서버의 성능을 올리기 전에 `APScheduler` 문서를 확인함 -> `misfire_grace_time`라는 것을 발견.

공식문서와 구글링을 통해 해당 설정이 스케쥴의 지연시간에 관여한다는 것을 추측함. 

소스를 조금만 들여다 봄.
![](/assets/other/misfire_grace_time_code.png)
`misfire_grace_time`가 없으면 1초를 고정으로 설정 해주는것을 확인. 1.01초 이상이면 실패 하던것이 생각남.

`misfire_grace_time`을 초단위로 주어서 스케쥴이 지연되어도 해당 시간동안에는 `Missed!`가 안나고 수행될 수 있을것 같음.

공식 문서를 확인하니 `misfire_grace_time=None`을 줄 경우 수행 될 때까지 기다린다고 함. 

`None`으로 지정함.
```python
    sched.add_job(
        job,
        trigger=CronTrigger(day="*", hour="0", minute="0"),
        id="job",
        misfire_grace_time=None,
        replace_existing=True,
    )
```

![](/assets/other/apscheduler_excuted.png)
성공!
