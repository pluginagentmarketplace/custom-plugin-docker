---
name: ml-data-engineering
description: Build machine learning models and data pipelines with Python, TensorFlow, PyTorch, and Spark. Learn model training, feature engineering, deployment, and MLOps. Use when working on AI/ML or data engineering tasks.
---

# ML & Data Engineering

Build intelligent systems powered by machine learning and data.

## Quick Start

### Machine Learning with Scikit-learn
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Load data
df = pd.read_csv('data.csv')
X = df.drop('target', axis=1)
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))
```

### Deep Learning with PyTorch
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x

# Initialize
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuralNetwork().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(10):
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        # Forward pass
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### Data Pipeline with Pandas
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('raw_data.csv')

# Data cleaning
df = df.drop_duplicates()
df = df.dropna()

# Feature engineering
df['feature1'] = df['col1'] * df['col2']
df['feature2'] = df['col3'].astype('category').cat.codes

# Normalization
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[['feature1', 'feature2']] = scaler.fit_transform(
    df[['feature1', 'feature2']]
)

# Save processed data
df.to_csv('processed_data.csv', index=False)
```

### MLOps with MLflow
```python
import mlflow
from mlflow.models import infer_signature

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("max_depth", 5)

    # Train model
    model = RandomForestClassifier(max_depth=5)
    model.fit(X_train, y_train)

    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # Log model
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(model, "model", signature=signature)
```

## Key Concepts

### Machine Learning
- **Supervised learning**: Classification, regression
- **Unsupervised learning**: Clustering, dimensionality reduction
- **Feature engineering**: Creating meaningful features
- **Model evaluation**: Cross-validation, metrics, overfitting

### Deep Learning
- **Neural networks**: Layers, activation functions, backpropagation
- **CNN**: Convolutional layers for image processing
- **RNN**: Sequential data, LSTM, GRU
- **Transformers**: Attention mechanisms, self-attention

### Data Engineering
- **ETL pipelines**: Extract, transform, load
- **Data warehousing**: Structured data storage
- **Big data**: Spark, distributed computing
- **Real-time streaming**: Kafka, event processing

### MLOps
- **Model versioning**: Track model versions and data
- **Experiment tracking**: Compare model performances
- **Model serving**: Deploy models to production
- **Monitoring**: Track model performance degradation

## Common Patterns

### Feature Engineering Pipeline
```python
class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder()

    def fit_transform(self, X):
        X_scaled = self.scaler.fit_transform(X[numeric_cols])
        X_encoded = self.encoder.fit_transform(X[categorical_cols])
        return np.concatenate([X_scaled, X_encoded], axis=1)

    def transform(self, X):
        X_scaled = self.scaler.transform(X[numeric_cols])
        X_encoded = self.encoder.transform(X[categorical_cols])
        return np.concatenate([X_scaled, X_encoded], axis=1)
```

### Model Validation
```python
from sklearn.model_selection import cross_validate

scores = cross_validate(
    model, X, y, cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1']
)

print(f"Accuracy: {scores['test_accuracy'].mean():.3f}")
print(f"Precision: {scores['test_precision'].mean():.3f}")
print(f"Recall: {scores['test_recall'].mean():.3f}")
```

## Best Practices

1. **Start simple** - Simple models before complex ones
2. **Clean data** - Garbage in, garbage out
3. **Feature engineering** - Domain knowledge matters
4. **Cross-validation** - Proper evaluation
5. **Monitor drift** - Track data and model performance
6. **Version everything** - Data, models, code
7. **Document experiments** - Track what you tried
8. **Reproducibility** - Set random seeds

## Tools & Libraries

**ML Frameworks**: scikit-learn, TensorFlow, PyTorch, XGBoost
**Data Processing**: Pandas, NumPy, Polars, Apache Spark
**MLOps**: MLflow, Kubeflow, Weights & Biases, Determined
**Data Pipeline**: Airflow, Prefect, dbt, Kafka
**Visualization**: Matplotlib, Seaborn, Plotly, Tensorboard
