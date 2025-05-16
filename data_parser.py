#!/usr/bin/env python3

import glob
import sys
import re
import pandas as pd


DATA_DIR = sys.argv[1]


def sample_selector(DATA_DIR):
    '''Read sample sheet and pick sample names, sex, age and
    diagnosis. Drop all samples with low read count.'''

    annotation_file = DATA_DIR + "features_frame_annon.xlsx"

    if annotation_file not in glob.glob(DATA_DIR+"*"):
        raise Exception("ERROR! Annotation file either not found or has wrong name")

    cases_df = pd.read_excel(annotation_file, usecols=["Barcode", "ID", "Diagnose", "Mean Cov"])

    if cases_df.empty:
        raise Exception(f"ERROR! Annotation file is empty")

    # Set the lowes tolerated read count. Default 200 reads.
    cases_df = cases_df[cases_df["Mean Cov"] >= 200]

    # Construct a distinct identifier. Since same samples could be
    # found accross multiple libraries.
    cases_df["sample"] = cases_df["Barcode"] + "_" + cases_df["ID"]

    if cases_df["sample"].duplicated().sum().sum() != 0:
        cases_df = cases_df.drop_duplicates(subset=["sample"])

    return cases_df


def datamatix_constructor(path_to_cnn, output_file, samples_df):
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

        if sample in selected_cases:
            print(sample)

            df = pd.read_csv(file, sep="\t", usecols=["chromosome","start","log2"])
            df["sample"] = sample
            data = pd.concat([df,data])

    # make identifier chrom_genomic_position
    data["identifier"] = data["chromosome"].astype(str) + "_" + data["start"].astype(str)
    data = data[(data["chromosome"] != "chrY") & (data["chromosome"] != "chrX")]
    data = data.drop(["chromosome","start"],axis=1)

    # generate Pivot table merged on sample
    data_long = data.pivot(index="sample", columns="identifier", values="log2")
    data_long = pd.merge(data_long, samples_df, on="sample", how="inner")
    data_long = data_long.drop(columns=["ID", "Barcode"])

    # TODO make state of the art output file
    if output_file != "":
        data_long.to_csv(output_file)
        print(data_long)
    else:
        print("No output")



samples_df = sample_selector(DATA_DIR)
datamatix_constructor(DATA_DIR+"antitarget_2025/",DATA_DIR+"raw_datamatrix.csv", samples_df)
