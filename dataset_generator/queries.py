LIKES_QUERY ="""
    SELECT
        did_id AS did_id,
        subject.did_id AS subject_id,
        subject.collection AS collection,
        created_at AS created_at
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and subject.did_id={user2}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'""" 

FOLLOWS_QUERY="""
    SELECT
        did_id AS did_id,
        subject_id AS subject_id,
        created_at AS created_at
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and subject_id={user2}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'"""

REPOSTS_QUERY ="""
    SELECT
        did_id AS did_id,
        subject.did_id AS subject_id,
        subject.collection AS collection,
        created_at AS created_at
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and subject.did_id={user2}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'""" 

LISTBLOCK_QUERY ="""
    SELECT
        did_id AS did_id,
        subject.did_id AS subject_id,
        subject.collection AS collection,
        created_at AS created_at
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and subject.did_id={user2}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'""" 

BLOCKS_QUERY="""
    SELECT
        did_id AS did_id,
        subject_id AS subject_id,
        created_at AS created_at
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and subject_id={user2}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'"""

LIST_ITEMS_QUERY="""
    SELECT
        did_id AS did_id,
        subject_id AS subject_id,
        created_at AS created_at,
        list.did_id AS list_creator,
        list.collection collection
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and subject_id={user2}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'"""

LIST_QUERY="""
    SELECT
        did_id AS did_id,
        created_at AS created_at,
        purpose AS purpose,
        labels AS labels,
        name AS name
    FROM read_parquet({file_name})
    WHERE did_id = {user1}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'"""

PROFILES_QUERY="""
    SELECT
        did_id AS did_id,
        created_at AS created_at,
        labels AS labels,
    FROM read_parquet({file_name})
    WHERE did_id = {user1}
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'"""

POSTS_QUERY="""
    SELECT
        did_id AS did_id,
        created_at AS created_at,
        labels AS labels,
        languages AS languages,
        reply.root.did_id AS root_id,
        reply.parent.did_id AS parent_id
    FROM read_parquet({file_name})
    WHERE did_id = {user1} and (reply.root.did_id={user2} OR reply.parent.did_id={user2})
    AND created_at >= TIMESTAMP '{start_datetime}' AND created_at <= TIMESTAMP '{end_datetime}'"""
