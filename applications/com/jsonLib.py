#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.http import HttpResponse

import json

def jsonStr(jsonobj):
    return json.dumps(jsonobj, indent=4, ensure_ascii=False, encoding='utf8')
def jsonResponse(jsonobj):
    return HttpResponse(jsonStr(jsonobj))
