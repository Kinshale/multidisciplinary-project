import duckdb

def main():
    query = """
        SELECT *
        FROM read_parquet(followsFilteredFinal6.parquet)
        WHERE did_id NOT IN (
            SELECT DISTINCT subject_did_id
            FROM read_parquet(followsFilteredFinal6.parquet)
            GROUP BY subject_did_id
            HAVING COUNT(subject_did_id) > 1
            )
    """
    result = duckdb.query(query).fetchdf()
    print(result)

    query = """
            SELECT *
            FROM read_parquet('followsFilteredFinal6.parquet')
            WHERE subject_did_id NOT IN (
                SELECT DISTINCT did_id
                FROM read_parquet('followsFilteredFinal6.parquet')
            )
            """
    result = duckdb.query(query).fetchdf()
    print(result)

if __name__ == "__main__":
    main()