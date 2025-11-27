import pyarrow.parquet as pq
import random
import duckdb
from queries import LIKES_QUERY, FOLLOWS_QUERY, REPOSTS_QUERY, LISTBLOCK_QUERY, BLOCKS_QUERY, LIST_ITEMS_QUERY, LIST_QUERY, PROFILES_QUERY, POSTS_QUERY
from datetime import datetime
import time


def choose_random_users(parquet_file):
    
    table = parquet_file.read_row_group(random.randint(0, parquet_file.num_row_groups-1))

    row = table.slice(random.randint(0, len(table)-1), 1).to_pylist()[0]

    return row["did_id"], row["subject"]["did_id"]




def get_events(file_name, query, user1, user2, start_datetime, end_datetime):
    
    filled_query = query.format(file_name=file_name, user1=user1, user2=user2, start_datetime=start_datetime, end_datetime=end_datetime)

    result = duckdb.query(filled_query)
    cols = [c[0] for c in result.description]

    rows = result.fetchall()

    list_of_dicts = [dict(zip(cols, row)) for row in rows]

    return list_of_dicts




pf = pq.ParquetFile("chunk_0_likes.parquet")
start = datetime(2024, 9, 3, 0, 0, 0).astimezone()
end   = datetime(2024, 9, 4, 0, 0, 0).astimezone()




start = time.perf_counter()

for i in range(1):
    event_list=[]

    user1, user2= choose_random_users(pf)

    event_list+= get_events("chunk_0_likes.parquet", LIKES_QUERY, user1, user2, start, end)
    event_list+= get_events("chunk_0_follow.parquet", FOLLOWS_QUERY, user1, user2, start, end)
    event_list+= get_events("chunk_0_posts.parquet", POSTS_QUERY, user1, user2, start, end)
    event_list+= get_events("chunk_0_reposts.parquet", REPOSTS_QUERY, user1, user2, start, end)
    event_list+= get_events("list_blocks.parquet", LISTBLOCK_QUERY, user1, user2, start, end)
    event_list+= get_events("list_items.parquet", LIST_ITEMS_QUERY, user1, user2, start, end)
    event_list+= get_events("lists.parquet", LIST_QUERY, user1, user2, start, end)
    event_list+= get_events("profiles.parquet", PROFILES_QUERY, user1, user2, start, end)

end = time.perf_counter()


print(event_list)
print(f"Calculation took {end - start:.6f} seconds")