---
layout: post
title: "장고 템플릿 include에서 jquery를 이용한 클래스 설정"
categories:
  - Django
tags:
  - Django
  - Jquery
---


장고 템플릿 `base.html`에 `include`를 이용하여 `kind`를 `child.html`로 전달하여 사용

{% raw %}
```html
<div class="parent">
    {% include 'child.html' with kind='report' %}
 </div>
```

```html
<a href="{% url 'faq_page' %}" id="faq" class="faq_class">FAQ</a>
<a href="{% url 'contact_page' %}" id="contact" class="contact_class">문의</a>
<a href="{% url 'report_page' %}" id="report" class="report_class">신고</a>

<script type="text/javascript">    
    (function () {
          $('.base a').each(function () {
            var id = $(this).attr('id')
            if(id == '{{ kind }}'){
                // 해당 페이지를 활성화 시키고
                // href 속성을 제거함
                $(this).addClass('active').removeAttr("href");
            }else{
                // 해당 페이지를 제외한 페이지들은
                // 비활성 함
                $(this).removeClass('active')
            }
        })
    })
</script>
```
{% endraw %}
