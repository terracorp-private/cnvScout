import pandas as pd
import glob
import re
import sys


# Fins all cnv files based on entity name
CASES = glob.glob("/home/alpha/programs/python_files/datasets/cnv_and_mut/WES_cnv/*")
GLOB_PATH = "/home/alpha/programs/python_files/datasets/cnv_and_mut/WES_cnv/"
REF = pd.read_excel("/home/alpha/programs/python_files/datasets/cnv_and_mut/setWES_CNV.xlsx")

REF = REF[REF["curated"] == 1]
refENT = REF["txt_EINSENDERDIAGNOSE"]
sampID = REF["material_id"]

cnv_files = ";".join(CASES)

missed_cases = []
df_cnv = pd.DataFrame()
for entity, sample in zip(refENT,sampID):
    print(entity,sample)
    if str(sample) not in cnv_files:
        missed_cases.append(sample)
    else:
        df = pd.read_excel(GLOB_PATH + str(sample) + ".xlsx")
        df = df[["chrom","win.start","segmented"]]
        df["chrom"] = df["chrom"].astype(str)
        df["win.start"] = df["win.start"].astype(str)
        df["bin"] = df["chrom"] + "-" + df["win.start"]
        df = df.set_index("bin")
        df = df.T
        df["entity"] = entity
        df["sample"] = sample
        df = df.drop(index=["chrom","win.start"])
        df_cnv = pd.concat([df_cnv,df])
        print(df_cnv)

df_cnv.to_csv("/home/alpha/programs/python_files/datasets/cnv_and_mut/" + "entitiesWES.csv")


