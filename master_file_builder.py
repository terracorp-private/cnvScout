import pandas as pd
import numpy as np
import glob
import sys
import pywt


# Fins all cnv files based on entity name
GLOB_PATH = "/home/alpha/programs/python_files/datasets/cnv_and_mut/"
ENTITY_NAME = ["gbm","k27","mng","oligo","pxa","astroLow","astroHigh","pa"]
FILE_TYPE = input("which file type to use? wes/igv \n")

if FILE_TYPE == "wes":
    POSTFIX = "_cnv/*.MAXDENS.segments.seg"
elif FILE_TYPE == "igv":
    POSTFIX = "_cnv/*.bins.igv"

# add all paths to a list
ENTITY_NAME_PATH = []
for entity in ENTITY_NAME:
    entityPath = glob.glob(GLOB_PATH + entity + POSTFIX)
    ENTITY_NAME_PATH.extend(entityPath)

# read the files into a dataframe
df_cnv = pd.DataFrame()
for entity in ENTITY_NAME_PATH:
    if FILE_TYPE == "seg":
        file = pd.read_csv(entity,sep="\t",header=0,names=["ID","chr","start","end","mark","bstat","pval","seg_mean","seg_median","alteration"])
        file["entity"] = entity.split("/")[-2]
        file["chr"] = file["chr"].replace(regex=r'[a-z]',value = '')
        file["chr"] = file["chr"].replace(regex=[r"X","Y"],value=[23,24])
        file["chr"] = file["chr"].astype("int")
    elif FILE_TYPE == "igv":
        file = pd.read_csv(entity,sep="\t",header=0,names=["chr","start","end","feature","value"])
        file = file[["feature",file.columns.tolist()[-1]]]
        file = file.set_index("feature")
        
        # PREFILTER DATA
        # file["value"] = 2*((file["value"]-file["value"].min())/(file["value"].max()-file["value"].min()))-1
        # file["value"] = (file["value"]-file["value"].mean())/file["value"].std()
        
        decomp_function = pd.Series(pywt.wavedec(file["value"], 'db1', level=2)[0])
        decomp_function = decomp_function.to_frame()
        decomp_function = decomp_function.T
        # extract the entity name from the path
        decomp_function["entity"] = entity.split("/")[-2] 
        # extract the ID from the path
        decomp_function["ID"] = entity.split("/")[-1].split(".")[0]
        # print(decomp_function.shape,decomp_function)
        # print(len(decomp_function))
        # 3883
        if decomp_function.shape == (1,3882):
            df_cnv = pd.concat([df_cnv,decomp_function])

df_cnv = df_cnv.set_index("ID")   
print(df_cnv.tail(2))

answer = input("do you what to save .cvs file? y/n \n")
if answer == "y":
    df_cnv.to_csv(GLOB_PATH + "entities_transformed.csv")
else:
    print("exiting program")