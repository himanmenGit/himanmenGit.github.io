# Facebook Login

### Django Facebook Login
1. 사이트에서 '페이스북 로그인' 버튼 클릭
2. 페이스북 사이트로 이동해서 사용자 인증 및 권한 인가 완료
3. 토큰이 사이트에 GET매개변수로 전달됨 (페이스북 -> 사이트서버로 전달)
4. 사이트의 View에서 받은 토큰을 사용해서 페이스북과 인증 과정 거침 (사용자 개입 없음)
5. 인증이 완료되면 사이트에서 회원가입 및 로그인 유지를 위한 처리

* 페이스북의 로그인 호출하기전 관련 SDK로드 및 버전 설정
```html
<script type="text/javascript">
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '556722268030664',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.12'
    });

    FB.AppEvents.logPageView();

  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));
</script>
```

페이스북에 로그인 할 때는 첫 번째 단계로 사용자가 Facebook 로그인을 사용하여 이미 앱에 로그인 했는지 확인한다. `FB.getLoginStatus`를 호출하여 이 프로세스를 시작한다. 이 함수는 `Facbook` 호출을 요청하여 로그인 상태를 가져오고 결과를 통해 콜백 함수를 호출한다.
```html
<button id="btn-facebook">페이스북 로그인</button>

$('#btn-facebook').click(function() {
      facebookLogin();
    })
    
function facebookLogin() {
      FB.getLoginStatus(function(response) {
        if (response.status != 'connected') {
          FB.login(function(response) {
            console.log(response);
          });
        } else {
          console.log(response);
        }
      });
    }
```
`facebookLogin()`으로 감싼 이유눈 로그인 상태 체크 함수는 페이스북 SDK로드가 끝나고 실행 되어야 한다. 함수로 감싼다음 해당 함수를 특정 이벤트에 호출 하는 방법도 좋은 방법이 될 것이다.
브라우저 콘솔에서 `facebookLogin()`을 호출 해보면 페이스북에서 어떤 데이터를 돌려주는 것을 볼 수 있다.

그리고 돌아온 데이터중 `status`가 `connected`가 아닐 경우 는 명시적으로 페이스북 로그인을 호출 해주어야 한다. 
이제 버튼을 눌려보면 페이스북 로그인 대화상자가 뜰 것이다 (안뜬다면 크롬 시크릿 모드로 해보면 된다.) 그러면 `status`가 `connected`로 돌아오는것을 볼 수 있다.

그러면 클라이언트에서는`accessToken`, `userID` 를 가지고 있게 된다. 이 정보들을 서버로 보내 `accessToken`을 통해 페이스북에 인증하여 유저정보를 가져와 해당 유저가 유효한지 검사한 후 유저를 만들거나 가져와서 유저를 특정화 시킨다음 유저의 토큰을 다시 클라이언트로 보내 주면 된다.

### Token Login
1. 클라이언트가 `username`, `password`를 이용해 토큰을 요청
2. 서버는 전달받은 자격 인증을 이용해서 유저를 인증, 성공하면 `token`을 돌려줌
3. 클라이언트는 받은 `Token`을 이후 요청마다 `HTTP Header`에 담아 보냄

### 클라이언트의 Facebook Login with Token
1. 클라이언트가 Facebook `access_token`을 이용해 `Token`을 요청
2. 서버는 전달받은 `access_token`을 이용해서 유저를 인증, 
	페이스북 토큰의 검증에 성공했고 해당하는 유저가 있으면 `Token`을 돌려줌
	페이스북 토큰의 검증에 성공했으나 해당하는 유저가 없으면 유저를 생성 후 `Token`을 돌려줌
	페이스북 토큰의 검증에 실패했으면 오류 발생시킴
3. 클라이언트는 받은 `Token`을 이후 요청마다 `HTTP Header`에 담아 보냄

***필요 사항***
1. 서버측의 페이스북 `access_token`을 사용한 `authenticate Backend` 구현
2. `AuthTokenForFacebookAccessTokenView()`
	-> `/api/members/facebook-auth-token/` `url`로 연결
3. 클라이언트에서 `function getAuthTokenForFacebook()` 구현
4. 이후 해당 엑세스 토큰을 가지고 페이스북 정보를 받아와 유저를 생성시켜서 해당 유저와 토큰을 돌려주는 `View`작성. 해당 `View`에는 페이스북 엑세스 토큰을 가지고 직렬화시킨 유저를 반환하는 로직 작성. `AccessTkenSerializer()`
해당 로직은 유저 인증에 대한 `APIFacebookBackends`로 인증하는 `authenticate`와 해당 유저를 