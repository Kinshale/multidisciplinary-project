import duckdb
import pandas as pd
import os
import time
from tqdm import tqdm


def filter_and_save_direct(
        input_file,
        min_follows=1,
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

    # Create output file name if not provided
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_filtered_{min_follows}avg.parquet"

    print(f"Output will be saved to: {output_file}")

    # SINGLE EFFICIENT QUERY: Process and save in one go
    # This avoids creating intermediate dataframes or temp tables

    query = f"""
   
        SELECT DISTINCT subject_collection
        FROM read_parquet('{input_file}')
        
    """

    # Execute the query - this writes directly to disk
    result=conn.execute(query).fetchdf()

    elapsed_time = time.time() - start_time

    print("PROCESSING COMPLETE")
    print(f"Total processing time: {elapsed_time:.2f} seconds")
    print(f"Output file: {output_file}")
    conn.close()
    print(result)
    print(result["subject_collection"].dtypes)
    return output_file


def main():
    """Example usage"""

    # Input file path
    input_file = "likesFinal.parquet"  # Update this path

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
        min_follows=1,
        output_file='followsFilteredFinal6.parquet',
    )


if __name__ == '__main__':
    main()