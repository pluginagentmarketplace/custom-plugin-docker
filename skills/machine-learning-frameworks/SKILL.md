---
name: machine-learning-frameworks
description: Master scikit-learn, XGBoost, and traditional machine learning for classification, regression, and clustering problems.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# Machine Learning Frameworks

Building ML models with Python.

## Scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
```

## XGBoost

```python
import xgboost as xgb

model = xgb.XGBClassifier(max_depth=6, learning_rate=0.1)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

## Key Topics

- Supervised learning
- Unsupervised learning
- Feature engineering
- Model evaluation
- Hyperparameter tuning
- Ensemble methods
