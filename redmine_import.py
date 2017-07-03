import dataset
import pandas as pd

#db = dataset.connect('postgresql://postgres@localhost:5432/knowledge')
db = dataset.connect('postgresql://postgres@localhost:5432/knowledge_import_test')

# 管理者を取得
manager = db['users'].find_one(user_name='管理者ユーザ')
#print(manager['user_id'])
# 現在の最終記事を取得
last_knowledge = db['knowledges'].find_one(order_by='-knowledge_id')
#print(last_knowledge['knowledge_id'])


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

# create table object    
t_knowledges = db['knowledges'].table

# 以上
#knowledges = db.query(t_knowledges.select(t_knowledges.c.knowledge_id > last_knowledge['knowledge_id']))
knowledges = db.query(t_knowledges.select(t_knowledges.c.knowledge_id > 31))
print(type(knowledges))
print(dir(knowledges))

#NOTIFY_QUEUES 
l_knowledge_users = []
l_knowledge_histories = []
l_view_histories = []
for k in knowledges:
    l_knowledge_users.append(dict(knowledge_id=k['knowledge_id'], user_id=manager['user_id'], insert_user=manager['user_id'], insert_datetime=k['insert_datetime'], update_user=manager['user_id'], update_datetime=k['update_datetime'], delete_flag=0))
    l_knowledge_histories.append(dict(knowledge_id=k['knowledge_id'], history_no=1, title=k['title'], content=k['content'], public_flag=1, tag_ids='', tag_names='', like_count=0, comment_count=0, insert_user=manager['user_id'], insert_datetime=k['insert_datetime'], update_user=manager['user_id'], update_datetime=k['update_datetime'], delete_flag=0))
    l_view_histories.append(dict(knowledge_id=k['knowledge_id'], view_date_time=k['update_datetime'], insert_user=manager['user_id'], insert_datetime=k['insert_datetime'], update_user=manager['user_id'], update_datetime=k['update_datetime'], delete_flag=0))

#print(l_knowledge_users)
#print(l_knowledge_histories)
#print(l_view_histories)

db['knowledge_users'].insert_many(l_knowledge_users)
db['knowledge_histories'].insert_many(l_knowledge_histories)
db['view_histories'].insert_many(l_view_histories)
