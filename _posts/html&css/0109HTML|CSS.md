#atom
###tips
- auto indent
>atom->setting->keybindings->yourkeymaps
>>
`'atom-text-editor':`
` 'ctrl-i' : 'editor:auto-indent'`
---
#html
### table
-  table
><pre>`<table></table>`</pre>
- 제목
><pre>`<caption></caption>`</pre>
- 행
><pre>`<tr></tr>`</pre>
- 테이블 헤더
><pre>`<th></th>`</pre>
- 테이블 데이터
><pre>`<td></td>`</pre>
- 행 병합 [colspan]
><pre>`<td rowspan="3"></td>`</pre>
- 열 병합 [rowspan]
><pre>`<td colspan="3"></td>`</pre>
- 행의 구조화 [thead][tbody]
>
<pre>`
<thead></rhead>  열 제목 한번만 사용 가능,
<tbody></tbody> 
<tfoot></tfoot> 제일 아래 쓰는 용도로, 한번만 사용 가능,
 `</pre>
 
 ---
 
### form

 - method
> 데이터를 전달하는 방법은 GET, POST 두가지 이다.
기본으로 GET 방식으로 전달 된다
POST 방식으로 전달시 데이터는 주소 표시줄에 노출 되지 않는다.
<pre>`<form action='' method='GET/POST'>`</pre>
- action
>폼에서 데이터를 전달하는 URL
<pre>`<form action='join' method=''>`</pre>
- tags
>Input 태그의 종류
<pre>`
<input type="text" name="username">
<input type="password" name="password">
<input type="radio" name="radio">
<input type="checkbox" name="checkbox">
<input type="button" value="버튼">
<input type="file" name="file">
<input type="submit" value="전송">
<input type="reset" value="리셋">
<input type="hidden" name="hidden" value="hiddenValue">
`</pre>

- input 속성
>- disables 사용 막음 submit 전송 불가
>- readolny 사용 막음 submit 전송 가능 
>- required 사용자 입력이 반드시 있어야함. 값이 없을 경우 submit되지 않음
>- size 해당 Input 크기
>- maxlength 글자 총 길이

- textarea
>장문의 글을 적을때 사용
col, row로 크기 조절가능
<textarea id="textarea1" rows="8" cols="80" placeholder="자기소개"></textarea>
- Label
>label 안에 input 태그와 밖의 차이
<div>
이름 선택하여 체크박스 선택 가능
      <label>ID <input type="text"></label>
      <label>Check<input type="checkbox"></label>
    </div>
    <div>
연결 하지 않았을 경우 for 속성으로 id 와 매칭시켜 연결 가능
      <label for="text1">ID</label><input type="text" id="text1">
      <label for="checkbox1">Check</label><input type="checkbox" id="checkbox1">
</div>

- select
>기본 사용법
<select name="" >
      <option value="">Item1</option>
      <option value="">Item2</option>
      <option value="">Item3</option>
      <option value="">Item4</option>
    </select>
optgroup 묶음
<select name="" id="">
      <optgroup label="Fruits">
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </optgroup>
      <optgroup label="Colors">
        <option value="red">Red</option>
        <option value="blue">Blue</option>
        <option value="green">Green</option>
      </optgroup>
</select>

- fieldset, legend
>틀을 만들어 준다
<fieldset>
	<legend>Login</legend>
      <label for="">username : <input type="text"></label>
      <label for="">password : <input type="text"></label>
</fieldset>

---

### Class, ID
- class 와 id의 차이
>id는 같은페이지에서 단 한번만 선언 가능 해당 태그의 유일함을 표현
class는 여러개의 같은 클래스를 사용 가능