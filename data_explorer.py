#!/usr/bin/env python3

# system
import sys

# core
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Sklearn & UMAP
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from umap import UMAP


def data_integrity():
    """Check for missing or duplicated data."""
    path_to_data = sys.argv[1]
    data = pd.read_csv(path_to_data)

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


def var_filter(features, normalization_method, plot):
    """Filter data based on highest variance."""
    # Standardize features
    if normalization_method == "norm":
        normalized_features=(features-features.min())/(features.max()-features.min())
    elif normalization_method == "std":
        normalized_features = (features-features.mean())/features.std()
    else:
        features

    if plot is True:
        # Probes variance
        probes_variance = normalized_features.var().sort_values()
        probes_variance = probes_variance.to_frame(name="values")
        probes_variance["chrom"] = probes_variance.index.str.split("_").str[0]

        sns.boxplot(data=probes_variance,
                    x="chrom",
                    y="values",
                    log_scale=True,
                    )
        plt.show()
    else:
        return normalized_features


def multicollinearity_cleaner(data, features):
    """Identify and remove multicollinearity."""
    sns.heatmap(data.corr(method='spearman'))
    plt.show()
    print(data.corr())


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


targets = data_integrity()[0]
data = data_integrity()[1]

normalized_features = var_filter(data, "std", False)
# data_analyzer(data, targets)

# for i in range(3, 16, 1):
pca_data = PCA_reduction(targets, normalized_features, 11, "PC1", "PC2", plot=False)
UMAP_reduction(targets, pca_data, neighbours=9)
