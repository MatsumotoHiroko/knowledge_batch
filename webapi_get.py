# -*- coding: utf-8 -*-

import json
import requests

knowledge_id = '43'
url = 'http://192.168.11.202:8080/knowledge/api/knowledges/' + knowledge_id
token = 'Access token'

query = {
          'private_token': token,
        }

r = requests.get(
        url,
        params=query)
print(r)
print(r.text)
print(r.headers)
