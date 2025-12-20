#!/usr/bin/python

import pandas as pd


# process

df = pd.read_csv("./data/data_export_icin.csv", sep=';')

# print(df)
# print(df.columns)
print(df.info)

for col in df.columns:
    print(col)

# check missing values
print("\nmissing values: ")
print(df.isnull().sum())

'''
# plot

import matplotlib.pyplot as plt

# Basic info
summary = df[['HbA1c','Hba1c_change','age']].describe()

# Plot HbA1c distribution
plt.figure()
plt.hist(df['HbA1c'].dropna(), bins=30)
plt.xlabel('HbA1c')
plt.ylabel('Count')
plt.title('Distribution of HbA1c')
plt.savefig("./plt_output/HbA1c_distribution.png")
plt.show()

# Age distribution
plt.figure()
plt.hist(df['age'].dropna(), bins=30)
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Age Distribution')
plt.savefig("./plt_output/age_distribution.png")
plt.show()

# Glycemic control counts
plt.figure()
df['Glycemic_control'].value_counts().sort_index().plot(kind='bar')
plt.xlabel('Glycemic Control (0=Poor, 1=Good)')
plt.ylabel('Count')
plt.title('Glycemic Control Outcome')
plt.savefig("./plt_output/glycemic_control_outcome.png")
plt.show()

summary

# LDL / HDL / Triglyceride
plt.figure()
df[['LDL', 'HDL', 'Triglyceride']].boxplot()
plt.title('Distribution of Lipid Profiles')
plt.xlabel('Lipid Type')
plt.ylabel('Value')
plt.savefig("./plt_output/distribution_of_lipid_profiles.png")
plt.show()


# HbA1c and HbA1c change
plt.figure()
plt.scatter(df['HbA1c'], df['Hba1c_change'], alpha=0.3)
plt.xlabel('HbA1c')
plt.ylabel('HbA1c Change')
plt.title('Baseline HbA1c vs HbA1c Change')
plt.savefig("./plt_output/baseline_HbA1c_vs_HbA1c_change.png")
plt.show()

# HBA1c distribution by glycemic control
plt.figure()
df.boxplot(column='HbA1c', by='Glycemic_control')
plt.title('HbA1c Distribution by Glycemic Control')
plt.suptitle('')
plt.xlabel('Glycemic Control (0 = Poor, 1 = Good)')
plt.ylabel('HbA1c')
plt.savefig("./plt_output/HbA1c_distribution_by_glycemic_control.png")
plt.show()


# proportion of patients and prevalence of microvascular complications
microvascular = df[['diabetic_nueropathy', 'retinopathy', 'nephropaties']].mean()

plt.figure()
microvascular.plot(kind='bar')
plt.xlabel('Complication Type')
plt.ylabel('Proportion of Patients')
plt.title('Prevalence of Microvascular Complications')
plt.savefig("./plt_output/prevalence_of_microvascular_complications.png")
plt.show()


# common diabetes medication usage
medication_use = df[
    ['metformin_hcl', 'insulin_glarjin', 'dapagliflozin', 'sitagliptin']
].mean()

plt.figure()
medication_use.plot(kind='bar')
plt.xlabel('Medication')
plt.ylabel('Proportion of Use')
plt.title('Common Diabetes Medication Usage')
plt.savefig("./plt_output/common_diabetes_medication_usage.png")
plt.show()
'''