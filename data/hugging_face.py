# NOTE: Some tester code for uploading a dataset to hugging face. 

import pandas as pd
import os
from huggingface_hub import HfApi

os.environ["HF_TOKEN"] = "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"  # ← REPLACE THIS

# Create dummy dataset
dummy_data = pd.DataFrame({
    'id': [1, 2],
    'text': ['This is a test sample for AI training', 'Another example text for model training'],
    'label': [0, 1],
    'created_at': ['2024-01-15', '2024-01-16']
})

# Save locally
os.makedirs('data/test_dataset', exist_ok=True)
dummy_data.to_parquet('data/test_dataset/data.parquet')
dummy_data.to_csv('data/test_dataset/data.csv', index=False)

# Create dataset card
with open('data/test_dataset/README.md', 'w') as f:
    f.write("""---
language: en
task_categories:
- text-classification
- text-generation
pretty_name: Test Multidisciplinary Dataset
---

# Test Dataset

Small test dataset for Hugging Face integration testing.

## Dataset Structure

- **text**: Sample text data
- **label**: Binary labels (0/1)
- **created_at**: Timestamp
""")

# Upload to Hugging Face
api = HfApi(token=os.getenv("HF_TOKEN"))
api.upload_folder(
    folder_path="data/test_dataset",
    repo_id="Kinshale/multidisciplinary-project",
    repo_type="dataset",
)

print("Dataset uploaded! Test retrieval with:")
print("from datasets import load_dataset")
print('dataset = load_dataset("Kinshale/multidisciplinary-project")')

## For retrieving 
from datasets import load_dataset

dataset = load_dataset("Kinshale/multidisciplinary-project")
print(dataset['train'][:])  # Shows your 2 rows 
