#!/usr/bin/python

import pandas as pd
import numpy as np

df = pd.read_csv("./data/data_export_icin.csv", sep=";")

# group by Glycemic_control
df_good = df[df["Glycemic_control"] == 0]
df_poor = df[df["Glycemic_control"] == 1]


# Descriptive Statistics
control_ratio = df["Glycemic_control"].value_counts(normalize=True)
print(control_ratio)

df_good.to_csv("./data/glycemic_control_good.csv", index=False)
df_poor.to_csv("./data/glycemic_control_poor.csv", index=False)

# comorbidity
comorbidities = [
    "nephropaties",     # CKD
    "kidney_failure",
    "hypertension_i10", # HTN
    "ischemic_heart_dis"
]

# diabetes medications
dm_meds = [
    "metformin_hcl",
    "insulin_glarjin",
    "dapagliflozin",
    "sitagliptin"
]

# age
df_good["age"].describe()
df_poor["age"].describe()

# sex
df_good["sex"].value_counts(normalize=True)
df_poor["sex"].value_counts(normalize=True)

# lipid profile
df_good["HDL_ok"] = df_good["HDL"] > 35
df_good["LDL_ok"] = df_good["LDL"] < 100
df_good["TG_ok"]  = df_good["Triglyceride"] < 150

df_good[["HDL_ok", "LDL_ok", "TG_ok"]].mean()

df_poor["HDL_ok"] = df_poor["HDL"] > 35
df_poor["LDL_ok"] = df_poor["LDL"] < 100
df_poor["TG_ok"]  = df_poor["Triglyceride"] < 150

df_poor[["HDL_ok", "LDL_ok", "TG_ok"]].mean()

# creatinine
df_good["Creatinine"].describe()
df_poor["Creatinine"].describe()

# cormorbidities
df_good[comorbidities].mean()
df_poor[comorbidities].mean()

# diabetes medications
df_good[dm_meds].mean()
df_poor[dm_meds].mean()



# Statistical Analyze
# t-test
from scipy.stats import ttest_ind

ttest_ind(
    df_good["age"],
    df_poor["age"],
    nan_policy="omit"
)

# chi-square
from scipy.stats import chi2_contingency

table = pd.crosstab(df["Glycemic_control"], df["hypertension_i10"])
chi2_contingency(table)


# EDA Visualization using matplotlib
# Grouped by Glycemic_control

import matplotlib.pyplot as plt


# Glycemic control proportion
title = "Proportion_of_Glycemic_Control_Status"

plt.figure()
df["Glycemic_control"].value_counts(normalize=True).sort_index().plot(kind="bar")
plt.xticks([0, 1], ["Good control", "Poor control"], rotation=0)
plt.ylabel("Proportion")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.show()

# Age distribution (boxplot) 
title = "Age_Distribution_by_Glycemic_Control"

plt.figure()
plt.boxplot([df_good["age"].dropna(), df_poor["age"].dropna()], labels=["Good", "Poor"])
plt.ylabel("Age")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.show()

# Sex proportion 
title = "Sex_Distribution_by_Glycemic_Control"

sex_prop = pd.DataFrame({
    "Good": df_good["sex"].value_counts(normalize=True),
    "Poor": df_poor["sex"].value_counts(normalize=True)
}).fillna(0)

x = np.arange(len(sex_prop.index))
width = 0.35

plt.figure()
plt.bar(x - width/2, sex_prop["Good"], width, label="Good")
plt.bar(x + width/2, sex_prop["Poor"], width, label="Poor")
plt.xticks(x, sex_prop.index)
plt.ylabel("Proportion")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.legend()
plt.show()

# Lipid profile target achievement 
title = "Lipid_Profile_Control_by_Glycemic_Status"

lipid_good = {
    "HDL>35": (df_good["HDL"] > 35).mean(),
    "LDL<100": (df_good["LDL"] < 100).mean(),
    "TG<150": (df_good["Triglyceride"] < 150).mean()
}

lipid_poor = {
    "HDL>35": (df_poor["HDL"] > 35).mean(),
    "LDL<100": (df_poor["LDL"] < 100).mean(),
    "TG<150": (df_poor["Triglyceride"] < 150).mean()
}

labels = list(lipid_good.keys())
x = np.arange(len(labels))

plt.figure()
plt.bar(x - width/2, lipid_good.values(), width, label="Good")
plt.bar(x + width/2, lipid_poor.values(), width, label="Poor")
plt.xticks(x, labels)
plt.ylabel("Proportion Achieving Target")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.legend()
plt.show()

# Creatinine distribution 
title = "Creatinine_Distribution_by_Glycemic_Control"

plt.figure()
plt.boxplot(
    [df_good["Creatinine"].dropna(), df_poor["Creatinine"].dropna()],
    labels=["Good", "Poor"]
)
plt.ylabel("Creatinine")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.show()

# Comorbidities prevalence 
title = "Comorbidities_by_Glycemic_Control"

comorbidities = ["nephropaties", "hypertension_i10", "ischemic_heart_dis"]

good_com = df_good[comorbidities].mean()
poor_com = df_poor[comorbidities].mean()

x = np.arange(len(comorbidities))

plt.figure()
plt.bar(x - width/2, good_com, width, label="Good")
plt.bar(x + width/2, poor_com, width, label="Poor")
plt.xticks(x, ["CKD", "HTN", "IHD"])
plt.ylabel("Proportion")
plt.title(title)
plt.savefig("./plt_output/{title}")
plt.legend()
plt.show()

# Diabetes medication usage 
title = "Diabetes_Medication_Usage_by_Glycemic_Control"

meds = ["metformin_hcl", "insulin_glarjin", "dapagliflozin", "sitagliptin"]

good_med = df_good[meds].mean()
poor_med = df_poor[meds].mean()

x = np.arange(len(meds))

plt.figure()
plt.bar(x - width/2, good_med, width, label="Good")
plt.bar(x + width/2, poor_med, width, label="Poor")
plt.xticks(x, ["Metformin", "Basal insulin", "SGLT2i", "DPP4i"], rotation=20)
plt.ylabel("Proportion of Use")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.legend()
plt.show()

# HbA1c boxplot 
title = "HbA1c_Distribution_by_Glycemic_Control"

plt.figure()
plt.boxplot(
    [df_good["HbA1c"].dropna(), df_poor["HbA1c"].dropna()],
    labels=["Good control", "Poor control"]
)
plt.ylabel("HbA1c (%)")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.show()

# HbA1c change boxplot 
title = "HbA1c_Change_by_Glycemic_Control"

plt.figure()
plt.boxplot(
    [df_good["Hba1c_change"].dropna(), df_poor["Hba1c_change"].dropna()],
    labels=["Good control", "Poor control"]
)
plt.ylabel("HbA1c Change")
plt.title(title)
plt.savefig("./plt_output/" + title)
plt.show()


# Export Table
summary = pd.DataFrame(columns=["Glycemic control: Good", "Glycemic control: Poor"])

# Continuous var: age, creatinine
summary.loc["Age (mean ± SD)", "Glycemic control: Good"] = (
    f"{df_good['age'].mean():.1f} ± {df_good['age'].std():.1f}"
)
summary.loc["Age (mean ± SD)", "Glycemic control: Poor"] = (
    f"{df_poor['age'].mean():.1f} ± {df_poor['age'].std():.1f}"
)

summary.loc["Creatinine (mean ± SD)", "Glycemic control: Good"] = (
    f"{df_good['Creatinine'].mean():.2f} ± {df_good['Creatinine'].std():.2f}"
)
summary.loc["Creatinine (mean ± SD)", "Glycemic control: Poor"] = (
    f"{df_poor['Creatinine'].mean():.2f} ± {df_poor['Creatinine'].std():.2f}"
)

# sex
summary.loc["Male (%)", "Glycemic control: Good"] = (
    f"{(df_good['sex'] == 1).mean() * 100:.1f}%"
)
summary.loc["Male (%)", "Glycemic control: Poor"] = (
    f"{(df_poor['sex'] == 1).mean() * 100:.1f}%"
)

# lipid profile
summary.loc["HDL > 35 (%)", "Glycemic control: Good"] = (
    f"{(df_good['HDL'] > 35).mean() * 100:.1f}%"
)
summary.loc["HDL > 35 (%)", "Glycemic control: Poor"] = (
    f"{(df_poor['HDL'] > 35).mean() * 100:.1f}%"
)

summary.loc["LDL < 100 (%)", "Glycemic control: Good"] = (
    f"{(df_good['LDL'] < 100).mean() * 100:.1f}%"
)
summary.loc["LDL < 100 (%)", "Glycemic control: Poor"] = (
    f"{(df_poor['LDL'] < 100).mean() * 100:.1f}%"
)

summary.loc["TG < 150 (%)", "Glycemic control: Good"] = (
    f"{(df_good['Triglyceride'] < 150).mean() * 100:.1f}%"
)
summary.loc["TG < 150 (%)", "Glycemic control: Poor"] = (
    f"{(df_poor['Triglyceride'] < 150).mean() * 100:.1f}%"
)

# comorbidities (binary)
summary.loc["CKD (%)", "Glycemic control: Good"] = (
    f"{df_good['nephropaties'].mean() * 100:.1f}%"
)
summary.loc["CKD (%)", "Glycemic control: Poor"] = (
    f"{df_poor['nephropaties'].mean() * 100:.1f}%"
)

summary.loc["Hypertension (%)", "Glycemic control: Good"] = (
    f"{df_good['hypertension_i10'].mean() * 100:.1f}%"
)
summary.loc["Hypertension (%)", "Glycemic control: Poor"] = (
    f"{df_poor['hypertension_i10'].mean() * 100:.1f}%"
)

# diabetes medications
summary.loc["Metformin (%)", "Glycemic control: Good"] = (
    f"{df_good['metformin_hcl'].mean() * 100:.1f}%"
)
summary.loc["Metformin (%)", "Glycemic control: Poor"] = (
    f"{df_poor['metformin_hcl'].mean() * 100:.1f}%"
)

summary.loc["Basal insulin (%)", "Glycemic control: Good"] = (
    f"{df_good['insulin_glarjin'].mean() * 100:.1f}%"
)
summary.loc["Basal insulin (%)", "Glycemic control: Poor"] = (
    f"{df_poor['insulin_glarjin'].mean() * 100:.1f}%"
)

'''
Medication categories are not mutually exclusive; 
proportions therefore reflect usage prevalence 
rather than exclusive treatment assignment.
'''

# export
print(summary)
summary.to_csv("./data/Table1_Glycemic_control_summary.csv")
