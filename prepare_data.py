import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


df = pd.read_csv("/home/alpha/programs/python_files/datasets/cnv_and_mut/entities.csv")

df = df[["entity","chr","start","end","alteration"]]
df["alteration"] = df["alteration"].replace(["balanced"],0)
df["alteration"] = df["alteration"].replace(["loss"],-1)
df["alteration"] = df["alteration"].replace(["gain"],1)
df["alteration"] = df["alteration"].replace(["chromothripsis"],2)
df["chr"] = df["chr"].astype("int")
print(df)
df = df.dropna()
print(df)

features = ["chr","alteration","start","end"]
x = df.loc[:,features].values
y = df.loc[:,["entity"]].values


x = StandardScaler().fit_transform(x)

pca = PCA(n_components=2)

principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

# unten würde ich df["entity"] durch y ersetzen, dafür muss ich y in df überführen
finalDf = pd.concat([principalDf, df['entity']], axis = 1)

print(finalDf.head())


fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

entities = ["k27_cnv","mng_cnv","gbm_cnv"]
colors = ['r', 'b', 'm']
for entity, color in zip(entities,colors):
    indicesToKeep = finalDf['entity'] == entity
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 10
               , alpha = 0.3)
ax.legend(entities)
ax.grid()
plt.show()

