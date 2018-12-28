---
layout: post
title: "s3에 올라온 이미지를 aws lambda를 이용하여 썸네일 만들기"
categories:
  - aws
tags:
  - aws
  - serverless
---

# 기능
`aws lambda`를 이용하여 `s3`에 업로드된 이미지를 `Pillow`를 사용하여 썸네일을 만든후 다시 `s3`에 업로드 함.