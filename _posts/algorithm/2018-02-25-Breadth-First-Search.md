---
layout: post
title: "너비 우선 탐색"
categories:
  - Algorithm
tags:
  - Algorithm
---

# Chapter 6 너비 우선 탐색

### 2. 그래프(graph)
***트윈 픽스에서 금문교 까지 가는 문제***

어디로 가야 가장 짧은 경로로 갈 수 있는지에 대한 방법을 찾으려면 다음과 같은 절차가 필요함.

1. 문제를 그래프로 모형화 한다.
2. 너비 우선 탐색으로 문제를 푼다.

* 그래프란 연결의 집합을 모형화 한것.
* 그래프는 정점<sup>node</sup>과 간선<sup>edge</sup>으로 이루어짐.
* 정점은 여러 개의 다른 정점과 바로 이어질 수 있다.
* 바로 이어진 정점을 이웃<sup>neighbor</sup> 라고 함.

### 3.너비 우선 탐색(BFS)
* 그래프 알고리즘중 하나
* BFS를 사용하면 두 항목 간의 최단 경로를 찾을 수 있다.
* 체커 게임에서 가장 적은 수로 승리할 수 있는 방법을 계산하는 인공지능
* 맞춤법 검사기(실제 단어에서 가장 적은 개수의 글자를 고쳐서 올바른 단어를 만드는 방법을 찾음)
* 우리 네트워크에서 가장 가까운 의사 선생님을 찾기

BFS는 다음과 같은 종류의 질문에 대답하는데 도움이 됨.
* 정점 A에서 정점 B로 가는 경로가 존재하는가?
* 정점 A에서 정점 B로 가는 최단 경로는 무엇인가?

***망고 농장 주인의 문제***
1. 찾아볼 친구 목록을 만듬.
2. 목록에서 각각의 사람이 망고 판매상인지 판단.
3. 목록에서 누군가를 찾아 볼 떄마다 목록에 그사람의 친구들도 추가.
4. 목록에서 망고 판매상을 찾는 것
* 이런 식으로 망고 판매상에 도달할 때 까지 전체 탐색을 함. 이게 너비 우선 탐색.

***최단 경로 찾기***
1. 이웃인 정점에서 우선 탐색을 함. 
2. 없을 경우 이웃의 이웃들에서 탐색을 함. 
* 이런식으로 탐색 범위를 넓혀 감.
* 다른 방법으로는 탐색 목록에 가까운 이웃 부터 추가 하는 것.

***큐***
* FIFO 먼저 들어간 요소가 먼저 나온다.
* 큐 안의 원소에 임의로 접근할 수 없다.
* 삽입 과 제거가 존재
* 큐를 사용하여 목록에 먼저 추가된 이웃들을 먼저 꺼내서 탐색 가능하다.

***스택***
* LIFO 나중에 들어간 요소가 먼저 나온다.

### 4.그래프의 구현
* 해시테이블을 사용하여 구현 (딕셔너리)
```python
graph = {}
graph['you'] = ['alice', 'bob', 'claire']
```

* 그래프는 여러 개의 정점과 간선이 모여 있는 것.
```python
graph = {}
graph['you'] = ['alice', 'bob', 'claire']
graph['bob'] = ['anuj', 'peggy']
graph['alice'] = ['peggy']
graph['claire'] = ['thom', 'jonny']
graph['anuj'] = []
graph['peggy'] = []
graph['thom'] = []
graph['jonny'] = []
```
* 키/값 쌍들을 넣는 순서는 중요하지 않다.
* 딕셔너리는 순서가 없다. (orderdDict는?)
* 방향 그래프와 무방향 그래프가 있다.
* 관계 에는 방향이 있다. 아누지는 밥의 이웃이지만 밥은 아누지의 이웃이 아니다.
* 무방향 그래프는 두 정점이 서로 이웃이 된다.

### 5. 알고리즘 구현
1. 확인할 사람의 명단을 넣을 큐를 준비한다.
2. 큐에서 한 사람을 꺼낸다.
3. 이 사람이 망고 판매상인지 확인.
4. True: 작업 완료 False: 그 사람의 이웃을 모두 큐에 추가 한다.
5. 1~4 과정 반복
6 만약 큐가 비어 있으면 네트워크에는 망고 판매상이 없다.

* 파이썬에서는 양방향 큐인 `deque`를 사용할 수 있다.

```python
# 1. 큐를 준비 하고 나의 이웃을 추가
search_queue = deque()
search_queue += graph["you"]
# 5. 큐에 요소가 있으면 계속 루프
while search_queue:
    # 2. 큐의 첫 번째 사람을 꺼냄
    person = search_queue.popleft()
    # 3. 망고 판매상인지 확인
    if person_is_seller(person):
        # 4.a 망고 판매상이 맞음
        print(person + 'is a mango seller!')
        return True
    else:
        # 4.b망고 판매상이 아님
        # 모든 이웃을 탐색 목록에 추가
        search_queue += graph[person]
    
# 6
return False
```
***종료조건***
* 망고 판매상을 발견
* 큐가 비게 되는 경우(망고 판매상이 없는 경우)

여기서 앨리스와 밥은 모두 페기라는 친구가 있음.
큐에 페기는 두명이 들어감.
하지만 한번만 확인하면 됨. 두번 확인하면 안됨.
그래서 한번 탐색후 다시 탐색되지 않도록 표시
잘못하면 무한 루프에 빠질 수도 있다.
**이미 탐색한 목록을 가지고 있어야 한다.**
```python
from collections import deque

graph = dict()
graph['you'] = ['alice', 'bob', 'claire']
graph['bob'] = ['anuj', 'peggy']
graph['alice'] = ['peggy']
graph['claire'] = ['thom', 'jonny']
graph['anuj'] = []
graph['peggy'] = []
graph['thom'] = []
graph['jonny'] = []


def search(name):
    search_queue = deque()
    search_queue += graph[name]
    # 이미 확인한 요소를 추적하기 위한 것
    searched = []
    # 큐에 요소가 있으면 계속 루프
    while search_queue:
        # 큐의 첫 번째 사람을 꺼냄
        person = search_queue.popleft()
        # 이전에 확인하지 않은 사람만 확인
        if person not in searched:
            # 망고 판매상인지 확인
            if person_is_seller(person):
                # 망고 판매상이 맞음
                print(person + ' 녀석이 사실 마피아 였던 거임!')
                return True
            else:
                # 망고 판매상이 아님
                # 모든 이웃을 탐색 목록에 추가
                search_queue += graph[person]
                # 이 요소를 확인한 것으로 표시
                searched.append(person)
    return False


def person_is_seller(name):
    # name의 마지막 문자가 m으로 끝나는지 확인
    # m으로 끝나면 망고판매상.
    return name[-1] == 'm'

search('you')

# 실행 결과
#  python code.py
# thom 녀석이 사실 마피아 였던 거임!
```

***실행 시간***
* 전체 네트워크를 탐색하는 것은 모든 정점을 따라서 움직인다는 뜻.
* 실행 시간은 최소 O(간선의 개수)가 된다.
* 탐색할 사람을 저장하는 큐도 있어야 함.
* 큐에 사람을 추가하는데 상수시간 O(1)이 걸림.
* 모든 사람에 이것을 적용하면 O(사람의 수)가 걸림.
* ***너비 우선 탐색은 O(사람의 수 + 간선의 수)가 된다***
* 표기는 O(V+E) V: 정점의 수 E: 간선의 수

### 요약
* 너비 우선 탐색은 A에서 B로 가는 경로가 있는지 알려줌.
* 만약 경로가 존재 한다면 최단 경로도 찾아줌.
* 만약 X까지의 최단 경로를 찾는 문제가 있다면 그 문제를 그래프로 모형화 하고 너비 우선 탐색 적용.
* 방향 그래프는 화살표를 가지며, 화살표 방향으로 관계를 가짐
* 무 방향 그래프는 화살표가 없고, 둘 간의 상호관계를 나타냄.
* 큐는 FIFO
* 스택은 LIFO
* 탐색 목록에 추가된 순서대로 사람을 확인. 그렇기 때문에 탐색 목록은 큐를 사용해야 함. 그렇지 않으면 최단 경로를 구할 수 없음.
* 누군가를 확인하면 두번 확인 하지 않게 해야함. 그렇지 않으면 무한 루프에 빠질수 있음.
 