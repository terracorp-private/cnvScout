#!/usr/bin/env python3

# system
import sys

# core
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Sklearn & UMAP
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap


def data_integrity():
    '''The function checks input data integrity. If the data is acceptable for further analysis it will return
    the data itself. If not it will raise an error.'''

    path_to_data = sys.argv[1]
    data = pd.read_csv(path_to_data)

    missing_values = data.isna().sum().sum()
    duplicated_values = data.duplicated().sum()

    if missing_values != 0:
        raise Exception(f"Data contatins missing {missing_values}")

    if duplicated_values != 0:
        raise Exception(f"Data contatins duplicates {duplicated_values}")

    print(data["Diagnose"], data.iloc[:,1:-1])

    return data["Diagnose"], data.iloc[:,1:-1]


def PCA_reduction(features, data, components_number, first_component, second_component, plot):

    # TODO work on PCA_explained_variance

    std_scaler = StandardScaler()
    X = pd.DataFrame(std_scaler.fit_transform(data), columns=data.columns)

    pca = PCA(n_components=components_number)
    X_pca = pca.fit_transform(X)
    principal_df = pd.DataFrame(data = X_pca)

    if plot == True:
        # Scatterplot
        # plt.scatter(principal_df.iloc[:,0], principal_df.iloc[:,1], s=20)
        plt.scatter(principal_df[first_component], principal_df[second_component], s=20)

        # Aesthetics
        plt.title('PCA plot in 2D')
        plt.xlabel(first_component)
        plt.ylabel(second_component)
        plt.show()

    return principal_df

def UMAP_reduction(data):

    # Scaler
    std_scaler = StandardScaler()
    X = pd.DataFrame(std_scaler.fit_transform(data), columns=data.columns)

    # UMAP
    u = umap.UMAP(n_neighbors=5, random_state=42)
    X_fit = u.fit(X)
    X_umap = u.transform(X)

    # Convert to data frame
    umap_df = pd.DataFrame(data = X_umap, columns = ['umap comp. 1', 'umap comp. 2'])
    x = umap_df.iloc[:,0]
    y = umap_df.iloc[:,1]

    # Scatterplot
    fig = px.scatter(
        umap_df, x=x, y=y,
        color=features
    )
    fig.show()



features = data_integrity()[0]
data = data_integrity()[1]

# PCA_reduction(features, data, 3, "PC1", "PC2")
pca_data = PCA_reduction(features, data, 9, "PC1", "PC2", plot=False)
UMAP_reduction(pca_data)
