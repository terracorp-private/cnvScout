#!/usr/bin/env python3

import glob
import sys
import re
import pandas as pd


def datamatix_constructor(path_to_cnn, output_file):
    '''The function iterates through cnn files and merges them to one data_matrix,
    output needs an argv argument. Use /tmp/tmp.csv if you don't need one
    '''

    # TODO Duplicated samples management. Actuall solution is really quick and dirty.

    cases_df = pd.read_excel("../../../Documents/datasets/cnv_ngs/features_frame_annon.xlsx", usecols=["Barcode", "ID", "Diagnose"])
    cases_df["sample"] = cases_df["Barcode"] + "_" + cases_df["ID"]

    if cases_df["sample"].duplicated().sum().sum() != 0:
        cases_df = cases_df.drop_duplicates(subset=["sample"])
        print("Duplicates were dropped", cases_df[cases_df["sample"].duplicated() == True], sep="\n")

    selected_cases = cases_df["sample"].to_list()


    # empty dataframe for final merged data
    data = pd.DataFrame()

    for file in glob.glob(path_to_cnn + "*.cnn"):
        sample = re.findall(r"[0-9]{4}_.*_[0-9]{2}_", file)
        sample = "".join(sample)

        if sample in selected_cases:
            print(sample)

            df = pd.read_csv(file, sep="\t", usecols=["chromosome","start","log2"])
            df["sample"] = sample
            data = pd.concat([df,data])

    # print(data.isnull().any().any())
    data["identifier"] = data["chromosome"].astype(str) + "_" + data["start"].astype(str)
    data = data[(data["chromosome"] != "chrY") & (data["chromosome"] != "chrX")]
    data = data.drop(["chromosome","start"],axis=1)

    # TODO try nans
    # print(data.isnull().any().any())
    # print(data)
    # print(smpl_ser)
    # smpl = data[data["sample"] == "N1363_25"]
    # smpl_ser = data["sample"].value_counts()

    data_long = data.pivot(index="sample", columns="identifier", values="log2")
    data_long = pd.merge(data_long, cases_df, on="sample", how="inner")
    data_long = data_long.drop(columns=["ID", "Barcode"])

    # TODO try nans
    # print(data_long.isnull().any().any())

    # TODO make state of the art output file
    if output_file != "":
        # print(data_long["sample"].isnull().any().any())
        data_long.to_csv(output_file)
        print(data_long)
    else:
        print("No output")


path_to_cnn_directory, output_file = sys.argv[1:]

datamatix_constructor(path_to_cnn_directory, output_file)
