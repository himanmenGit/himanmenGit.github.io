---
layout: post
title: "Chapter 02. 리팩터링 원칙 (2.5~2.6)"
categories:
  - Book
tags:
  - Book
---

## 2.5 리팩터링 시 고려할 문제

### 새 기능 개발 속도 저하
- **리팩터링의 궁극적인 목적은 개발 속도를 높여서, 더 적은 노력으로 더 많은 가치를 장출하는 것이다.**
    - 모든것은 상황에 맞게 조율.
- 리팩터링을 할지 말지 판단하는 능력은 수년에 걸친 경험을 통해 서서히 형성 됨.
    - 리팩터링을 더 자주 하도록 노력 해야 한다.
- 리팩터링은 클린코드나 바람직한 엔지니어의 습관 같은 도덕적인 이유나 코드를 이쁘게 꾸미는 것은 아닌 오로지 경제적인 (궁극적인 목적) 이유로 하는 것.

### 코드 소유권

- 코도의 소유권이 나뉘어져 있으면 리팩터링에 방해가 된다.
- 할수 없는 것은 아니나 제약이 따른다.
    - 함수 이름 바꾸기를 적용 시 기존 함수는 그대로 유지 한 채 함수 본문에서 새 함수를 호출 하도록 수정.
    - 복잡해 진다.
- 코드의 소유권을 팀에 두는 것.
    - 팀원이라면 누구나 팀이 소유한 코드를 수정할 수 있게 한다.

### 브랜치

- 각 팀원마다 브랜치를 맡아서 작업 하다가 마스터에 통합하여 다른 팀원과 통합하는 방식이 있다. (우리)
    - 작업이 완전히 끝나지 않은 코드가 마스터에 섞이지 않고 명확하게 버전을 나눌 수 있으며 기능에 문제가 생겼을 경우 이전 상태로 쉽게 되돌릴 수 있다.
    - 작업 기간이 길어 질 수록 마스터에 통합하기 어려워 짐.
- 기능별 브랜치의 통합 주기를 매우 짧게 하는게 좋다.
    - 지속적 통합(Continuous Integration-CI)라 한다.
    - 또는 트렁크 기반 개발 (Trunk-Based-Development-TBD)라고도 한다.
- CI를 하면 다른 브랜치들과의 차이가 크게 벌어지지 않아 머지의 복잡도가 줄어 든다.
- CI를 유지하는것은 좀 힘들다.
    - 마스터를 건강하게 유지.
    - 큰 기능을 잘게 쪼개기
    - 각 기능을 끌 수 있는 토글을 적용 하여 완료되지 않은 기능에 때문에 시스템에 문제가 생기지 도록 해야 한다.
- CI와 리팩터링은 궁합이 좋다.
- 익스트림 프로그래밍 (eXtreme Programming - XP)
    - CI + 리팩터링
- CI를 완벽하게 적용하지 못하더라도 통합 주기는 짧게 잡는게 좋다.

### 테스팅

- 리팩터링하기 위해서는 대부분의 경우 테스트 코드를 마련해야 한다.
- 테스트가 실패 한다면 최신 버전에서 무엇이 달라 졌는데 빠르게 확인 할 수 있다.
- 리팩터링 과정에서 버그가 발생 할 것이라는 불안감을 많이 해소 할 수 있다.
- 테스트는 다른 방식으로도 해결 할 수 있다.
    - 자동 리팩터링 기능을 지원하는 환경을 사용한다면 굳이 테스트 하지 않아도 오류가 생기지 않는다고 생각 할 수 있다.
    - 그럼에도 불구 하고 테스트 코드를 갖추는 것이 훨씬 좋다.
- 안전하다고 검증된 몇가지 리팩터링 기법만 조합하여 사용하자는 흐름이 등장 하기도 했다.
- 테스트코드는 자연스럽게 CI와도 밀접하게 연관 된다.
- CI에 통합된 테스트는 XP(CI+리팩터링)의 권장사항이자 지속적 배포(Continous Delivery-CD)의 핵심.

### 레거시 코드

- 레거시코드는 대부분 복잡하고 다른이의 코드다.
- 레거시코드를 파악 할 때 리팩터링이 매우 도움이 된다.
- 레거시코드의 리팩터링을 위해서는 당연히 테스트 코드를 준비 하는 것.
- 쉽게 해결 할 방법은 없다.
    - 프로그램에서 테스트를 추가할 틈새를 찾아서 시스템을 테스트 해야 한다.
    - 틈새를 만들기 위해 리팩터링을 해야한다.
- 처음부터 테스트 코드를 작성해야 하는 이유이다.

### 데이터 베이스

- 진화형 데이터베이스 설계와 데이터 베이스 리팩터링 기법
    - 데이터 마이그레이션 스크립트를 작성.
    - 접근 코드와 데이터베이스 스키마에 대한 구조적 변경을 스크립트로 처리하게끔 통합.
- 프로덕션 환경에서 여러 단계로 나눠서 릴리즈 하는 것이 대체로 좋다.
- 필드 이름을 바꿀 때
    - 첫 커밋에서는 필드를 추가만 하고 사용하지 않음
    - 기존 필드와 새 필드를 동시에 업데이트 하도록 설정
    - 클라이언트들을 새 필드를 사용하는 버전으로 조금씩 교체
    - 버그 수정 및 교체작업이 모두 끝나면 이전 필드는 삭제
    - 병렬수정(팽창-수축)의 일반적인 예

## 2.6 리팩터링, 아키텍처, 애그니(YAGNI)

- 코딩 전에 아키텍처를 확정지으려 할 떄의 대표적인 문제는 소프트웨어 요구사항을 사전에 모두 파악해야 하는 것.
    - 실현 할 수 없는 목표일 때가 많다.
- 유연성 메커니즘을 소프트웨어에 심어 두는 것.
    - 함수에 다양한 예상 시나리오에 대응 할 수 있는 매개변수들을 추가 한다.
    - 매개변수들을 추가하다 보면 당장의 쓰임새 보다 함수가 복잡 해 진다.
    - 새로운 매개변수를 추가하기 여려워 질 수도 있다.
    - 유연성 메커니즘이 오히려 변화에 대응하는 능력을 떨어뜨릴 때가 대부분.
- 리팩터링을 활용하면 현재 파악한 요구사항만을 해결하는 소프트웨어를 구축한다.
    - 진행하면서 요구사항을 더 잘 파악하게 되면 리팩터링을 진행한다.
    - 소프트웨어의 복잡도에 지장을 주지 않을 정도의 메커니즘은 마음껏 추가 한다.
    - 복잡도를 높일 수 이는 유연성 메커니즘은 검증을 거친 후 추가 한다.
- 이런식으로 설계하는 방식을 간결한 설계, 점진적 설계, YAGNI(you aren't going no teed it)등으로 부른다.
- 추후 문제를 더 깊이 이해하게 됐을 때 처리하는 것이 더 낫다고 생각 한다.
- 진화형 아키텍처 원칙이 발전하는 계기가 됨.
    - 아키텍처 관련 결정을 시간을 두고 반복해 내릴수 있다는 장점을 활용하는 패턴과 실천법
