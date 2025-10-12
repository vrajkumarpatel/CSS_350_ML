import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.datasets import StandardDataset
from aif360.algorithms.preprocessing import Reweighing

# Load dataset
df = pd.read_csv("adult.csv")
# Basic preprocessing, note that column names may need to be adjusted depending on
# the datset's structure. 
df = pd.get_dummies(df, columns=["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex"], drop_first=True)
df['income'] = df['income'].apply(lambda x: 1 if x == ">50K" else 0)

# Train/test split
X = df.drop("income", axis=1)
y = df["income"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Calculate fairness metrics (e.g., demographic parity, equalized odds)
# Example of reweighting (mitigation technique)
# Use AIF360 library to define dataset and apply reweighing

dataset = StandardDataset(df, label_name="income", favorable_classes=[1], protected_attribute_names=["sex"], privileged_classes=[[1]])
RW = Reweighing(unprivileged_groups=[{'sex': 0}], privileged_groups=[{'sex': 1}])
dataset_transf = RW.fit_transform(dataset)

# Re-train and evaluate fairness again with the reweighted dataset
# Complete with ClassificationMetric from AIF360 for fairness assessment
