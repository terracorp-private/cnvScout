import pandas as pd
import numpy as np


# preprocessing and dimensionality reduction
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
import pywt
from umap import UMAP


# visualization
import matplotlib.pyplot as plt
import plotly.express as px


AMPLITUDE_THRESHOLD = 0.06


df = pd.read_csv("/home/alpha/programs/python_files/datasets/cnv_and_mut/entities_transformed.csv")

# basic filtering. Rename Unnamded 0 with ID. Dropp chromosomes Y and X
# df = df.dropna(axis=1)
# df = df.fillna(0)
# df = df.rename(columns={"Unnamed: 0": "ID"})
df = df[df.columns.drop(list(df.filter(regex='[YX]')))]

print(df.head())
# Make it amplitude agnostic (experimental) 
def stupid_custom_filter(df=df,AMPLITUDE_THRESHOLD=AMPLITUDE_THRESHOLD):
    # temporary drop non digit columns
    helper_df = df[["entity","ID"]]
    df = df.drop(columns=["entity","ID"])
    # standardize and normalize data
    df = (df-df.mean())/df.std()
    df = 2*((df-df.min())/(df.max()-df.min()))-1
    # apply the filter
    df[df < -AMPLITUDE_THRESHOLD] = -1
    df[df > AMPLITUDE_THRESHOLD] = 1
    df[(df <= AMPLITUDE_THRESHOLD) & (df >= -AMPLITUDE_THRESHOLD)] = 0
    # append the dropped columns on the filtered dataframe
    df["ID"] = helper_df["ID"]
    df["entity"] = helper_df["entity"]
    
    return df

# df = stupid_custom_filter()

# Make features
features = df.columns.tolist()
features.remove("entity")
features.remove("ID")

print(df.head())



PRINCIPAL_COMPONENTS = 5

# make targets
x = df.loc[:,features].values
y_entity = df.loc[:,"entity"].values
y_id = df.loc[:,"ID"].values


# test transform and preprocessing methods
def custom_preprocess(method=1,x=x):
    if method == 2:
        scaler = MinMaxScaler()
    elif method == 3:
        scaler = RobustScaler(quantile_range=(0.2,0.8))
    elif method == 4:
        scaler = QuantileTransformer(n_quantiles=10, random_state=0, output_distribution="normal")
    elif method == 5:
        scaler = Normalizer()
    else:
        print("using default StandardScaler")
        scaler = StandardScaler()
    
    x = scaler.fit_transform(x)
    # x = Normalizer(norm="max").fit_transform(x)
    return x
    
method = int(input("Scaler to use (default StandardSclaer) : \n 1.StandardScaler \n 2.MinMaxScaler \n 3.RobustScaler \n 4.QuantileTransformer \n 5. Normalizer \n"))
x = custom_preprocess(method,x)


# PCA
pca_denoize = PCA(n_components=PRINCIPAL_COMPONENTS)
denoize = pca_denoize.fit_transform(x)
# print components which contribute to variance the most
variance = pca_denoize.explained_variance_ratio_
noise = pca_denoize.noise_variance_
print(variance, noise)

plt.figure(figsize=[14,6])
plt.bar(range(variance.shape[0]),variance)
plt.xlabel('PCA features')
plt.ylabel('variance %')


N_NEIGHBORS = 6

umap_2d = UMAP(n_neighbors=N_NEIGHBORS,n_epochs=500,random_state=1,spread=3,min_dist=0.5)
umap_2d.fit(denoize)

projections = umap_2d.transform(denoize)

fig = px.scatter(
    projections, x=0, y=1,
    title= f'PCA components = {PRINCIPAL_COMPONENTS}, n_neighbors = {N_NEIGHBORS}, n_cases = {df.shape[0]}, fold_change_threshold = {AMPLITUDE_THRESHOLD}' ,
    color=y_entity.astype(str), labels={'color': 'entity'},
    opacity=1
)

fig.update_layout(width=1000, height=600)

fig.show()




# SETTINGS FOR .BIN.IGV


# import pandas as pd
# import numpy as np

# import plotly.express as px
# from umap import UMAP
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA


# df = pd.read_csv("/home/alpha/programs/python_files/datasets/cnv_and_mut/entities.csv")

# # some samples have more columns, filter them out and drop all samples from 450k. Usually theier ID begins with 9 or 3
# df = df.dropna(axis=1)
# # filter = df["Unnamed: 0"].str.contains(r'(^9|^3|^100|^201|^101|^200|^8)')
# # df = df[~filter]

# # drop xy chromosomes and make features
# df = df[df.columns.drop(list(df.filter(regex='[YX]')))]
# features = df.columns.tolist()
# features.remove("entity")
# features.remove("Unnamed: 0")

# # make targets and scale the data
# x = df.loc[:,features].values
# y_entity = df.loc[:,"entity"].values
# y_id = df.loc[:,"Unnamed: 0"].values
# x = StandardScaler().fit_transform(x)


# pca_denoize = PCA(n_components=5)
# denoize = pca_denoize.fit_transform(x)
# print(denoize.shape)

# umap_2d = UMAP(n_neighbors=7,n_epochs=5000,random_state=1,spread=3)
# umap_2d.fit(denoize)

# projections = umap_2d.transform(denoize)

# fig = px.scatter(
#     projections, x=0, y=1,
#     color=y_entity.astype(str), labels={'color': 'entity'},
#     opacity=0.9
# )
# fig.show()

