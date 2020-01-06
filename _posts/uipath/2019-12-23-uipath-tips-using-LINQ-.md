---
layout: post
title: "UiPath LINQ 사용방법 및 팁"
categories:
  - UiPath
tags:
  - UiPath
---

***이 문서는 지속적으로 업데이트 될 예정 입니다.***

### Datatable

* Sample DataTable

| Age | Sex |
|-----|-----|
| 32  | m   |
| 27  | f   |
| 35  | m   |
| 35  | f   |
| 26  | m   |

* 기본 Select

```c#
selectedRows<Row[]> = dataTable.Select("Age >= 30 AND Sex = 'm'")
forEach row in selectedRows
    Log("Age:" + row(age) + " Sex: " + row(sex)

> Age : 32 Sex : m
> Age : 35 Sex : m

copiedDt<Datatable> = dataTable.Select("Age >= 30 AND Sex = 'm'").CopyToDatatable
forEachRow row in copiedDt
    Log("Age:" + row(age) + " Sex: " + row(sex)

> Age : 32 Sex : m
> Age : 35 Sex : m
```

* Select 를 이용한 Rows 합

```c#
int64 TotalAge = dataTable.AsEnumerable().Sum(Function(row) Convert.ToInt64(row("Age")))
Log(TotalAge)

> 155
```
    

* Group by와 Sum을 같이 사용

```c#
GroupSum<String[]> = dataTable.AsEnumerable.
                        GroupBy(Function(row) row("Sex").ToString).
                            Select(
                                Function(그룹) 
                                    String.Format("{0} : {1} Count - {2}", 
                                        그룹.Sum(Function(row) Convert.ToInt64(row("Age"))), 
                                        그룹.Key, 
                                        그룹.Count()
                                    )
                            ).ToArry
                            
forEach GroupSum in item
    Log(item)

> 93 : m Count - 3
> 62 : f Count - 2
```

* 지정한 Column의 Row들을 Array로 가져오기

```c#
array_row<String[]> = dataTable.AsEnumerable.Select(Function(row) row("Sex").ToString).ToArray

forEach item in array_row
    Log(item)

> m
> f
> m
> f
> m
```

### Collection

* Sampel Array

```c#spq 
names = {"Marius", "Daniel" "Arial", "Asta"}
```

* Array<String>에 Select 문법 사용

```c#
filteredNames<String[]> = (From name In names.AsEnumerable Where name.StartsWith("A") Select name).ToArray

forEach name in filteredNames
    Log(name)
    
> Arial, Asta
```