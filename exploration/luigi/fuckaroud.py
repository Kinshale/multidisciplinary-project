import duckdb
from tqdm import tqdm


def count_unique_ids_whole_file(parquet_file):
    """Count unique IDs from the original 220GB parquet file"""

    print(f"Counting unique IDs from: {parquet_file}")

    conn = duckdb.connect()

    # Count unique IDs directly from the big file
    query = f"""
    SELECT COUNT(DISTINCT did_id) as total_unique_ids
    FROM read_parquet('{parquet_file}')
    """

    result = conn.execute(query).fetchone()
    conn.close()

    unique_count = result[0] if result else 0
    print(f"Total unique did_id in whole file: {unique_count:,}")

    return unique_count

if __name__ == "__main__":
    # Usage
    unique_count = count_unique_ids_whole_file('likes.parquet')
    print(f"Total unique did_id in whole file: {unique_count:,}")