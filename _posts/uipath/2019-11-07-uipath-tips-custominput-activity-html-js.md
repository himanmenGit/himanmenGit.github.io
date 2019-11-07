---
layout: post
title: "Html + JS로 CustomInput Activity 사용하기."
categories:
  - UiPath
tags:
  - UiPath
---

+ Custom Input Activity를 아래 html 코드가 저장 되어 있는 template.html을 URI로 호출 하면 된다.
![](/assets/uipath/customInput-activity.png)

```html
<!doctype html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
First Name:<br>
<input type="text" id="First_Name"><br>
Last Name:<br>
<input type="text" id="Last_Name"><br>
Age:<br>
<input type="text" id="Age"><br>

<button onclick="SubmitValues()">Submit</button>

<script type="text/javascript">
    function SubmitValues() {
        var First_Name = document.getElementById("First_Name").value;
        var Last_Name = document.getElementById("Last_Name").value;
        var Age = document.getElementById("Age").value;
        window.external.setResult(First_Name + "," + Last_Name + "," + Age);
        return true;
    }
</script>
</body>
</html>
```

* 브라우저
![](/assets/uipath/customInput-activity-browser.png)

* 결과 메세지 박스
![](/assets/uipath/customInput-activity-submit-box.png)