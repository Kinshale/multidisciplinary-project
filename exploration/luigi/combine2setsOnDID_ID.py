import duckdb

def delete_useless_events(file_name,file_name2,output_file_name):
    """
    from the likes dataset deletes all the
    events where the id receiving a like is
    not in the dataset as an id giving a like
    """


    query = """
    COPY (
        SELECT DISTINCT did_id
        FROM read_parquet({file_name})
        UNION
        SELECT DISTINCT did_id
        FROM read_parquet({file_name2})
    )
    TO '{output_file_name}'
    (FORMAT PARQUET);
    """
    query= query.format(file_name=file_name,file_name2=file_name2,output_file_name=output_file_name)
    duckdb.query(query)

if __name__ == "__main__":
    delete_useless_events(file_name='followsFilteredFinal.parquet',file_name2='likesFinal.parquet',output_file_name='UNIONbothDID.parquet')