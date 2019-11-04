---
layout: post
title: "데이터 테이블의 1개의 컬럼 데이터들을 배열로 변환하기."
categories:
  - UiPath
tags:
  - UiPath
---

```csharp
out_arr_str_data = (From row in in_dt_data.AsEnumerable() Select Convert.Tostring(row(in_str_columnName))).ToArray
```

![](/assets/uipath/datatable-column-data-to-array.png)