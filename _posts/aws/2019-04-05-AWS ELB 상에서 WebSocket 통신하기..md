---
layout: post
title: "AWS ELB 상에서 WebSocket 통신하기"
categories:
  - Deploy
tags:
  - Deploy
  - Docker
---

# aws elb를 이용한 django channels 웹소켓 https 적용시 웹소켓 적용 안되는 문제 해결 방법.

let`s encrypt를 사용 하던 중 aws - acm을 elb에 적용하도록 바꾸는 일이 생겼다. 그런데 websocket이 붙질 않는다. 왜그럴까?

aws-acm을 이용하여 elb에 https를 적용 하고 nginx에서 http로 들어온 요청을 https로 리다이렉트 시켰을때 django channels의 웹 소켓의 connection 이 안되는 문제

로드 밸런스의 종류에 따라 해결 방법이 다르다.


### Classic Load Balancer

로드 밸런서의 리스너에 HTTPS 를 SSL로 바꾸어 주어야 한다.
그리고 nginx에서의 HTTP요청에 대한 리다이렉트를 해준다.

HTTP는 TCP로 바꾸면 안된다.

```nginx
if ($http_x_forwarded_proto = "http") {
    return 307 https://$host$request_uri;
}
```

사실 이전에 쓰던 코드는 
```nginx
if ($http_x_forwarded_proto != "https") {
    return 307 https://$host$request_uri;
}
```
인데 TCP 통신까지 모두 리다이렉트 시키는 바람에(추정) 무한 리다이렉션이 걸려 페이지가 뜨지 않음.


### Application Load Balancer

> Application Load Balancer는 WebSockets에 대한 기본 지원을 제공한다. 
> HTTP 및 HTTPS 리스너 모두에서 WebSockets를 사용할 수 있다.

이 말은 Classic Load Balancer에서 HTTPS를 SSL로 바꾼 작업을 하지 않아도 로드밸런서가 알아서 처리 해준다는 말인것 같다.

그래서 단순히 HTTP/HTTPS설정만 하고 nginx는 Classis Load Balancer와 동일하다.

### 로드 밸런서의 헬스체크

로드 밸런서의 상태 검사에서 Ping을 HTTP:8000 /health-check로 수정하고
nginx에 로드밸런서 헬스체크용 포트를 지정한다.

```nginx
server {
    listen 8000;
    server_name ...
    ...

    location /health-check {
        access_log off;
        return 200;
    }}
server {
    listen 80;
    ...
```

더 좋은 방법이 있을것 같다.

## 참고
출처 : [삵(sarc.io)](https://sarc.io/index.php/aws/972-aws-classic-load-balancer-elb-websocket)