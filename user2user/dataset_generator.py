import pyarrow.parquet as pq
import random
import duckdb
from queries import (LIKES_AB_QUERY, LIST_A_QUERY,LIST_B_QUERY,LIKES_BA_QUERY,BLOCKS_AB_QUERY,BLOCKS_BA_QUERY,
                     FOLLOWS_AB_QUERY,FOLLOWS_BA_QUERY,PROFILES_A_QUERY,PROFILES_B_QUERY,REPOSTS_AB_QUERY,
                     REPOSTS_BA_QUERY,LISTBLOCK_AB_QUERY,LISTBLOCK_BA_QUERY,LIST_ITEMS_AB_QUERY,LIST_ITEMS_BA_QUERY,
                     POSTS_AB_ROOT_QUERY,POSTS_BA_ROOT_QUERY,POSTS_AB_PARENT_QUERY,POSTS_BA_PARENT_QUERY,
                     LIST_ITEMS_AB_CREATOR_QUERY,LIST_ITEMS_BA_CREATOR_QUERY)

from datetime import date, timedelta
import pickle



def choose_random_users(parquet_file):
    
    table = parquet_file.read_row_group(random.randint(0, parquet_file.num_row_groups-1))

    row = table.slice(random.randint(0, len(table)-1), 1).to_pylist()[0]
    
    return row["did_id"], row["subject_did_id"], row["created_date"]



def get_events(file_name, query, user1, user2, start_datetime, end_datetime):
    
    filled_query = query.format(file_name=file_name, user1=user1, user2=user2, start_datetime=start_datetime, end_datetime=end_datetime)

    result = duckdb.query(filled_query)
    cols = [c[0] for c in result.description]

    rows = result.fetchall()

    list_of_dicts = [dict(zip(cols, row)) for row in rows]

    return list_of_dicts



def append_to_pickle(file_path, new_data):
    
    existing_data=[]
    with open(file_path, 'rb') as f:
        existing_data = pickle.load(f)

    existing_data.append(new_data)
    
    with open(file_path, 'wb') as f:
        pickle.dump(existing_data, f)



pf = pq.ParquetFile("datasets/likes.parquet")



c=0
# for i in range(1):
while True:
    event_list=[]

    user1, user2, start_date= choose_random_users(pf)
    end_date=start_date + timedelta(days=6)

    event_list+= get_events("datasets/likes.parquet", LIKES_AB_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/likes.parquet", LIKES_BA_QUERY, user1, user2, start_date, end_date)

    event_list+= get_events("datasets/follows.parquet", FOLLOWS_AB_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/follows.parquet", FOLLOWS_BA_QUERY, user1, user2, start_date, end_date)

    event_list+= get_events("datasets/reposts.parquet", REPOSTS_AB_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/reposts.parquet", REPOSTS_BA_QUERY, user1, user2, start_date, end_date)

    event_list+= get_events("datasets/list_blocks.parquet", LISTBLOCK_AB_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/list_blocks.parquet", LISTBLOCK_BA_QUERY, user1, user2, start_date, end_date)

    event_list+=  get_events("datasets/lists.parquet", LIST_A_QUERY, user1, user2, start_date, end_date)
    event_list+=  get_events("datasets/lists.parquet", LIST_B_QUERY, user1, user2, start_date, end_date)

    event_list+=  get_events("datasets/profiles.parquet", PROFILES_A_QUERY, user1, user2, start_date, end_date)
    event_list+=  get_events("datasets/profiles.parquet", PROFILES_B_QUERY, user1, user2, start_date, end_date)

    event_list+= get_events("datasets/posts.parquet", POSTS_AB_ROOT_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/posts.parquet", POSTS_BA_ROOT_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/posts.parquet", POSTS_AB_PARENT_QUERY, user1, user2, start_date, end_date)
    event_list+= get_events("datasets/posts.parquet", POSTS_BA_PARENT_QUERY, user1, user2, start_date, end_date)

    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_AB_QUERY, user1, user2, start_date, end_date)
    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_BA_QUERY, user1, user2, start_date, end_date)
    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_AB_CREATOR_QUERY, user1, user2, start_date, end_date)
    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_BA_CREATOR_QUERY, user1, user2, start_date, end_date)


    block_list=[]
    
    start_date2=start_date+ timedelta(days=7)
    end_date2=start_date2 + timedelta(days=6)

    block_list+=  get_events("datasets/blocks.parquet", BLOCKS_AB_QUERY, user1, user2, start_date2, end_date2)
    block_list+=  get_events("datasets/blocks.parquet", BLOCKS_BA_QUERY, user1, user2, start_date2, end_date2)

    append_to_pickle("datasets/user2user_events.pkl",{"events":event_list, "blocks":block_list, "start_date": start_date})

    c+=1
    print(c)


    
