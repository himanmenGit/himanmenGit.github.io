# Authentication

인증은 들어오는 요청을 사용자 또는 서명된 토큰과 같은 식별 자격 증명 세트와 연관 시키는 메커니즘. 권한 및 제한 정책은 이러한 자격증명을 사용하여 요청을 허용 해야하는지 결정 할 수 있다.

`REST framework`는 여러가지 인증 스키마를 제공하며 사용자 정의 스키마를 구현 할 수도 있다.
인증은 항상 뷰의 맨처음 퍼미션과 스로틀링 검사를 하기 전에 이루어 진다.
`request.user` 속성은 일반적으로 `contrib.auth` 클래스 인스턴스로 설정된다.
`request.auth` 등록정보는 추가 인증 정보를 나타내는데 사용된다. 예를 들어서 요청이 서명된 인증토큰을 나타내는 데 사용될수 있다. 이것은 `BasicAuthentication`, `TokenAuthentication`, `SessionAuthentication`, `RemoteUserAuthentication` 의 인증 방식에 따른 정보들이 `request.auth`에 들어 있다는 것을 말한다.