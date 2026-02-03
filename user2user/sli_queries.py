LIKES_AB_QUERY ="""
    SELECT
        *,
        'likeAB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and subject_did_id={user2}
""" 

LIKES_BA_QUERY ="""
    SELECT
        *,
        'likeBA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and subject_did_id={user1}
""" 

FOLLOWS_AB_QUERY="""
    SELECT
        *,
        'followAB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and subject_did_id={user2}
"""

FOLLOWS_BA_QUERY="""
    SELECT
        *,
        'followBA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and subject_did_id={user1}
"""

REPOSTS_AB_QUERY ="""
    SELECT
        *,
        'repostAB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and subject_did_id={user2}
"""

REPOSTS_BA_QUERY ="""
    SELECT
        *,
        'repostBA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and subject_did_id={user1}
"""

LISTBLOCK_AB_QUERY ="""
    SELECT
        *,
        'list_blockAB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and subject_did_id={user2}
"""

LISTBLOCK_BA_QUERY ="""
    SELECT
        *,
        'list_blockBA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and subject_did_id={user1}
""" 

BLOCKS_AB_QUERY="""
    SELECT
        *,
        'blockAB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and subject_did_id={user2}
"""

BLOCKS_BA_QUERY="""
    SELECT
        *,
        'blockBA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and subject_did_id={user1}
"""

LIST_A_QUERY="""
    SELECT
        *,
        'listA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1}
"""

LIST_B_QUERY="""
    SELECT
        *,
        'listB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2}
"""

PROFILES_A_QUERY="""
    SELECT
        *,
        'profileA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1}
"""

PROFILES_B_QUERY="""
    SELECT
        *,
        'profileB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2}
"""

POSTS_AB_ROOT_QUERY="""
    SELECT
        *,
        'postABroot' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and reply_root_did_id={user2}
"""

POSTS_AB_PARENT_QUERY="""
    SELECT
        *,
        'postABparent' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and reply_parent_did_id={user2}
"""

POSTS_BA_ROOT_QUERY="""
    SELECT
        *,
        'postBAroot' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and reply_root_did_id={user1}
"""

POSTS_BA_PARENT_QUERY="""
    SELECT
        *,
        'postBAparent' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and reply_parent_did_id={user1}
"""

LIST_ITEMS_AB_QUERY="""
    SELECT
        *,
        'list_itemAB' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and subject_did_id={user2}
"""

LIST_ITEMS_AB_CREATOR_QUERY="""
    SELECT
        *,
        'list_itemABcreator' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user1} and list_did_id={user2}
"""

LIST_ITEMS_BA_QUERY="""
    SELECT
        *,
        'list_itemBA' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and subject_did_id={user1}
"""

LIST_ITEMS_BA_CREATOR_QUERY="""
    SELECT
        *,
        'list_itemBAcreator' as event
    FROM read_parquet('{file_name}')
    WHERE did_id = {user2} and list_did_id={user1}
"""