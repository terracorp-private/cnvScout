import pandas as pd
import glob
import sys


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
        # file = pd.read_csv(entity,sep="\t",header=0,names=["chr","start","end","feature","value"])
        file = pd.read_csv(entity,sep="\t")
        file = file[["Feature",file.columns.tolist()[-1]]]
        file = file.set_index("Feature")
        file = file.T
        file["entity"] = entity.split("/")[-2]
        print(file.shape)
        if file.shape == (1,15524):
            df_cnv = pd.concat([df_cnv,file])
            print(df_cnv)
    
print(df_cnv.tail(10))

answer = input("do you what to save .cvs file? y/n \n")
if answer == "y":
    df_cnv.to_csv(GLOB_PATH + "entities.csv")
else:
    print("exiting program")




