import duckdb

def main():
    query = """
    SELECT subject_did_id
    FROM read_parquet('likesFinal4.parquet')
    WHERE subject_did_id NOT IN (
        SELECT DISTINCT did_id
        FROM read_parquet('likesFinal4.parquet')
    )
    """
    result = duckdb.query(query).fetchdf()
    print(result)

    query = """
        SELECT *
        FROM read_parquet('likesFinal4.parquet')
        WHERE subject_did_id NOT IN (
            SELECT DISTINCT did_id
            FROM read_parquet('likesFinal4.parquet')
        )
        """
    result = duckdb.query(query).fetchdf()
    print(result)



if __name__ == "__main__":
    main()