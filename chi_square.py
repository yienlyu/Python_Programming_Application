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

pd.crosstab(df["Glycemic_control"], df["hypertension_i10"])

from scipy.stats import chi2_contingency

# hypertension v.s. glycemic control
table = pd.crosstab(df["Glycemic_control"], df["hypertension_i10"])
chi2, p, dof, expected = chi2_contingency(table)

print("\n##########\n")
print("Hypertension vs Glycemic control")
print(table)
print(f"Chi-square = {chi2:.2f}, p-value = {p:.3e}")

# gender v.s. glycemic control
table = pd.crosstab(df["Glycemic_control"], df["sex"])
chi2, p, dof, expected = chi2_contingency(table)

print("\n##########\n")
print("Sex vs Glycemic control")
print(table)
print(f"Chi-square = {chi2:.2f}, p-value = {p:.3e}")

# insulin use v.s. glycemic control
table = pd.crosstab(df["Glycemic_control"], df["insulin_use"])
chi2, p, dof, expected = chi2_contingency(table)

print("\n##########\n")
print("Insulin use vs Glycemic control")
print(table)
print(f"Chi-square = {chi2:.2f}, p-value = {p:.3e}")

# comorbidities v.s. glycemic control
comorbidities = {
    "Hypertension": "hypertension_i10",
    "CKD": "nephropaties",
    "Dyslipidemia": "lipoprotein_met_dis"
}

for name, var in comorbidities.items():
    table = pd.crosstab(df["Glycemic_control"], df[var])
    chi2, p, _, _ = chi2_contingency(table)
    print("\n##########\n")
    print(name + "vs Glycemic control")
    print(table)
    print(f"Chi-square = {chi2:.2f}, p-value = {p:.3e}")
