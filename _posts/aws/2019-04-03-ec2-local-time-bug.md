---
layout: post
title: "ec2에서 google spread sheet를 사용하기 위해 oauth2client로 인증하다가 에러 발생"
categories:
  - Aws
tags:
  - Aws   
---

### django qcluster 를 돌리던중 google spead sheet의 oauth2client 에서 
```
raise HttpAccessTokenRefreshError(error_msg, status=resp.status)
oauth2client.client.HttpAccessTokenRefreshError: invalid_grant: Invalid JWT: Token must be a short-lived token (60 minutes) and in a
 reasonable timeframe. Check your iat and exp values and use a clock with skew to account for clock differences between systems.
```
라는 에러 발생하여 supervisor가 제대로 동작 하지 않음.

### 에러의 이유
1. ec2의 로컬 타임 동기화가 제대로 되어 있지 않은 경우.
2. JWT 토큰의 새로고침 토큰 만료

### 확인
에러 발생확인후 ec2의 로컬 타임존과 타임을 확인
```
$ cat /etc/timezone
Etc/UTC

$ grep UTC /etc/default/rcS
# assume that the BIOS clock is set to UTC time (recommended)
UTC=yes

$ date
Wed Apr  3 02:14:01 UTC 2019 <- 요기서 UTC기준 +09:00 이 아니라 좀 이상한 시각이 나옴.
```

### 수정
타임을 재 조정
```
sudo ntpdate ntp.ubuntu.com
```

그리고 supervisor를 재 실행
```
sudo service supervisor stop
sudo service supervisor start
```
supervisor의 service를 재실행 한 이유는 sueprvisor.sock이 없다고 나와서 완전 재실행 함.
이후 문제 해결.
