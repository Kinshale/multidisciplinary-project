import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def main():
    # Load the parquet file
    df = pd.read_parquet('likesFilteredChunks/chunk_0_filtered_30avg.parquet')
    # Count interactions per user and sort by count (descending)
    interactions_per_user = df['did_id'].value_counts()

    # Plot users ordered by interaction count
    plt.figure(figsize=(15, 6))
    plt.semilogy(range(len(interactions_per_user)), interactions_per_user.values,
                 linewidth=1)
    plt.title('Users Ordered by Number of Interactions (Log Scale)')
    plt.xlabel('User Rank (ordered by interaction count)')
    plt.ylabel('Number of Interactions (log scale)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()