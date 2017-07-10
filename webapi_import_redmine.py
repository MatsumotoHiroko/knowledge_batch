# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd

api_url = 'http://192.168.11.202:8080/knowledge'
api_token = 'API TOKEN'
db_url = 'postgresql://postgres@localhost:5432/knowledge'
def run_post_api(df):
    query = {
              #'private_token': api_token,
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
              'template': 'redmine移行用',
              'templateItems': [],
              'title': df['title'],
              'content': df['content']
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


# ['#', 'ステータス', 'プロジェクト', 'トラッカー', '優先度', '題名', '担当者', 'カテゴリ', '対象バージョン', '作成者', '開始日', '期日', '進捗 %', '予定工数', '親チケット', '作成日', '更新日', 'PL', 'タグ', '説明']
df = pd.read_csv('redmine_export.csv', header=1, names=('index', 'status', 'project', 'tracker', 'priority', 'title', 'staff', 'category', 'version', 'creator', 'started_at', 'limited_at', 'progress_rate', 'workload', 'parent_ticket', 'insert_datetime', 'update_datetime', 'pl', 'tag', 'contents'))
df = df.reindex_axis(['title', 'contents'], axis=1)
print(df)

for d in df:
    run_post_api(d)
    break
