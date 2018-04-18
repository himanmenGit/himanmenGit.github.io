`settings.py` 에서 불러 오는 `base.json`의 값들을 하나씩 불러오는 것이 아닌 동적으로 파일을 파싱하여 해당 변수를 `eval()`을 통해 동적으로 할당을 해보자.

`sys.modules[<module name>]`을 사용하여 module name을 할당 받아 해당 모듈에 있는 것을 사용할 수 있다. 그리고 `getattr`을 사용해 해달 모 듈의 변수를 가져 올 수 있다. 반대로 `setattr`로 해당 모듈에 변수를 넣을 수도 있다.
만약 문자열이 있을때 문자열이 가진 내용을 해석 하여 가져 오고 싶을 경우도 있다. 이경우 `eval()` 내장함수를 사용하여 가져 올 수 있다.
```
import os
BASE_DIR =os.path.dirname(os.path.abspath(__name__))
# BASE_DIR /home/user/projects/temp
import sys 
m = sys.modules[__name__]
# m <module '__main__'>

getattr(m, 'BASE_DIR')
BASE_DIR
# BAES_DIR과 getattr(m, BASE_DIR)은 동일하다.

setattr(m, 'ROOT_DIR', os.path.dirname(BASE_DIR))
ROOT_DIR
# ROOT_DIR /home/user/projects

s = 'ROOT_DIR'
eval(s)
# ROOT_DIR /home/user/projects

import json
s3 = '{"SECRET_DIR": "os.path.join(ROOT_DIR, \'.secrets\')"}'
d = json.loads(s3)
eval(d['SECRET_DIR'])
# SECRET_DIR /home/user/projects/.secrets
```

파일의 크기와 뎁스를 모르니 재귀 함수로 모두 탐색 하면서 할당 하자
그리고 `eval()` 함수로 파이썬 객체의 타입에 따라 변환이 불가한 경우(int, float, str and digit, 없는 변수, 모든 Exception) 그냥 그 객체를 반환하는 검사도 해야 한다.
```
def set_config(obj, start=False):
    """
    Python객체를 받아, 해당 객체의 key-value쌍을
    현재 모듈(config.settings.base)에 동적으로 할당
    1. dict거나 list일 경우에는 내부 값들이 eval()이 가능한지 검사해야 함
    2. value가 dict나 list가 아닐 경우에는
        2-1. eval()이 가능하다면 해당 결과를 할당
        2-2. eval()이 불가능하다면 (일반 텍스트나 숫자일 경우) 값 자체를 할당
    :param obj:
    :return:
    """

    def eval_obj(obj):
        """
        주어진 파이썬 객체의 타입에 따라 eval()결과를 반환하거나 불가한 경우 그냥 그 객체를 반환
        1. 그대로 반환
            - int, float형이거나 str형이며 숫자 변환이 가능한 경우에는 그대로 반환
            - eval()에서 예외가 발생했으며 없는 변수를 참조할때의 NameError가 발생한 경우
        2. eval() 평가값을 반환
            - 1번의 경우가 아니며 eval()이 가능한 경우 평가값을 반환
        3. 그대로 반환하되, 로그를 출력
            - 1번의 경우가 아니며 eval()에서 NameError외의 예외가 발생한 경우
        :param obj: 파이썬 객체
        :return: eval(obj)또는 obj
        """
        # 객체가 int, float거나
        if isinstance(obj, numbers.Number) or (
                # str형이면서 숫자 변환이 가능한 경우
                isinstance(obj, str) and obj.isdigit()):
            return obj

        # 객체가 int, float가 아니면서 숫자형태를 가진 str도 아닐경우
        try:
            return eval(obj)
        except NameError:
            # 없는 변수를 참조할 때 발생하는 예외
            return obj
        except Exception as e:
            # print(f'Cannot eval object({obj}), Exception: {e}')
            return obj
            # raise ValueError(f'Cannot eval object({obj}), Exception: {e}')

    # base.json파일을 parsing한 결과 (Python dict)를 순회
    # set_config에 전달된 객체가 'dict'형태일 경우
    if isinstance(obj, dict):
        # key, value를 순회
        for key, value in obj.items():
            # value가 dict거나 list일 경우 재귀적으로 함수를 다시 실행
            if isinstance(value, dict) or isinstance(value, list):
                set_config(value)
            # 그 외의 경우 value를 평가한 값을 할당
            else:
                obj[key] = eval_obj(value)
            # set_config()가 처음 호출된 loop에서만 setattr()을 실행
            if start:
                setattr(sys.modules[__name__], key, value)
    # 전달된 객체가 'list'형태일 경우
    elif isinstance(obj, list):
        # list아이템을 순회하며
        for index, item in enumerate(obj):
            # list의 해당 index에 item을 평가한 값을 할당
            obj[index] = eval_obj(item)

```

`import raven`도 동적으로 할당하자 `importlib` 를 쓰면 된다.
```
# base.json
"raven": "importlib.import_module('raven')",
```
그리고 `base.json`을 함수에 넣어주자
```
set_config(secrets, root=True)
```

그리고 export로 local환경 변수를 지정해 주는것을 자동으로 하게 만들자
`manage.py`의 `DJANGO_SETTINGS_MODULE`을 가져오는것을 활용하여 `DJANGO_SETTINGS_MODULE`가 빈값이거나 기본 값이면 `local settings`를 로드하자.
```
import os

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not SETTINGS_MODULE or SETTINGS_MODULE == 'config.settings':
    from .local import *

```