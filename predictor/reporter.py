#!/usr/bin/env python3


def var_filter(features, plot):
    """Plot variations chromosomal abberation."""
    probes_variance = features.var().sort_values()
    probes_variance = probes_variance.to_frame(name="values")
    probes_variance["chrom"] = probes_variance.index.str.split("_").str[0]

    sns.boxplot(data=probes_variance,
                x="chrom",
                y="values",
                log_scale=True,
                )
    plt.show()
