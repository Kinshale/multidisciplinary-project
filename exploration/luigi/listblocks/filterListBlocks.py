import duckdb
import pandas as pd
import os
import time
from tqdm import tqdm


def filter_and_save_direct(
        input_file,
        did_file,
        output_file=None
):
    """
    Process and save directly without intermediate temp files
    """
    print(f"Processing large file: {os.path.basename(input_file)}")

    start_time = time.time()

    # Connect to DuckDB with minimal memory usage
    conn = duckdb.connect()

    # Configure for direct writing
    conn.execute("PRAGMA memory_limit='8GB'")  # Use minimal memory
    conn.execute("SET threads=4")  # Reduce parallel processing
    conn.execute("SET preserve_insertion_order=false")  # Faster

    print(f"Output will be saved to: {output_file}")

    # SINGLE EFFICIENT QUERY: Process and save in one go
    # This avoids creating intermediate dataframes or temp tables

    query = f"""
    COPY (
        SELECT *
        FROM read_parquet('{input_file}')
        WHERE did_id IN (
            SELECT DISTINCT did_id 
            FROM read_parquet('{did_file}')
            )
    ) TO '{output_file}' (FORMAT 'parquet')
    """

    # Execute the query - this writes directly to disk
    conn.execute(query)

    elapsed_time = time.time() - start_time

    print("PROCESSING COMPLETE")
    print(f"Total processing time: {elapsed_time:.2f} seconds")
    print(f"Output file: {output_file}")
    conn.close()

    return output_file


def main():
    """Example usage"""

    # Input file path
    input_file = "list_blocksFiltered.parquet"  # Update this path
    did_file = "../INTERSECTbothDID.parquet"
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
        did_file=did_file,
        output_file='list_blocksFiltered2.parquet',
    )


if __name__ == '__main__':
    main()