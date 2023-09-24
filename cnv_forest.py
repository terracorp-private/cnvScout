# Data Processing
import pandas as pd
import numpy as np

# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image
from IPython.display import display
import graphviz


df = pd.read_csv("/home/alpha/programs/python_files/datasets/cnv_and_mut/entities.csv")

df = df.dropna(axis=1)
print(df)
# df = df[df.columns.drop(list(df.filter(regex='[YX]')))]
filter = df["Unnamed: 0"].str.contains(r'(^9|^3|^100|^201|^101|^200|^8)')
df = df[~filter]
X = df.drop("Unnamed: 0",axis=1)
X = X.drop("entity",axis=1)
print(X)
y = df["entity"].map({'gbm_cnv':0,'k27_cnv':1,'mng_cnv':2,'oligo_cnv':3,'pxa_cnv':4,'astroLow_cnv':5,'astroHigh_cnv':6,'pa_cnv':7})
print(y)

# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)


# Model fitting
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Accuracy test
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Export the first three decision trees from the forest

for i in range(3):
    tree = rf.estimators_[i]
    dot_data = export_graphviz(tree,
                               feature_names=X_train.columns,  
                               filled=True,  
                               max_depth=2, 
                               impurity=False, 
                               proportion=True)
    graph = graphviz.Source(dot_data)
    display(graph)

