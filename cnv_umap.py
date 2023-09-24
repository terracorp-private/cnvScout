import pandas as pd
import numpy as np

import plotly.express as px
from umap import UMAP
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


df = pd.read_csv("/home/alpha/programs/python_files/datasets/cnv_and_mut/entities.csv")

# some samples have more columns, filter them out and drop all samples from 450k. Usually theier ID begins with 9 or 3
df = df.dropna(axis=1)
# filter = df["Unnamed: 0"].str.contains(r'(^9|^3|^100|^201|^101|^200|^8)')
# df = df[~filter]

# drop xy chromosomes and make features
df = df[df.columns.drop(list(df.filter(regex='[YX]')))]
features = df.columns.tolist()
features.remove("entity")
features.remove("Unnamed: 0")

# make targets and scale the data
x = df.loc[:,features].values
y_entity = df.loc[:,"entity"].values
y_id = df.loc[:,"Unnamed: 0"].values
x = StandardScaler().fit_transform(x)


pca_denoize = PCA(n_components=5)
denoize = pca_denoize.fit_transform(x)
print(denoize.shape)

umap_2d = UMAP(n_neighbors=7,n_epochs=5000,random_state=1,spread=3)
umap_2d.fit(denoize)

projections = umap_2d.transform(denoize)

fig = px.scatter(
    projections, x=0, y=1,
    color=y_entity.astype(str), labels={'color': 'entity'},
    opacity=0.9
)
fig.show()


# # UMAP FOR SEGMENTS
#
# df = df[["entity","ID","chr","start","end","alteration","seg_mean","seg_median"]]
# df["ID"] = df["ID"].str.replace(r"[RC_]","",regex=True)
# df["methylation_class"] = df["entity"]
# df["methylation_class"] = df["methylation_class"].replace(df["methylation_class"].unique().tolist(),[0,1,2,3,4])
# df['id_numeric'] = df.reset_index().index
# df["alteration"] = df["alteration"].replace(["balanced"],0)
# df = df[df["alteration"] != 0]
# df["alteration"] = df["alteration"].replace(["loss"],1)
# df["alteration"] = df["alteration"].replace(["gain"],2)
# df["alteration"] = df["alteration"].replace(["chromothripsis"],3)
# df["length"] = df["end"] - df["start"]
# df["chr"] = df["chr"].astype("int")
# df = df.dropna()
# # df = df.drop_duplicates(subset=["ID"])
#
# features = ["id_numeric","ID","chr","alteration","start","end","length","seg_mean","methylation_class"]
#
# print(df.tail(10))
#
# x = df.loc[:,features].values
# y_entity = df.loc[:,"entity"].values
# y = df.loc[:,"chr"].values
# x = StandardScaler().fit_transform(x)
#
# print(len(y))
#
# umap_2d = UMAP(n_neighbors=25,min_dist=0.2)
# umap_2d.fit(x)
#
# projections = umap_2d.transform(x)
#
# fig = px.scatter(
#     projections, x=0, y=1,
#     color=y_entity.astype(str), labels={'color': 'entity'},
#     opacity=0.7
# )
# fig.show()
