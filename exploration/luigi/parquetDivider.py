import pyarrow.parquet as pq
import pyarrow as pa
import os

def split_parquet_pyarrow(input_file, output_dir, rows_per_file=10000):
    """Split parquet file using PyArrow (memory efficient)"""
    os.makedirs(output_dir, exist_ok=True)

    parquet_file = pq.ParquetFile(input_file)
    total_rows = parquet_file.metadata.num_rows

    chunk_num = 0
    for batch in parquet_file.iter_batches(batch_size=rows_per_file):
        table = pa.Table.from_batches([batch])
        output_file = os.path.join(output_dir, f'chunk_{chunk_num}.parquet')

        pq.write_table(table, output_file)
        print(f"Created {output_file} with {batch.num_rows} rows")
        chunk_num += 1
        break

def main():
    # Usage
    split_parquet_pyarrow('likes.parquet', 'output_arrow', rows_per_file=20000000)

if __name__ == "__main__":
    main()