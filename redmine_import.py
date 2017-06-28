import dataset
import pandas as pd

#db = dataset.connect('postgresql://postgres@localhost:5432/knowledge')
db = dataset.connect('postgresql://postgres@localhost:5432/knowledge_import_test')

# 管理者を取得
manager = db['users'].find_one(user_name='管理者ユーザ')
print(manager['user_id'])
# ['#', 'ステータス', 'プロジェクト', 'トラッカー', '優先度', '題名', '担当者', 'カテゴリ', '対象バージョン', '作成者', '開始日', '期日', '進捗 %', '予定工数', '親チケット', '作成日', '更新日', 'PL', 'タグ', '説明']
df = pd.read_csv('redmine_export.csv', header=1, names=('index', 'status', 'project', 'tracker', 'priority', 'title', 'staff', 'category', 'version', 'creator', 'started_at', 'limited_at', 'progress_rate', 'workload', 'parent_ticket', 'insert_datetime', 'update_datetime', 'pl', 'tag', 'contents'))
df = df.reindex_axis(['title', 'contents', 'insert_datetime', 'update_datetime'], axis=1)
df['public_flag'] = 1
df['tag_ids'] = None
df['tag_names'] = ""
df['like_count'] = None
df['comment_count'] = None
df['type_id'] = -100
df['notify_status'] = 0
df['insert_user'] = manager['user_id']
df['update_user'] = manager['user_id']
df['delete_flag'] = 0

dictionary = df.T.to_dict().values()

db['knowledges'].insert_many(dictionary)

