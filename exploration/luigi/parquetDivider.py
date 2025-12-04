import pyarrow.parquet as pq
import pyarrow as pa
import os


def split_parquet_pyarrow(input_file, output_dir, rows_per_file=10000, start_chunk=0,end_chunk=None):
    """Split parquet file starting from specific chunk"""
    os.makedirs(output_dir, exist_ok=True)

    parquet_file = pq.ParquetFile(input_file)
    total_rows = parquet_file.metadata.num_rows

    chunk_num = 0
    rows_processed = 0

    for batch in parquet_file.iter_batches(batch_size=rows_per_file):
        # Skip chunks until we reach start_chunk
        if chunk_num < start_chunk:
            print(f"Skipping chunk {chunk_num}")
            chunk_num += 1
            rows_processed += batch.num_rows
            continue

        table = pa.Table.from_batches([batch])
        output_file = os.path.join(output_dir, f'chunk_{chunk_num}.parquet')

        pq.write_table(table, output_file)
        print(f"Created {output_file} with {batch.num_rows} rows")

        chunk_num += 1
        rows_processed += batch.num_rows

        # Progress reporting
        progress = (rows_processed / total_rows) * 100
        print(f"Progress: {progress:.1f}% ({rows_processed}/{total_rows} rows)")
        if(end_chunk is not None and chunk_num >= end_chunk):
            print(f"Ending chunk {chunk_num}")
            break


def main():
    # Start from chunk 50 (if you stopped at chunk 49)
    split_parquet_pyarrow('likes.parquet', 'likesChunks',
                          rows_per_file=20000000, start_chunk=20, end_chunk=40)

if __name__ == "__main__":
    main()
