# -*- coding: utf-8 -*-

import json
import requests

url = 'https://test-knowledge.support-project.org/api/knowledges'
token = 'Access token'

query = {
          'private_token': token,
          'tags': [],
          'publicFlag': 1,
          'editors': {
              'groups': [],
              'users': []
          },
          'viewers': {
              'groups': [],
              'users': []
          },
          'template': 'knowledge',
          'templateItems': [],
          'title': 'test_title',
          'content': 'test_content'
        }

headers = {
            'Content-type': 'application/json',
            'PRIVATE-TOKEN': token
        }

r = requests.post(
        url,
        json=query,
        headers=headers)
print(r)
print(r.text)
print(r.headers)
