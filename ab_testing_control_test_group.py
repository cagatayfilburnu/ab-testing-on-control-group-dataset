#######################################################
# AB Testing with Control and Test Group
#######################################################
# 1- General Table of Dataset
# 2- Specifying Hypothesis Test
# 3- Calculations on Normality Assumption, Homogeneity of Variance and Hypothesis Test
# #- Conclusion

import itertools
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 500)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.float_format", lambda x: '%.4f' % x)

df_control = pd.read_excel("projects/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("projects/ab_testing.xlsx", sheet_name="Test Group")

#######################################################
# 1- General Table of Dataset
#######################################################
def check_df(dataframe, head=5):
    print("################ Shape ##################")
    print(dataframe.shape)
    print("################ Types ##################")
    print(dataframe.dtypes)
    print("################ Head ##################")
    print(dataframe.head(head))
    print("################ Tail ##################")
    print(dataframe.tail(head))
    print("################ NA ##################")
    if dataframe.isnull().values.any():
        print(dataframe.isnull().sum())
    else:
        print("There is no NA")
    print("################ Quantiles ##################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("################ Value Counts for Each Column ##################")
    for col in dataframe.columns:
        if dataframe[col].nunique() > 10:
            print("Too many elements for *{}*".format(col))
            continue
        else:
            print(f"{col}: {dataframe[col].value_counts()}")


check_df(df_test)
check_df(df_control)

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=False)
df.head()

df.groupby("group").agg({"Purchase": "mean"})


#######################################################
# 2- Specifying Hypothesis Test
#######################################################
# H0: M1 = M2
# H1: M1!= M2

df.groupby("group").agg({"Purchase": "mean"})

#          Purchase
# group
# control  550.8941
# test     582.1061

#######################################################
# 3- Calculations on Normality Assumption, Homogeneity of Variance and Hypothesis Test
#######################################################

# Normality Assumption
test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5891 => the assumption of normality is provided.

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.1541 => the assumption of normality is provided.

# Creating histogram for see the normal distribution.
def create_displot(dataframe, col):
    sns.displot(data=dataframe, x=col, kde=True)
    plt.show()


create_displot(df_control, "Purchase")
df_control["Purchase"].mean()
# 550.8940587702316

# This is the optional way to see p-values with for loop.
for group in list(df["group"].unique()):
    pvalue = shapiro(df.loc[df["group"] == group, "Purchase"])[1]
    print(group, 'p-value = %.4f' % pvalue)

# Homogeneity of Variance
test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.1083 => Variances are homogeneous.

# According to Normality Assumption and Homogeneity of Variance, two independent sample t-test can be created.
test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# Conclusion:
# p-value = 0.3493 => H0 cannot be rejected.
# There is not enough evidence that can say a statistical differences for control and test groups.
#
#
