# Detail View만들기
`SomeList`의 `get`은 리스트를 가져 오는 것이고, `post`는 리스트에 추가 하는 것이었다. 하지만 `DetailView`에서는 `get`이 해당 리스트중 하나를 조회, `put`은 업데이트 `delete`는 삭제를 한다.
이것이 RestAPI에서 가장 기본적인 구조이다.

```
# views.py
class SomeDetail(APIView):
    def get_object(self, pk):
        somemodel = get_object_or_404(SomeModel, pk)
        return somemodel

    def get(self, request, pk):
        somemodel = self.get_object(pk)
        serializer = SnippetSerializer(somemodel)
        return Response(serializer.data)

    def post(self, request, pk):
        somemodel = self.get_object(pk)
        serializer = SnippetSerializer(somemodel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        somemodel = self.get_object(pk)
        somemodel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```
```
# urls.py
urlpatterns = [
    ...
    path('<int:pk>/', SomeDetail.as_view()),
]

```
* `get_object_or_404`를 rest_framwork에서 가져오는 것은 에러메시지가 json형태로 반환되기 때문이다.
* `Response`에서 `status`를 돌려 주지 않으면 기본 값인 `HTTP_200_OK`이 간다.

# URL의 점미어를 통해 다른 포맷 제공하기
포맷의 접미어를 URL 형태로 전달 받으려면, URL을 다룰수 있어야 함.
`http://example.com/api/items/4.json` 이런 형태는 `json`형태로 받고 싶은 것이고 만약 `1.xml`이면 `xml`형태로 받고 싶은 것이다. 
그럴려면 각 기능 함수에 `foramt=None`이라는 인자를 넣어 준다.
```
class SomeList(APIView):
    def get(self, request, format=None):
        ...
    def post(self, request, format=None):
        ...
```
그리고 `urlpatterns`를 한번 감싸야 한다.
```
from rest_framework.urlpatterns import format_suffix_patterns
...
urlpatterns = format_suffix_patterns(urlpatterns)

```
그리고 `xml`에 대한 테스트를 위해 `djangorestframework-xml`을 설치하자
```
pip install djangorestframework-xml
```
그리고 셋팅을 하자
`config/settings`에 기본설정과 추가 설정을 넣자.
```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_xml.parsers.XMLParser',
    )
}
```
그리고 `http://localhost:8000/somemodel/?format=xml`을 하면 데이터가 `xml`로 바뀌어서 온것을 볼 수 있다.