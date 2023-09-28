# Data Processing
import pandas as pd
import numpy as np


# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

DATA_PATH = "entities_transformed.csv"

df = pd.read_csv(DATA_PATH)

print(df.head())

df = df.dropna(axis=1)
# df = df[df.columns.drop(list(df.filter(regex='[YX]')))]
X = df.drop("ID",axis=1)
X = X.drop("entity",axis=1)
y = df["entity"].map({'gbm_cnv':0,'k27_cnv':1,'mng_cnv':2,'oligo_cnv':3,'pxa_cnv':4,'astroLow_cnv':5,'astroHigh_cnv':6,'pa_cnv':7})

# Standartize data
X =( X - X.mean() ) / X.std()

# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(type(X_train))

# Model fitting
rf = RandomForestClassifier(max_depth=9,n_estimators=294)
rf.fit(X_train, y_train)

# Accuracy testprint(y_pred)
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


# SECTION II
    
param_dist = {'n_estimators': randint(50,500),
              'max_depth': randint(1,20)}

# Create a random forest classifier
rf = RandomForestClassifier()

# Use random search to find the best hyperparameters
rand_search = RandomizedSearchCV(rf, 
                                 param_distributions = param_dist, 
                                 n_iter=5, 
                                 cv=5)

# Fit the random search object to the data
rand_search.fit(X_train, y_train)

# SECTION III

# Create a variable for the best model
best_rf = rand_search.best_estimator_

# Print the best hyperparameters
print('Best hyperparameters:',  rand_search.best_params_)

# Generate predictions with the best model
y_pred = best_rf.predict(X_test)