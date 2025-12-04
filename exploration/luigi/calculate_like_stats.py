import duckdb
import glob
import os
import pandas as pd


def calculate_likes_stats_duckdb(chunk_dir, start_chunk=0, end_chunk=None):
    """Calculate statistics using DuckDB for maximum performance"""

    chunk_files = sorted(glob.glob(os.path.join(chunk_dir, 'chunk_*.parquet')))

    if end_chunk is not None:
        chunk_files = chunk_files[start_chunk:end_chunk + 1]

    print(f"Processing {len(chunk_files)} chunks with DuckDB")

    # Create a temporary view with all chunks
    conn = duckdb.connect()

    # Register all parquet files
    union_parts = []
    for i, file in enumerate(chunk_files):
        union_parts.append(f"SELECT did_id FROM read_parquet('{file}')")

    union_query = " UNION ALL ".join(union_parts)

    # Calculate all statistics in ONE query
    query = f"""
    WITH all_likes AS (
        {union_query}
    ),
    user_stats AS (
        SELECT 
            did_id,
            COUNT(*) as total_likes,
            COUNT(*) / {len(chunk_files)}.0 as mean_likes_per_chunk
        FROM all_likes
        GROUP BY did_id
    ),
    stats_with_stddev AS (
        SELECT 
            did_id,
            total_likes,
            mean_likes_per_chunk,
            SQRT((total_likes - mean_likes_per_chunk) * (total_likes - mean_likes_per_chunk)) as std_dev_likes_per_chunk
        FROM user_stats
    ),
    overall_stats AS (
        SELECT 
            COUNT(DISTINCT did_id) as total_users,
            AVG(total_likes) as overall_avg_likes_per_user,
            STDDEV_SAMP(total_likes) as overall_std_likes_per_user
        FROM user_stats
    )
    SELECT 
        s.*,
        o.total_users,
        o.overall_avg_likes_per_user,
        o.overall_std_likes_per_user
    FROM stats_with_stddev s
    CROSS JOIN overall_stats o
    """

    stats_df = conn.execute(query).df()

    # Extract overall stats from the first row
    first_row = stats_df.iloc[0]
    overall_stats_dict = {
        'total_users': first_row['total_users'],
        'overall_avg_likes_per_user': first_row['overall_avg_likes_per_user'],
        'overall_std_likes_per_user': first_row['overall_std_likes_per_user']
    }

    # Remove the overall stats columns from the individual user stats
    stats_df = stats_df[['did_id', 'total_likes', 'mean_likes_per_chunk', 'std_dev_likes_per_chunk']]

    conn.close()

    return stats_df, overall_stats_dict


def calculate_weekly_likes_stats_with_users(chunk_dir, start_chunk=0, end_chunk=None):
    """Calculate weekly likes statistics including individual user data"""

    chunk_files = sorted(glob.glob(os.path.join(chunk_dir, 'chunk_*.parquet')))

    if end_chunk is not None:
        chunk_files = chunk_files[start_chunk:end_chunk + 1]

    print(f"Processing {len(chunk_files)} chunks for weekly stats with user details")

    conn = duckdb.connect()

    # Register all parquet files
    union_parts = []
    for file in chunk_files:
        union_parts.append(f"SELECT did_id, created_at FROM read_parquet('{file}')")

    union_query = " UNION ALL ".join(union_parts)
    conn.execute(f"CREATE OR REPLACE TEMPORARY VIEW all_likes AS {union_query}")

    # Option 1: Get weekly stats with individual user breakdown
    weekly_query_with_users = """
    WITH likes_with_week AS (
        SELECT 
            did_id,
            created_at,
            DATE_TRUNC('week', created_at::TIMESTAMP) as week_start,
            EXTRACT(WEEK FROM created_at::TIMESTAMP) as week_number,
            EXTRACT(YEAR FROM created_at::TIMESTAMP) as year
        FROM all_likes
        WHERE created_at IS NOT NULL
    ),
    weekly_user_counts AS (
        SELECT 
            did_id,
            year,
            week_number,
            week_start,
            COUNT(*) as weekly_likes
        FROM likes_with_week
        GROUP BY did_id, year, week_number, week_start
    ),
    weekly_aggregates AS (
        SELECT 
            week_start,
            year,
            week_number,
            COUNT(DISTINCT did_id) as active_users,
            SUM(weekly_likes) as total_likes,
            AVG(weekly_likes) as avg_likes_per_user,
            STDDEV_SAMP(weekly_likes) as std_likes_per_user,
            MIN(weekly_likes) as min_likes_per_user,
            MAX(weekly_likes) as max_likes_per_user,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_likes) as median_likes_per_user
        FROM weekly_user_counts
        GROUP BY week_start, year, week_number
    )
    SELECT 
        w.*,
        u.did_id,
        u.weekly_likes as user_weekly_likes
    FROM weekly_aggregates w
    CROSS JOIN weekly_user_counts u
    WHERE w.week_start = u.week_start
    ORDER BY w.week_start, u.weekly_likes DESC
    """

    weekly_stats_with_users_df = conn.execute(weekly_query_with_users).df()

    # Option 2: Get separate dataframes for aggregated stats and user details
    weekly_aggregates_query = """
    WITH weekly_user_counts AS (
        SELECT 
            DATE_TRUNC('week', created_at::TIMESTAMP) as week_start,
            EXTRACT(WEEK FROM created_at::TIMESTAMP) as week_number,
            EXTRACT(YEAR FROM created_at::TIMESTAMP) as year,
            did_id,
            COUNT(*) as weekly_likes
        FROM all_likes
        WHERE created_at IS NOT NULL
        GROUP BY week_start, week_number, year, did_id
    )
    SELECT 
        week_start,
        year,
        week_number,
        COUNT(DISTINCT did_id) as active_users,
        SUM(weekly_likes) as total_likes,
        AVG(weekly_likes) as avg_likes_per_user,
        STDDEV_SAMP(weekly_likes) as std_likes_per_user,
        MIN(weekly_likes) as min_likes_per_user,
        MAX(weekly_likes) as max_likes_per_user,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_likes) as median_likes_per_user
    FROM weekly_user_counts
    GROUP BY week_start, year, week_number
    ORDER BY week_start
    """

    weekly_aggregates_df = conn.execute(weekly_aggregates_query).df()

    # User-level weekly data
    user_weekly_query = """
    SELECT 
        DATE_TRUNC('week', created_at::TIMESTAMP) as week_start,
        EXTRACT(WEEK FROM created_at::TIMESTAMP) as week_number,
        EXTRACT(YEAR FROM created_at::TIMESTAMP) as year,
        did_id,
        COUNT(*) as weekly_likes
    FROM all_likes
    WHERE created_at IS NOT NULL
    GROUP BY week_start, week_number, year, did_id
    ORDER BY week_start, weekly_likes DESC
    """

    user_weekly_df = conn.execute(user_weekly_query).df()

    # Overall statistics
    overall_weekly_query = """
    WITH weekly_counts AS (
        SELECT 
            DATE_TRUNC('week', created_at::TIMESTAMP) as week_start,
            did_id,
            COUNT(*) as weekly_likes
        FROM all_likes
        WHERE created_at IS NOT NULL
        GROUP BY week_start, did_id
    )
    SELECT 
        AVG(weekly_likes) as overall_avg_weekly_likes,
        STDDEV_SAMP(weekly_likes) as overall_std_weekly_likes,
        MIN(weekly_likes) as overall_min_weekly_likes,
        MAX(weekly_likes) as overall_max_weekly_likes
    FROM weekly_counts
    """

    overall_weekly_stats = conn.execute(overall_weekly_query).fetchone()

    conn.close()

    overall_weekly_dict = {
        'overall_avg_weekly_likes': overall_weekly_stats[0] if overall_weekly_stats[0] is not None else 0,
        'overall_std_weekly_likes': overall_weekly_stats[1] if overall_weekly_stats[1] is not None else 0,
        'overall_min_weekly_likes': overall_weekly_stats[2] if overall_weekly_stats[2] is not None else 0,
        'overall_max_weekly_likes': overall_weekly_stats[3] if overall_weekly_stats[3] is not None else 0
    }

    return weekly_aggregates_df, user_weekly_df, overall_weekly_dict


def main():
    stats_df, overall_stats = calculate_likes_stats_duckdb('likesChunks', start_chunk=0, end_chunk=19)

    print(f"Overall Statistics:")
    print(f"Total users: {overall_stats['total_users']}")
    print(f"Average likes per user: {overall_stats['overall_avg_likes_per_user']:.2f}")
    print(f"Standard deviation: {overall_stats['overall_std_likes_per_user']:.2f}")
    print(f"\nFirst few users:")
    print(stats_df.head(10))

    weekly_agg, user_weekly, overall_weekly = calculate_weekly_likes_stats_with_users('likesChunks', start_chunk=0,
                                                                                      end_chunk=19)

    # Set display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print("Weekly Aggregated Statistics:")
    print("=" * 80)
    print(weekly_agg.head(10))

    print("\nUser-Level Weekly Data (first 20 rows):")
    print("=" * 80)
    print(user_weekly.head(20))

    print(f"\nOverall Weekly Statistics:")
    print(f"Average weekly likes per user: {overall_weekly['overall_avg_weekly_likes']:.2f}")
    print(f"Standard deviation: {overall_weekly['overall_std_weekly_likes']:.2f}")
    print(f"Min weekly likes per user: {overall_weekly['overall_min_weekly_likes']}")
    print(f"Max weekly likes per user: {overall_weekly['overall_max_weekly_likes']}")

if __name__ == '__main__':
    main()