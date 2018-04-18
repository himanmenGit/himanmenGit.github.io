# django rest framework Testing

### APIRequestFactory
개발자 차원에서의 테스트. 단위 테스트
뷰를 함수단위로 테스트를 하고 싶을 때 사용 한다.
장고는 웹 애플리케이션이 켜져 있고 사용자가 접속하기를 기다렸다가 요청에 대한 응답을 돌려 준다.
그래서 웹 서버만 켜져 있고 장고는 해당 요청에 대한 아웃풋만 주는 것.
웹 애플리케이션 이라는 것은 어떤 인풋이 들어왔을때 아웃풋을보내는 함수에 불과하다.
`APIRequestFactory`는 뷰를 하나의 함수로 놓고 함수에대해서 테스트를 할수 있게 한다.
API단위 자체를 함수로 구분 하는 것

`request`객체를 만들어 `view(request)`에 던지면 `response` 가 오는 형태인데 이 `view`는 함수의 형태로 `request`를 받게 작성 되어 있기 때문에 해당 함수를 테스트 할 수 있게 된다.

그래서 하나하나의 단위로 테스트 하고 싶을 경우 `APIRequestFactory`를 사용한다.

### APIClient
사용자 차원에서의 테스트. 기능 테스트
실제로 브라우저에 요청 하는것 과 동일 하다. 가상의 브라우저를 만드는 방식이라고 생각하면 된다.

사용자가 접근하여 요청하는것을 가정 한다고 하면 `APIClient`를 쓰는것이 좋다.
우리가 만든 모든 `API View`는 모두다 기능 테스트가 된다. 왜냐하면 사용자가 해당 API뷰에 요청을 보내기 때문이다.
만약 유효성 검증이 특이한 형태로 되어 있을 경우 단위 테스트로 만드는 것이 좋다. 모든 것을 기능 테스트로 할 경우 시간이 많이 걸리기 때문이다. 기능 테스트는 요청이 왔을 때 잘못된 요청/제대로 된 요청 두가지의 경우로 나누고 사용자가 할 수 있는 잘못된 입력을 넣어 보는 것.
단위 테스트는 개발자가 만들어 놓은 모델, 시리얼라이저가 할 수 있는 에러를 발생 시켜 보는것 이다.

하지만 테스트로 모든 것을 다하는 것은 무리다. 그렇기 때문에 일반적으로 API뷰를 만들면서 개발자 본인이 막고 싶은 것에 대한것만 하는것이 좋다.

### TestCase
`django rest frameowrk testing`에서는 모든 `TestCase`앞에 `API`가 붙는다. 특별한 내용이 아니면 `APITestCase` 만 사용 하면 된다. 해당 모듈을 사용할 경우 `client`에 접근 할 때 따로 만들지 않고 `self.client`로 접근하면 된다.
```
self.client.get(...
self.client.post(...
```

### Testing
```
import random

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase

from some.apis import SomeListView
from some.models import Some


class SomeListTest(APITestCase):
    PATH = '/api/some/'
    VIEW_NAME = 'apis:some:some-list'
    VIEW = SomeListView
    PAGINATION = 5

    def test_reverse(self):
        # some-list에 해당하는 URL reverse했을 때,
        # 우리가 기대하는 URL path와 일치하는지 테스트
        #   -> Django url reverse
        self.assertEqual(reverse(self.VIEW_NAME), self.PATH)

    def test_resolve(self):
        # some-list에 해당하는 URL path를 resolve했을 때,
        # 1. ResolverMatch obj의 func가 우리가 기대하는 View function과 같은지
        # 2. ResolverMatch obj의 view_name이 우리가 기대하는 URL name과 같은지
        #   테스트
        #   -> Django url resolve, Django resolver match
        resolve_url = resolve(self.PATH)
        self.assertEqual(resolve_url.func.__name__, self.VIEW.as_view().__name__)
        self.assertEqual(resolve_url.view_name, self.VIEW_NAME)

    def test_some_list_count(self):
        # some-list요청시 할 수 있는 전체 Some개수가 기대값과 같은지 테스트
        #   (테스트용 Some를 여러개 생성해야 함)
        num = random.randrange(1, 10)
        for i in range(num):
            Some.objects.create(name=f'Some{i}')

        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), num)

    def test_some_list_pagination(self):
        # some-list요청시 pagination이 잘 적용 되어 있는지 테스트
        num = 13
        for i in range(num):
            Some.objects.create(name=f'Some{i + 1}')

        for i in range(math.ceil(num / self.PAGINATION)):
            response = self.client.get(self.PATH, {'page': i + 1})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertLessEqual(len(response.data.get('results')), self.PAGINATION)

            self.assertEqual(response.data.get('results'),
                             SomeSerializer(Some.objects.all()[i * self.PAGINATION:(i * self.PAGINATION) + self.PAGINATION], many=True).data, )
        
```

#### resolve()
`URL_PATH` 로 부터 `View`의 `function`을 가져 오는 것.
`ResolveMatch` 오브젝트를 반환한다. 해당 객체에는 여러가지 속성이 있다.

#### reverse()
`URL_NAME`으로 부터 `URL`의 `PATH`를 가져 오는 것


그리고 테스트시에는 데이터베이스가 임시로 생겼다가 지워진다. 만약 테스트를 디버깅 할 경우에 중단 했을 경우 다음 테스트 실행시 진행중이었던 더미 데이터베이스를 삭제 할 것이냐는 질문이 나오면 `yes`로 지워주고 테스트를 진행하면 된다.