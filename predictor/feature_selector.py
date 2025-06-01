#!/usr/bin/env python3

import sys
import pandas as pd

DATA_PATH = sys.argv[1]


def data_integrity(DATA_PATH):
    """Check for missing or duplicated data."""
    data = pd.read_csv(DATA_PATH + "raw_datamatrix.csv")
    missing_values_sum = data.isna().sum().sum()
    missing_values = data.isna().sum()
    duplicated_values = data.duplicated().sum()

    if missing_values_sum != 0:
        raise Exception(f"Following data is missing {missing_values}")

    if duplicated_values != 0:
        raise Exception(f"Data contatins duplicates {duplicated_values}")

    target_names = ["sample", "Diagnose"]
    targets = data[target_names]
    features = data.drop(target_names, axis=1)

    return targets, features


def data_standardization(features, std_method):
    """Apply one of the standardization method and return dataset."""
    if std_method == "norm":
        normalized_features=(features-features.min())/(features.max()-features.min())
    elif std_method == "std":
        normalized_features = (features-features.mean())/features.std()
    else:
        normalized_features  # return unchanged dataset

    return normalized_features


def corr_matrix_builder(features, DATA_PATH, corr_threshold=0.95):
    """Build correlation matrix for each chromosome.

    Identify highly correlated features. Save them in a file.
    """
    cor_cols = set()
    for c in range(1, 23):
        chrom_corr_matrix = features.filter(regex=("chr"+str(c)+"_.*"), axis=1).corr().abs()
        for i in range(len(chrom_corr_matrix.columns)):
            for j in range(i):
                if abs(chrom_corr_matrix.iloc[i, j]) > corr_threshold:
                    cols = chrom_corr_matrix.columns[i]
                    cor_cols.add(cols)

    high_corr_features = list(cor_cols)
    with open(DATA_PATH+"features_with_high_correlation.txt", "w") as file:
        for item in high_corr_features:
            file.write(item+",")


def multicollinearity_cleaner(features, DATA_PATH):
    """Remove multicollinearity. Build and save correlation matix if does't exist."""
    highliy_correlated_features = DATA_PATH+"features_with_high_correlation.txt"
    cols_to_drop = pd.read_csv(highliy_correlated_features).columns
    # print(cols_to_drop)
    return features.drop(labels=cols_to_drop, axis=1)


targets = data_integrity(DATA_PATH)[0]
features = data_integrity(DATA_PATH)[1]

features_std = data_standardization(features, "std")
# corr_matrix_builder(features_std, DATA_PATH)
features_cropped = multicollinearity_cleaner(features_std, DATA_PATH)

targets.to_csv(DATA_PATH+"targets.csv", index=False)
features_cropped.to_csv(DATA_PATH+"cropped_features.csv", index=False)
