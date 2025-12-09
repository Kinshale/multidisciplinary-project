import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def main():
    input_file = "likesFinal.parquet"

    query = """
        
           WITH user_weekly_stats AS (
    SELECT 
        did_id,
        DATE_TRUNC('week', created_date) as week_start,
        COUNT(*) as weekly_likes
    FROM read_parquet('{input_file}')
    GROUP BY did_id, week_start
    )
    SELECT 
        did_id,
        AVG(weekly_likes) as avg_weekly_likes
    FROM user_weekly_stats
    GROUP BY did_id
        
        """
    query = query.format(input_file=input_file)
    user_like_counts = duckdb.query(query).fetchdf()

    # Create a 2x2 plot to understand the distribution better
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Original histogram
    ax1 = axes[0, 0]
    data = user_like_counts['avg_weekly_likes'].values
    n, bins, patches = ax1.hist(data, bins=30, density=True,
                                alpha=0.6, color='lightblue',
                                edgecolor='black')
    mu, sigma = stats.norm.fit(data)
    x = np.linspace(min(data), max(data), 1000)
    p = stats.norm.pdf(x, mu, sigma)
    ax1.plot(x, p, 'r-', linewidth=2, label=f'Gaussian Fit')
    ax1.set_title('Original Scale', fontsize=12)
    ax1.set_xlabel('Likes Per Week')
    ax1.set_ylabel('Density')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Log-transformed histogram
    ax2 = axes[0, 1]
    log_data = np.log1p(data)  # log(1 + x) to handle zeros
    n, bins, patches = ax2.hist(log_data, bins=30, density=True,
                                alpha=0.6, color='lightgreen',
                                edgecolor='black')
    mu_log, sigma_log = stats.norm.fit(log_data)
    x_log = np.linspace(min(log_data), max(log_data), 1000)
    p_log = stats.norm.pdf(x_log, mu_log, sigma_log)
    ax2.plot(x_log, p_log, 'r-', linewidth=2, label=f'Gaussian Fit')
    ax2.set_title('Log Scale (log(1 + x))', fontsize=12)
    ax2.set_xlabel('log(1 + Likes Per Week)')
    ax2.set_ylabel('Density')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Box plot
    ax3 = axes[1, 0]
    ax3.boxplot(data, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue'))
    ax3.set_title('Box Plot of Likes Per Week', fontsize=12)
    ax3.set_ylabel('Likes Per Week')
    ax3.grid(True, alpha=0.3)

    # 4. Cumulative distribution
    ax4 = axes[1, 1]
    sorted_data = np.sort(data)
    y_vals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    ax4.plot(sorted_data, y_vals, 'b-', linewidth=2)
    ax4.set_title('Cumulative Distribution Function', fontsize=12)
    ax4.set_xlabel('Likes Per Week')
    ax4.set_ylabel('Cumulative Probability')
    ax4.grid(True, alpha=0.3)

    plt.suptitle('Analysis of User Likes Per Week Distribution', fontsize=16)
    plt.tight_layout()
    plt.show()

    # Check skewness
    from scipy.stats import skew
    skewness = skew(data)
    print(f"\n=== Distribution Characteristics ===")
    print(f"Skewness: {skewness:.2f}")
    print(f"If |skewness| > 1, data is highly skewed (common for social media)")
    print(f"Most users likely have few likes, while a few have many (power-law)")
    # Step 4: Statistical summary
    print("\nStatistical Summary:")
    print(f"Number of unique users: {len(user_like_counts)}")
    print(f"Mean likes/posts per user: {mu:.2f}")
    print(f"Standard deviation: {sigma:.2f}")
    print(f"Median: {np.median(user_like_counts.values):.2f}")
    print(f"Min: {user_like_counts.min()}")
    print(f"Max: {user_like_counts.max()}")

if __name__ == '__main__':
    main()