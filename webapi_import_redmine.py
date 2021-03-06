# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
import os
import os.path
import glob

api_url = 'http://192.168.11.202:8080/knowledge/api/knowledges'
api_token = 'API TOKEN'
db_url = 'postgresql://postgres@localhost:5432/knowledge'
csv_dir = './csv'
def run_post_api(d):
    query = {
              #'private_token': api_token,
              'tags': [],
              'publicFlag': 2,
              'editors': {
                  'groups': [],
                  'users': []
              },
              'viewers': {
                  'groups': [
                      {
                          'id': '4',
                      }
                  ],
                  'users': []
              },
              'template': '[システム]redmine移行用',
              'templateItems': [
                  {
                      'label': '[必須]担当者名、対応者名',
                      'value': d['staff']
                  }
              ],
              'title': d['title'],
              'content': d['content']
            }
    
    headers = {
                'Content-type': 'application/json',
                'PRIVATE-TOKEN': api_token
            }
    
    r = requests.post(
            api_url,
            json=query,
            headers=headers)
    print(r)
    print(r.text)
    print(r.headers)

for dirname in glob.iglob(csv_dir + '/*'):
    if os.path.isdir(dirname):
        print(dirname)
        for filename in glob.iglob(dirname + '/*.csv'):
            print(filename)
            # ['#', 'ステータス', 'プロジェクト', 'トラッカー', '優先度', '題名', '担当者', 'カテゴリ', '対象バージョン', '作成者', '開始日', '期日', '進捗 %', '予定工数', '親チケット', '作成日', '更新日', 'PL', 'タグ', '説明']
            df = pd.read_csv(filename, header=1, names=('index', 'status', 'project', 'tracker', 'priority', 'title', 'staff', 'category', 'version', 'creator', 'started_at', 'limited_at', 'progress_rate', 'workload', 'parent_ticket', 'insert_datetime', 'update_datetime', 'pl', 'tag', 'content'))
            df = df.reindex_axis(['title', 'content', 'staff'], axis=1)
            dictionary = df.T.to_dict().values()
            print(dictionary)
            for d in dictionary:
                #run_post_api(d)
                break
