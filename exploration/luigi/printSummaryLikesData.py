import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def main():
    file_name = "likesFinal.parquet"

    query = """

            SELECT DISTINCT did_id, COUNT(*) AS likesPerWeek, 
            FROM read_parquet({file_name})
            GROUP BY did_id

        """
    query = query.format(file_name=file_name)
    user_like_counts = duckdb.query(query).fetchdf()

    print


if __name__ == '__main__':
    main()