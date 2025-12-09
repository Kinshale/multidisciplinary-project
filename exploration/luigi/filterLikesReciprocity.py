import duckdb

def delete_useless_events(file_name,output_file_name):
    """
    from the likes dataset deletes all the
    events where the id receiving a like is
    not in the dataset as an id giving a like
    """


    query = """
    COPY (
        SELECT *
        FROM read_parquet({file_name})
        WHERE subject_did_id IN (
            SELECT DISTINCT did_id
            FROM read_parquet({file_name})
        )
    )
    TO '{output_file_name}'
    (FORMAT PARQUET);
    """
    query= query.format(file_name=file_name,output_file_name=output_file_name)
    duckdb.query(query)

if __name__ == "__main__":
    delete_useless_events('likesFinal1.parquet','likesFinal2.parquet')