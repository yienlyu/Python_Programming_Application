#!/usr/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./data/data_export_icin.csv", sep=";")

df["insulin_use"] = (
    (df["insulin_glarjin"] > 0) |
    (df["insulin_aspart"] > 0) |
    (df["insulin_lispro"] > 0)
)

dm_drugs = [
    "metformin_hcl", "glimepirid", "gliklazid", "dapagliflozin",
    "sitagliptin", "linagliptin", "pioglitazon_hcl",
    "insulin_glarjin", "insulin_aspart", "insulin_lispro"
]

df["dm_drug_burden"] = df[dm_drugs].sum(axis=1)

# grouping
df_good = df[df["Glycemic_control"] == 0]
df_poor = df[df["Glycemic_control"] == 1]

# glycemic proportion (bar chart)
plt.figure()
df["Glycemic_control"].value_counts(normalize=True).sort_index().plot(kind="bar")
plt.xticks([0, 1], ["Good control", "Poor control"], rotation=0)
plt.ylabel("Proportion")
plt.title("Overall Glycemic Control Status")
plt.savefig("./plt_output/1227/Overall Glycemic Control Status")
plt.show()

# HbA1c distribution (histogram)
plt.figure()
plt.hist(df["HbA1c"].dropna(), bins=30)
plt.xlabel("HbA1c (%)")
plt.ylabel("Count")
plt.title("Distribution of HbA1c")
plt.savefig("./plt_output/1227/Distribution of HbA1c")
plt.show()

# age distribution (histogram)
plt.figure()
plt.hist(df["age"].dropna())
plt.ylabel("Age")
plt.title("Age Distribution (Data Quality Check)")
plt.savefig("./plt_output/1227/Age Distribution (Data Quality Check)")
plt.show()

# HbA1c extreme value check (boxplot)
plt.figure()
plt.boxplot(df["HbA1c"].dropna())
plt.ylabel("HbA1c (%)")
plt.title("HbA1c Distribution (Outlier Check)")
plt.savefig("./plt_output/1227/HbA1c Distribution (Outlier Check)")
plt.show()

# age v.s. glycemic control (boxplot)
plt.figure()
plt.boxplot(
    [df_good["age"].dropna(), df_poor["age"].dropna()],
    labels=["Good control", "Poor control"]
)
plt.ylabel("Age")
plt.title("Age by Glycemic Control")
plt.savefig("./plt_output/1227/Age by Glycemic Control")
plt.show()


# gender v.s. glycemic control (stacked bar)
sex_ct = pd.crosstab(df["sex"], df["Glycemic_control"], normalize="columns")

sex_ct.plot(kind="bar", stacked=True)
plt.ylabel("Proportion")
plt.title("Sex Distribution by Glycemic Control")
plt.legend(["Good control", "Poor control"], title="Glycemic control")
plt.savefig("./plt_output/1227/Sex Distribution by Glycemic Control")
plt.show()

# Labs v.s. glycemic control (boxplots)
labs = ["LDL", "HDL", "Triglyceride", "Creatinine"]

for lab in labs:
    plt.figure()
    plt.boxplot(
        [df_good[lab].dropna(), df_poor[lab].dropna()],
        labels=["Good control", "Poor control"]
    )
    plt.ylabel(lab)
    plt.title(f"{lab} by Glycemic Control")
    plt.savefig("./plt_output/1227/" + f"{lab} by Glycemic Control")
    plt.show()


# HbA1c v.s. other labs (heatmap)
lab_corr = df[["HbA1c", "LDL", "HDL", "Triglyceride", "Creatinine"]].corr()

plt.figure()
plt.imshow(lab_corr, cmap="coolwarm")
plt.colorbar()
plt.xticks(range(len(lab_corr)), lab_corr.columns, rotation=45)
plt.yticks(range(len(lab_corr)), lab_corr.columns)
plt.title("Correlation Heatmap: HbA1c and Laboratory Variables")
plt.savefig("./plt_output/1227/Correlation Heatmap: HbA1c and Laboratory Variables")
plt.show()

# cormorbidities v.s. glycemic control (bar chart)
comorbidities = {
    "Hypertension": "hypertension_i10",
    "CKD": "nephropaties",
    "Dyslipidemia": "lipoprotein_met_dis"
}

for name, var in comorbidities.items():
    rate = [
        df_good[var].mean(),
        df_poor[var].mean()
    ]
    
    plt.figure()
    plt.bar(["Good control", "Poor control"], rate)
    plt.ylabel("Proportion")
    plt.title(f"{name} Prevalence by Glycemic Control")
    plt.savefig("./plt_output/1227/" + f"{name} Prevalence by Glycemic Control")
    plt.show()

# insulin usage (binary)
insulin_rate = [
    df_good["insulin_use"].mean(),
    df_poor["insulin_use"].mean()
]

plt.figure()
plt.bar(["Good control", "Poor control"], insulin_rate)
plt.ylabel("Proportion")
plt.title("Insulin Use by Glycemic Control")
plt.savefig("./plt_output/1227/Insulin Use by Glycemic Control")
plt.show()

# Total antidiabetic drug exposure per patient (boxplot)
plt.figure()
plt.boxplot(
    [df_good["dm_drug_burden"], df_poor["dm_drug_burden"]],
    labels=["Good control", "Poor control"]
)
plt.ylabel("Total Diabetes Drug Exposure")
plt.title("Treatment Complexity by Glycemic Control")
plt.savefig("./plt_output/1227/Treatment Complexity by Glycemic Control")
plt.show()
