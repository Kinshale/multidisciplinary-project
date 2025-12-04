import duckdb
import pandas as pd
import os
import time
from tqdm import tqdm


def filter_and_save_direct(
        input_file,
        min_avg_likes=5,
        output_file=None,
        max_rows=None
):
    """
    Process and save directly without intermediate temp files
    """
    print(f"Processing large file: {os.path.basename(input_file)}")
    print(f"File size: {os.path.getsize(input_file) / (1024 ** 3):.2f} GB")
    print(f"Minimum average weekly likes: {min_avg_likes}")

    start_time = time.time()

    # Connect to DuckDB with minimal memory usage
    conn = duckdb.connect()

    # Configure for direct writing
    conn.execute("PRAGMA memory_limit='8GB'")  # Use minimal memory
    conn.execute("SET threads=4")  # Reduce parallel processing
    conn.execute("SET preserve_insertion_order=false")  # Faster

    # Create output file name if not provided
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_filtered_{min_avg_likes}avg.parquet"

    print(f"Output will be saved to: {output_file}")

    # SINGLE EFFICIENT QUERY: Process and save in one go
    # This avoids creating intermediate dataframes or temp tables

    query = f"""
    COPY (
        -- Step 1: Get all qualifying users
        WITH qualifying_users AS (
            WITH user_weekly_stats AS (
                SELECT 
                    did_id,
                    DATE_TRUNC('week', DATE(created_at)) as week_start,
                    COUNT(*) as weekly_likes
                FROM read_parquet('{input_file}')
                WHERE created_at IS NOT NULL
                {'LIMIT ' + str(max_rows) if max_rows else ''}
                GROUP BY did_id, week_start
            )
            SELECT 
                did_id
            FROM user_weekly_stats
            GROUP BY did_id
            HAVING AVG(weekly_likes) >= {min_avg_likes}
        )
        -- Step 2: Get all records for qualifying users and save directly
        SELECT 
            q.did_id,
            DATE(r.created_at) as created_date,
            r.subject->>'did_id' as subject_did_id,
            r.subject->>'collection' as subject_collection
        FROM qualifying_users q
        JOIN read_parquet('{input_file}') r 
            ON q.did_id = r.did_id
        WHERE r.created_at IS NOT NULL
    ) TO '{output_file}' (FORMAT 'parquet')
    """

    print("Processing and saving data...")

    # Execute the query - this writes directly to disk
    conn.execute(query)

    # Get the count of saved records
    count_query = f"SELECT COUNT(*) FROM read_parquet('{output_file}')"
    total_records = conn.execute(count_query).fetchone()[0]

    elapsed_time = time.time() - start_time

    print(f"\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total processing time: {elapsed_time:.2f} seconds")
    print(f"Total records saved: {total_records:,}")
    print(f"Output file: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / (1024 ** 3):.2f} GB")

    conn.close()

    return output_file


def main():
    """Example usage"""

    # Input file path
    input_file = "likes.parquet"  # Update this path

    # Check if file exists
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        print("Please update the input_file path in the main() function.")
        return

    # Method 1: Batch processing with corrected query
    print("=" * 60)
    print("METHOD 1: Batch Processing (Corrected)")
    print("=" * 60)

    data_batch = filter_and_save_direct(
        input_file=input_file,
        min_avg_likes=30,
        output_file='likesFilteredChunks.parquet',
        max_rows=None  # Set to None for full processing
    )


if __name__ == '__main__':
    main()