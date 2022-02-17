---
layout: post
title: "POSTGRESQL DB 주기적으로 백업 및 복구"
categories:
  - Other
tags:
  - Other
---

# 개발서버 <-> 실서버 DB동기화를 위한 POSTGRESQL DB의 주기적인 백업 및 복구

## 문제 발생
개발서버와 실서버의 데이터가 달라서 `CS 대응` 및 `QA`시 사소한 에로 사항이 많이 발생함.

타 부서에서 개발서버와 실서버간의 주기적인 `DB 동기화`를 요청

## 문제 확인 및 원인 파악
`AWS EC2`에서 `RDS`의 개발서버를 실서버의 데이터를 `dump`하여 `resotre`하도록 함

## 해결
`AWS`의 `EC2` 빌드 서버에서 개발서버와 실서버의 DB 동기화 쉘 스크립트를 `Crontab`을 이용하여 복구 하기로 함.

현재 `AWS RDS`로 `Postgresql DB`를 운용 중이며 이를 위해 먼저 EC2에 `pg_dump`와 `pg_resotre`를 사용할 수 있도록 설치

설치

```
sudo apt install postgresql-client-common
```

설치 후 확인

```
pg_dump --version
pg_restore --version
```

Bash 쉘 스크립트 생성

```
vi ~/db-recorvery.sh
```

Bash 쉘 스크립트 작성

```shell
#!/bin/bash
LOG_PATH=/home/ubuntu/postgres/recorvery.log
echo "$(date +%Y-%m-%d) $(date +%H:%M:%S) - 실서버<->개발서버 동기화 시작 ($RUN_STR)" | tee -a $LOG_PATH

# DB 비밀번호는 ~/.pgpass에 작성
# [DB_HOST]:[PORT]:[DB_NAME]:[DB_USER]:[PASSWORD] 입력 (* 입력 시 전체)
DB_NAME=[DB_NAME]
DB_HOST=[DB_HOST]
DB_USER=[DB_USER]
DB_ROLE=[DB_ROLE]
# 덤프시 제외할 테이블 명 (다수 일 경우 각각 생성하여 -T 적용)
# -T example_table1 -T example_table2
EXCLUDE_TABLE_NAME=[EXCLUDE_TABLE_NAME]

BACKUP_DIR=/home/ubuntu/postgres/backup
BACKUP_NAME=$DB_NAME.backup

mkdir -p $BACKUP_DIR

rm -rf $BACKUP_DIR/$BACKUP_NAME

pg_dump -d $DB_NAME -h $DB_HOST -U $DB_USER --role $DB_ROLE -T $EXCLUDE_TABLE_NAME -w -v -F c > $BACKUP_DIR/$BACKUP_NAME

TARGET_DB_NAME=[TARGET_DB_NAME]
TARGET_DB_HOST=[TARGET_DB_HOST]
TARGET_DB_USER=$DB_USER

pg_restore -d $TARGET_DB_NAME -h $TARGET_DB_HOST -U $TARGET_DB_USER -v -c -F c $BACKUP_DIR/$BACKUP_NAME

echo "$(date +%Y-%m-%d) $(date +%H:%M:%S) - 실서버<->개발서버 동기화 끝 ($RUN_STR)" | tee -a $LOG_PATH
```

스크립트에 권한 추가

```
chmod +x db-recorvery.sh
```

스크립트를 작성 하였으면 `.pgpass`작성

```
vi ~/.pgpass
[DB_HOST]:[PORT]:[DB_NAME]:[DB_USER]:[PASSWORD] 입력 (* 입력 시 전체)

ex) *:*:*:pgadmin:password
```

`.pgpass` 권한 변경

```
chmod +x ~/.pgpass
```

주기적으로 동작하기 위한 `Crontab` 등록

```
crontab -e
```

매주 일요일 새벽 4시에 `db-recorvery.sh` 수행 후 `cron.log` 작성

```
0 4 * * 7 /home/ubuntu/db-recorvery.sh >> /home/ubuntu/postgres/cron.log 2>&1
```

`crontab` 등록 확인

```
crontab -l
```

`cron` 서비스 재시작

```
sudo service cron restart
```

## 참고 사이트
[갈색왜성님 블로그](https://browndwarf.tistory.com/12)

[스택 오버플로우](https://stackoverflow.com/questions/21646551/permission-denied-with-bash-sh-to-run-cron)

[kugancity님 블로그](https://kugancity.tistory.com/entry/postgreSQL-pgpass-%ED%8C%8C%EC%9D%BC-%EC%84%A4%EC%A0%95%EB%B2%95)
