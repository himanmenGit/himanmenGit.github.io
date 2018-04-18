## python-magic 의 MIME TYPE를 이용하여 이미지를 읽어 확장자를 알아 내는 방법

> MIME TYPE은 클라이언트에 전송된 문서의 다양성을 알려주기 위한 매커니즘.
> 웹에서 전송 된 해당 객체가 어떤 타입인지 알려 주어야 한다. 그것을 하기 위한 것.

*python-magic 설치
```
pip install python-magic
```

```pyhton
import magic
import requests
from io import BytesIO

url = 'http://cdnimg.melon.co.kr/cm/artistcrop/images/002/61/143/261143_500.jpg?8278b340c081cd2bd020bff2d632329f/melon/resize/416/quality/80/optimize'

response = requests.get(url)
binary_file = BytesIO()
binary_file.write(response.content)
binary_file.seek(0)
# mime_type = magic.from_file(<filename>, mime=True)	
mime_type = magic.from_buffer(binary_file.read(), mime=True)
file_ext = mime_type.split('/')[-1]

# >> 'jpeg'
```

