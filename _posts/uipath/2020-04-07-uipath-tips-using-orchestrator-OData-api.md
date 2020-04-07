---
layout: post
title: "Orchestrator OData API Filter 사용하기"
categories:
  - UiPath
tags:
  - UiPath
---

Orchestrator의 정보를 얻기 위해 API에서 Filter를 사용하는 방법에 대해 알아 보자.

Orchestrator API 구현은 OData 프로토콜을 기반으로합니다. OData (Open Data Protocol)는 ISO / IEC 승인 OASIS 표준으로, RESTful API를 구축하고 사용하기위한 모범 사례를 정의합니다.

[출처 - UiPath Doc](https://docs.uipath.com/orchestrator/reference/about-odata-and-references)

* OData 필터 연산자 $filter=Value1 연산자 Value2

| 연산자 	|       설명       	|                    예시                   	|
|:------:	|:----------------:	|:-----------------------------------------:	|
|   eq   	|       같다       	|             State eq 'Running'            	|
|   ne   	|     같지 않다    	|             State ne 'Running'            	|
|   gt   	|     보다 크다    	| LastLoginTime gt 2020-04-07T04:18:04.000Z 	|
|   ge   	| 보다 크거나 같다 	|        LastLoginTime ge 2020-04-07Z       	|
|   lt   	|     보다 작다    	|               RobotId lt 100              	|
|   le   	| 보다 작거나 같아 	|               UserId le 100               	|
|   and  	|       또는       	|      RobotId gt 0 and RobotId le 100      	|
|   or   	|       혹은       	|      RobotId le 50 or RobotId ge 100      	|
|   add  	|      더하기      	|             Price add 5 gt 10             	|
|   sub  	|       빼기       	|              Price sub 5 lt 5             	|
|   mul  	|      곱하기      	|              Price mul 5 eq 5             	|
|   div  	|      나누기      	|              Price div 2 eq 5             	|
|   mod  	|      나머지      	|              Price mod 2 eq 0             	|
|   ()   	|     Grouping     	|            (Price sub 5) gt 10            	|

* OData 필터 함수 $filter=함수명(Value1, Value2)

|   함수명   	|              예시              	|
|:----------:	|:------------------------------:	|
|  contains  	|       contains(Name, 'D')      	|
|  endswith  	|       endswith(Name, 'n')      	|
| startswith 	|      startswith(Name, 's')     	|
|   length   	|        length(Name) ge 7       	|
|   indexof  	|     indexof(Name, 'E') eq 1    	|
|  substring 	| substring(Name, 1) eq 'ESKTOP' 	|
|    trim    	|     trim(Name) eq 'DESKTOP'    	|
|    year    	|   year(LastLoginTime) eq 2020  	|
|    month   	|   month(LastLoginTime) eq 05   	|
|     day    	|    day(LastLoginTime) gt 01    	|


[출처1 - UiPath 포럼](https://forum.uipath.com/t/orchestrator-api-query-functions/185719)

[출처2 - OData CheatSheet](https://help.nintex.com/en-us/insight/OData/HE_CON_ODATAQueryCheatSheet.htm)