# AB Testing (Hypothesis Tests) in Dataset  
![6505894](https://user-images.githubusercontent.com/95078183/226137808-ce2869c5-d640-4295-8363-a7173b6ecbf8.jpg)


---
### **Business Problem**
Facebook recently introduced a new bidding type, **'average bidding'**, as an alternative to the existing bidding type called **'maximum bidding'**.

bombabomba.com, is testing this new feature. They decided to try and want to do an A/B test to see if **'average bidding'** converts more than **'maximum bidding'**.

The A/B test has been going on for 1 month and bombabomba.com is now waiting to analyze the results of this A/B test. The ultimate success criterion for bombabomba.com is **Purchase**. Therefore, the focus should be on the **Purchase** metric for statistical testing.

A/B Testing is a statistical method about **Hypothesis Tests**. A typical hypothesis test is;

```math
H_0: M_1 = M_2
```
```math
H_1: M_1 ≠ M_2
```
H<sub>0</sub> is the **null hypothesis** that means it is the focus point of study. **Alternative hypothesis** that is H<sub>1</sub> is just a B plan. 

Statistical differences can be say about new feature and other bidding method if there is a enough evidence. Therefore, hypothesis test have to specify for this problem.


---
### **Story of Dataset**
In this data set that contains the website information of a company there is information such as the number of advertisements that users see and click, as well as earnings information from here. There are two separate sheets, the control and test groups.

These datasets are in separate sheets of the **ab_testing.xlsx**. **Maximum Bidding** was applied to the **control** group and **Average Bidding** was applied to the **test group**.

---

### **Variables in Dataset**

- **Impression**: Ad views
- **Click**: Clicks for ad displayed
- **Purchase**: Product purchasing after adds clicked
- **Earning**: Earnings after purchased products
---
### **Goal of the Project**


1-) Firstly, two data sheets need to be merged in dataframe;

```ruby
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=False)
```

2-) Then, there is a difference betwwen two group's mean. However, this difference should be proven with hypothesis test;
```ruby
df.groupby("group").agg({"Purchase": "mean"})

#          Purchase
# group
# control  550.8941
# test     582.1061
```

3-) Normality Assumption and shapiro test;
```ruby
for group in list(df["group"].unique()):
    pvalue = shapiro(df.loc[df["group"] == group, "Purchase"])[1]
    print(group, 'p-value = %.4f' % pvalue)
```

4-) Homogeneity of Variance and levene test;
```ruby
test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
```


4-) According to Normality Assumption and Homogeneity of Variance, Two Independent Sample T-test can be created;
```ruby
test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)
```
---

**Conclusion:** 
- p-value = 0.3493 => H<sub>0</sub> (null-hypothesis) cannot be rejected.
- There is not enough evidence that can say a statistical differences for control and test groups. 


