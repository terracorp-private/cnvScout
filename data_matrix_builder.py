#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def feature_selector(input_file):
    '''The function looks for less variable probes selects them and drops from initial dataframe.
    Additionaly some features may be selected for further analysis.
    '''


    # select feature "sample" or "diagnosis" and drop unneeded.
    df = pd.read_csv(input_file)
    df = df.set_index("Diagnose")
    df = df.drop(columns=["sample"])


    # TODO other methods to select features. For example quartiles.

    # print(df.std().sort_values(ascending=False))
    probes_std = df.std().sort_values(ascending=False)

    # TODO make a not-guesstimating method for threshold of feature selection. I.e. first derivative.
    probes_std_selected = probes_std[probes_std < 0.1]
    probes_names_to_drop = list(probes_std_selected.index)

    print(probes_names_to_drop)
    # print(probes_std_selected)
    # print(probes_std_selected.sort_values(ascending=False))

    cropped_frame = df.drop(columns=probes_names_to_drop)
    print(cropped_frame)

    return cropped_frame, probes_std


def harry_plotter(df):

    sns.set_theme()
    plot = sns.scatterplot(df)
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
    plt.show()




input_file, output_file = sys.argv[1:]

feature_selector(input_file)[0].to_csv(output_file)
# harry_plotter(feature_selector(input_file)[1])
