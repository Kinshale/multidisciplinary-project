import pyarrow.parquet as pq
import random
import duckdb
from sli_queries import (LIKES_AB_QUERY, LIST_A_QUERY,LIST_B_QUERY,LIKES_BA_QUERY,BLOCKS_AB_QUERY,BLOCKS_BA_QUERY,
                     FOLLOWS_AB_QUERY,FOLLOWS_BA_QUERY,PROFILES_A_QUERY,PROFILES_B_QUERY,REPOSTS_AB_QUERY,
                     REPOSTS_BA_QUERY,LISTBLOCK_AB_QUERY,LISTBLOCK_BA_QUERY,LIST_ITEMS_AB_QUERY,LIST_ITEMS_BA_QUERY,
                     POSTS_AB_ROOT_QUERY,POSTS_BA_ROOT_QUERY,POSTS_AB_PARENT_QUERY,POSTS_BA_PARENT_QUERY,
                     LIST_ITEMS_AB_CREATOR_QUERY,LIST_ITEMS_BA_CREATOR_QUERY)

from datetime import date, timedelta
import pickle

MAX_LEN=100
MIN_LEN=1

BF="crawler/sli_user2user_blocking.pkl"
NBF="crawler/sli_user2user_non_blocking.pkl"

LIKES_DS="crawler/likes.parquet"
BLOCKS_DS="crawler/blocks.parquet"


def choose_random_users(parquet_file):
    
    table = parquet_file.read_row_group(random.randint(0, parquet_file.num_row_groups-1))

    row = table.slice(random.randint(0, len(table)-1), 1).to_pylist()[0]
    
    return row["did_id"], row["subject_did_id"]



def get_events(file_name, query, user1, user2):
    
    filled_query = query.format(file_name=file_name, user1=user1, user2=user2)

    result = duckdb.query(filled_query)
    cols = [c[0] for c in result.description]

    rows = result.fetchall()

    list_of_dicts = [dict(zip(cols, row)) for row in rows]

    return list_of_dicts


def choose_random_users(parquet_file):
    
    table = parquet_file.read_row_group(random.randint(0, parquet_file.num_row_groups-1))

    row = table.slice(random.randint(0, len(table)-1), 1).to_pylist()[0]
    
    return row["did_id"], row["subject_did_id"]



def append_to_pickle(file_path, new_data):
    
    existing_data=[]
    with open(file_path, 'rb') as f:
        existing_data = pickle.load(f)

    existing_data.append(new_data)
    
    with open(file_path, 'wb') as f:
        pickle.dump(existing_data, f)



pf1 = pq.ParquetFile(LIKES_DS)
pf2 = pq.ParquetFile(BLOCKS_DS)



c=0
while True:
    event_list=[]

    if c%2==0:
        user1, user2= choose_random_users(pf1)
    else:
        user1, user2= choose_random_users(pf2)

    user1, user2= choose_random_users(pf1)

    event_list+= get_events("datasets/likes.parquet", LIKES_AB_QUERY, user1, user2)
    event_list+= get_events("datasets/likes.parquet", LIKES_BA_QUERY, user1, user2)

    event_list+= get_events("datasets/follows.parquet", FOLLOWS_AB_QUERY, user1, user2)
    event_list+= get_events("datasets/follows.parquet", FOLLOWS_BA_QUERY, user1, user2)

    event_list+= get_events("datasets/reposts.parquet", REPOSTS_AB_QUERY, user1, user2)
    event_list+= get_events("datasets/reposts.parquet", REPOSTS_BA_QUERY, user1, user2)
    event_list+= get_events("datasets/list_blocks.parquet", LISTBLOCK_AB_QUERY, user1, user2)
    event_list+= get_events("datasets/list_blocks.parquet", LISTBLOCK_BA_QUERY, user1, user2)

    event_list+=  get_events("datasets/lists.parquet", LIST_A_QUERY, user1, user2)
    event_list+=  get_events("datasets/lists.parquet", LIST_B_QUERY, user1, user2)

    event_list+=  get_events("datasets/profiles.parquet", PROFILES_A_QUERY, user1, user2)
    event_list+=  get_events("datasets/profiles.parquet", PROFILES_B_QUERY, user1, user2)
    event_list+= get_events("datasets/posts.parquet", POSTS_AB_ROOT_QUERY, user1, user2)
    event_list+= get_events("datasets/posts.parquet", POSTS_BA_ROOT_QUERY, user1, user2)
    event_list+= get_events("datasets/posts.parquet", POSTS_AB_PARENT_QUERY, user1, user2)
    event_list+= get_events("datasets/posts.parquet", POSTS_BA_PARENT_QUERY, user1, user2)

    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_AB_QUERY, user1, user2)
    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_BA_QUERY, user1, user2)
    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_AB_CREATOR_QUERY, user1, user2)
    event_list+=  get_events("datasets/list_items.parquet", LIST_ITEMS_BA_CREATOR_QUERY, user1, user2)

    block_list=[]
    
    block_list+=  get_events("datasets/blocks.parquet", BLOCKS_AB_QUERY, user1, user2)
    block_list+=  get_events("datasets/blocks.parquet", BLOCKS_BA_QUERY, user1, user2)

    event_list = sorted(
                        event_list, 
                        key=lambda x: (x['created_date'] is None, x['created_date'])
                    )

    if c%2==0:
        file=BF
    else:
        file=NBF


    if len(event_list)> MIN_LEN:
        append_to_pickle(file,{"events":event_list, "blocks":block_list})
        c+=1
    print(c)


    
