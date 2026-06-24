# pipeline/data_preprocessing.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Handle relative imports for both module and direct execution
try:
    from .config import DATA_PATH
except ImportError:
    # When running directly, construct the path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    dataset_path = os.path.join(parent_dir, 'dataset', 'kaggle_diabetes.csv')
    DATA_PATH = dataset_path

def load_and_preprocess(test_size=0.2, random_state=0):
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={'DiabetesPedigreeFunction': 'DPF'})

    cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[cols_with_zero] = df[cols_with_zero].replace(0, np.nan)

    df['Glucose'] = df['Glucose'].fillna(df['Glucose'].mean())
    df['BloodPressure'] = df['BloodPressure'].fillna(df['BloodPressure'].mean())
    df['SkinThickness'] = df['SkinThickness'].fillna(df['SkinThickness'].median())
    df['Insulin'] = df['Insulin'].fillna(df['Insulin'].median())
    df['BMI'] = df['BMI'].fillna(df['BMI'].median())

    X = df.drop(columns='Outcome')
    y = df['Outcome']

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def check_feature_correlation(test_size=0.2, random_state=0, plot=True):
    """
    Check the correlation of all features with the output feature (Outcome)
    
    Parameters:
    -----------
    test_size : float, default=0.2
        Proportion of dataset to include in the test split
    random_state : int, default=0
        Random state for reproducibility
    plot : bool, default=True
        Whether to display correlation heatmap
    
    Returns:
    --------
    pandas.Series : Correlation values of each feature with Outcome
    """
    # Load the data
    df = pd.read_csv(DATA_PATH)
    
    # Apply same preprocessing
    df = df.rename(columns={'DiabetesPedigreeFunction': 'DPF'})
    
    cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[cols_with_zero] = df[cols_with_zero].replace(0, np.nan)
    
    df['Glucose'] = df['Glucose'].fillna(df['Glucose'].mean())
    df['BloodPressure'] = df['BloodPressure'].fillna(df['BloodPressure'].mean())
    df['SkinThickness'] = df['SkinThickness'].fillna(df['SkinThickness'].median())
    df['Insulin'] = df['Insulin'].fillna(df['Insulin'].median())
    df['BMI'] = df['BMI'].fillna(df['BMI'].median())
    
    # Calculate correlation with Outcome
    correlation_with_outcome = df.corr()['Outcome'].sort_values(ascending=False)
    
    print("\n" + "="*50)
    print("FEATURE CORRELATION WITH OUTCOME")
    print("="*50)
    print(correlation_with_outcome)
    print("="*50 + "\n")
    
    # Plot correlation heatmap
    if plot:
        plt.figure(figsize=(10, 8))
        
        # Create correlation matrix
        correlation_matrix = df.corr()
        
        # Plot heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                    fmt='.2f', square=True, linewidths=1)
        plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Plot bar plot for feature-outcome correlation
        plt.figure(figsize=(10, 6))
        correlation_with_outcome[:-1].plot(kind='barh', color='steelblue')
        plt.xlabel('Correlation Coefficient', fontsize=12)
        plt.ylabel('Features', fontsize=12)
        plt.title('Correlation of Features with Outcome', fontsize=14, fontweight='bold')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        plt.show()
    
    return correlation_with_outcome


if __name__ == "__main__":
    print("Testing data preprocessing module...")
    print("\nChecking feature correlation with Outcome...")
    check_feature_correlation(plot=True)