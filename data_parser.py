#!/usr/bin/env python3

import glob
import sys
import re
import pandas as pd


DATA_DIR = sys.argv[1]


def na_finder(data):

    columns_with_na = data.isnull().any()
    columns_with_na = columns_with_na[columns_with_na].index.tolist()
    if len(columns_with_na) != 0:
        print(f"Columns with NA \n {columns_with_na}\n")


def sample_selector(DATA_DIR, min_reads):
    """Read sample sheet and pick sample names, sex, age and
    diagnosis. Drop all samples with low read count."""

    annotation_file = DATA_DIR + "features_frame_annon.xlsx"


    if annotation_file not in glob.glob(DATA_DIR+"*"):
        raise Exception("ERROR! Annotation file either not found or has wrong name")

    cases_df = pd.read_excel(annotation_file, usecols=["Barcode", "ID", "Diagnose", "Mean Cov"])

    if cases_df.empty:
        raise Exception(f"ERROR! Annotation file is empty")

    # Set the lowes tolerated read count. Default 200 reads.
    cases_df = cases_df[cases_df["Mean Cov"] >= min_reads]

    # Construct a distinct identifier. Since same samples could be
    # found accross multiple libraries.
    cases_df["sample"] = cases_df["Barcode"] + "_" + cases_df["ID"]

    if cases_df["sample"].duplicated().sum().sum() != 0:
        cases_df = cases_df.drop_duplicates(subset=["sample"])

    cases_df = cases_df.drop(columns=["Barcode","ID","Mean Cov"])

    return cases_df


def datamatix_constructor(path_to_cnn, samples_df):
    '''The function iterates through cnn files and merges them to one data_matrix,
    output needs an argv argument. Use /tmp/tmp.csv if you don't need one
    '''

    # TODO Duplicated samples management. Actuall solution is really quick and dirty.
    # Read sample sheet. Construct barcode_SampleID identifier. Since there could be duplicated samples in separate libraries.
    # Drop duplicated barcode_SampleIDs and return a sample list.

    selected_cases = samples_df["sample"].to_list()

    # empty dataframe for final merged data
    data = pd.DataFrame()

    for file in glob.glob(path_to_cnn + "*.cnn"):
        sample = re.findall(r"[0-9]{4}_.*_[0-9]{2}_", file)
        sample = "".join(sample)
        # print(sample)

        if sample in selected_cases:
            df = pd.read_csv(file,
                             sep="\t",
                             usecols=["chromosome", "start", "log2"],
                             )
            print(df.shape)
            if (df.shape[0] == 19062 or df.shape[0] == 789):
                df["sample"] = sample
                df["probe"] = df["chromosome"].astype(str) + "_" + df["start"].astype(str)
                print(df.shape[0], sample, df.columns, sep="\t")

                data = pd.concat([df, data])

    # print(data)
    # make identifier chrom_genomic_position
    data = data[(data["chromosome"] != "chrY") & (data["chromosome"] != "chrX")]
    data = data.drop(["chromosome", "start"], axis=1)

    # generate Pivot table merged on sample
    data_long = data.pivot(index="sample", columns="probe", values="log2")
    data_long = pd.merge(data_long, samples_df, on="sample", how="inner")
    na_finder(data_long)

    return data_long


def final_matrix_merger(antitarget, target, DATA_DIR):

    """This function takes antitarget_cnv and target_cnv data,
    and merges them.
    """

    final_df = pd.merge(antitarget, target, on=["sample", "Diagnose"], how="inner")
    # final_df = final_df.dropna(axis=1)
    final_df.to_csv(DATA_DIR+"raw_datamatrix.csv", index=False)


samples_df = sample_selector(DATA_DIR, 200)
antitarget = datamatix_constructor(DATA_DIR+"antitarget/", samples_df)
target = datamatix_constructor(DATA_DIR+"target/", samples_df)
final_matrix_merger(antitarget, target, DATA_DIR)
