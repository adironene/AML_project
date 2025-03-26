import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler

file_path = 'cancer.csv'
df = pd.read_csv(file_path)

print("data samples...")
print(df.head())

print("\n Null Values")
print(df.isnull().sum())

df.columns = df.columns.str.strip()
print(df.columns)

print("handling missing data")
df = df.dropna(subset=['County'])

numerical_cols = df.select_dtypes(include=[np.number]).columns
for col in numerical_cols:
    df[col].fillna(df[col].mean(), inplace=True)

categorical_cols = df.select_dtypes(include=[object]).columns
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

print("data samples...")
print(df.head())

print("working on data type conversion")
df['Age-Adjusted Incidence Rate'] = pd.to_numeric(df['Age-Adjusted Incidence Rate([rate note]) - cases per 100,000'], errors='coerce')

print("working on detecting outliers using z-scores")
df['Z-Score'] = zscore(df['Age-Adjusted Incidence Rate'])
# df = df[df['Z-Score'].abs() <= 3] 

print('scaling data')
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print('numerical columns', numerical_columns)
scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

print(df.info())
print(df.head())

cleaned_file_path = 'cleaned_cancer_incidence_data.csv'
df.to_csv(cleaned_file_path, index=False)
