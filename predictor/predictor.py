#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from umap import UMAP

DATA_PATH = sys.argv[1]


def PCA_reduction(features,
                  data,
                  components_number,
                  first_component,
                  second_component,
                  plot):
    # TODO work on PCA_explained_variance

    # std_scaler = StandardScaler()
    # X = pd.DataFrame(std_scaler.fit_transform(data), columns=data.columns)

    pca = PCA(n_components=components_number, whiten=True)
    X_pca = pca.fit_transform(data)
    principal_df = pd.DataFrame(data=X_pca)

    if plot is True:
        # Scatterplot
        plt.scatter(principal_df[first_component], principal_df[second_component], s=20)

        # Aesthetics
        plt.title('PCA plot in 2D')
        plt.xlabel(first_component)
        plt.ylabel(second_component)
        plt.show()

    return principal_df


def UMAP_reduction(targets, X, neighbours):
    """Perform dimentionality reduction and plot the result."""
    u = UMAP(n_neighbors=neighbours,
             min_dist=0.05,
             random_state=42)
    umap_proj = u.fit_transform(X)

    # Convert to data frame
    umap_df = pd.DataFrame(data=umap_proj, columns=['X', 'Y'])
    x = umap_df.iloc[:, 0]
    y = umap_df.iloc[:, 1]

    # Scatterplot
    fig = px.scatter(
        umap_df, x=x, y=y,
        color=targets["Diagnose"]
    )
    fig.show()


targets = pd.read_csv(DATA_PATH+"targets.csv")
features = pd.read_csv(DATA_PATH+"cropped_features.csv")

pca_data = PCA_reduction(targets, features, 12, "PC1", "PC2", plot=False)
UMAP_reduction(targets, pca_data, neighbours=6)

# print(features)
# print(targets)
