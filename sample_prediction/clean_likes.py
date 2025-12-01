import duckdb

def delete_useless_events(file_name):
    """
    from the likes dataset deletes all the 
    events where the id receiving a like is 
    not in the dataset as an id giving a like
    """


    query = """
    COPY (
        SELECT *
        FROM read_parquet({file_name})
        WHERE subject.did_id IN (
            SELECT DISTINCT did_id
            FROM read_parquet({file_name})
        )
    )
    TO '{file_name}'
    (FORMAT PARQUET);
    """ 
    query= query.format(file_name=file_name)
    duckdb.query(query)


delete_useless_events("chunk_0_likes.parquet")