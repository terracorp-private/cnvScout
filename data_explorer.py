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
import umap


def data_integrity():
    '''The function checks input data integrity. If the data is acceptable for further analysis it will return
    the data itself. If not it will raise an error.'''

    path_to_data = sys.argv[1]
    data = pd.read_csv(path_to_data)

    # TODO why naaaa?
    # data = data.dropna(axis=1)

    # missing_values_sum = data.isna().sum().sum()
    # missing_values = data.isna().sum()
    # duplicated_values = data.duplicated().sum()

    # if missing_values_sum != 0:
    #     raise Exception(f"Following data is missing {missing_values}")

    # if duplicated_values != 0:
    #     raise Exception(f"Data contatins duplicates {duplicated_values}")

    target_names = ["sample", "Diagnose"]
    targets = data[target_names]
    features = data.drop(target_names, axis=1)

    return targets, features


def var_filter(features):

    features = (features-features.mean())/features.std()

    features_names = features.columns.str.split("_").str[0]
    features_frequency = features_names.value_counts()
    print(features_frequency)
    # print(features.var().sort_values())
    # print(features.var().index)
    # features = features.std().sort_values()
    # features = features.reset_index()
    # print(features)
    # features["chrom"] = features["index"].str.split("_").str[0]
    # print(features)
    # print(features["chrom"].value_counts())

    # sns.boxplot(data=features, x="chrom", y=0, log_scale=True)
    # plt.show()


def data_analyzer(data, features):
    """Do analyze the data. Find most imp. features"""

    sns.heatmap(data.corr(method='spearman'))
    plt.show()
    print(data.corr())


def rudimental_clean(data):

    probes_std = data.std().sort_values(ascending=False)

    # TODO make a not-guesstimating method for threshold of feature selection. I.e. first derivative.
    probes_std_selected = probes_std[probes_std < 0.9]
    probes_names_to_drop = list(probes_std_selected.index)

    data = data.drop(columns=probes_names_to_drop)

    print(data.shape)

    return data


def PCA_reduction(features,
                  data,
                  components_number,
                  first_component,
                  second_component,
                  plot):
    # TODO work on PCA_explained_variance

    std_scaler = StandardScaler()
    X = pd.DataFrame(std_scaler.fit_transform(data), columns=data.columns)

    pca = PCA(n_components=components_number, whiten=True)
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

    X = data

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
        color=targets
    )
    fig.show()


targets = data_integrity()[0]
data = data_integrity()[1]

print(targets, data, sep="\n")

var_filter(data)
# data_analyzer(data, targets)
# precleaned_data = rudimental_clean(data)
# pca_data = PCA_reduction(targets, precleaned_data, 2, "PC1", "PC2", plot=False)
# UMAP_reduction(pca_data)
