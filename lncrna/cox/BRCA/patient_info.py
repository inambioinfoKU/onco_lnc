## A script for extracting info about the patients used in the analysis

## Load necessary modules

from rpy2 import robjects as ro
import numpy as np
import os
ro.r('library(survival)')
import re

##This call will only work if you are running python from the command line.
##If you are not running from the command line manually type in your paths.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))



## There were three clinical files with nonredundant data.  V4.0 is in general the most uptodate, but it is possible
## for data in the other files to be more uptodate.  As a result, clinical data will be merged.


f=open(os.path.join(BASE_DIR,'tcga_data','BRCA','clinical','nationwidechildrens.org_clinical_follow_up_v4.0_brca.txt'))
##get the column indexes needed
columns=f.readline().split('\t')
patient_column=columns.index('bcr_patient_barcode')
alive_column=columns.index('last_contact_days_to')
death_column=columns.index('death_days_to')
f.readline()
f.readline()
data=[i.split('\t') for i in f]
## A patient can be listed multiple times in the file. The most recent listing (furthest down in the file), contains the most recent
## follow up data.  This code checks if the patient has already been loaded into the list, and if so, takes the more recent data.
## This required an empty value in the list initialization.
## Data is: [[Patient ID, time(days), Vital status],[Patient ID, time(days), Vital status],...]
clinical1=[['','','']]
for i in data:
    if clinical1[-1][0]==i[patient_column]:
        if re.search('^[0-9]+$',i[alive_column]):
            clinical1[-1]=[i[patient_column],int(i[alive_column]),'Alive']
        elif re.search('^[0-9]+$',i[death_column]):
            clinical1[-1]=[i[patient_column],int(i[death_column]),'Dead']
        else:
            pass
    else:
        if re.search('^[0-9]+$',i[alive_column]):
            clinical1.append([i[patient_column],int(i[alive_column]),'Alive'])
        elif re.search('^[0-9]+$',i[death_column]):
            clinical1.append([i[patient_column],int(i[death_column]),'Dead'])
        else:
            pass


## Removing the empty value.
clinical1=clinical1[1:]


f=open(os.path.join(BASE_DIR,'tcga_data','BRCA','clinical','nationwidechildrens.org_clinical_follow_up_v2.1_brca.txt'))
##get the column indexes needed
columns=f.readline().split('\t')
patient_column=columns.index('bcr_patient_barcode')
alive_column=columns.index('last_contact_days_to')
death_column=columns.index('death_days_to')
f.readline()
f.readline()
data=[i.split('\t') for i in f]
clinical2=[['','','']]
for i in data:
    if clinical2[-1][0]==i[patient_column]:
        if re.search('^[0-9]+$',i[alive_column]):
            clinical2[-1]=[i[patient_column],int(i[alive_column]),'Alive']
        elif re.search('^[0-9]+$',i[death_column]):
            clinical2[-1]=[i[patient_column],int(i[death_column]),'Dead']
        else:
            pass
    else:
        if re.search('^[0-9]+$',i[alive_column]):
            clinical2.append([i[patient_column],int(i[alive_column]),'Alive'])
        elif re.search('^[0-9]+$',i[death_column]):
            clinical2.append([i[patient_column],int(i[death_column]),'Dead'])
        else:
            pass


##removing the empty value
clinical2=clinical2[1:]


##merging the data
new_clinical=[]

for i in clinical2:
    if i[0] not in [j[0] for j in clinical1]:
        new_clinical.append(i)
    else:
        if i[1]<=clinical1[[j[0] for j in clinical1].index(i[0])][1]:
            new_clinical.append(clinical1[[j[0] for j in clinical1].index(i[0])])
        else:
            new_clinical.append(i)



for i in clinical1:
    if i[0] not in [j[0] for j in new_clinical]:
        new_clinical.append(i)




f=open(os.path.join(BASE_DIR,'tcga_data','BRCA','clinical','nationwidechildrens.org_clinical_follow_up_v1.5_brca.txt'))
##get the column indexes needed
columns=f.readline().split('\t')
patient_column=columns.index('bcr_patient_barcode')
alive_column=columns.index('last_contact_days_to')
death_column=columns.index('death_days_to')
f.readline()
f.readline()
data=[i.split('\t') for i in f]
clinical3=[['','','']]
for i in data:
    if clinical3[-1][0]==i[patient_column]:
        if re.search('^[0-9]+$',i[alive_column]):
            clinical3[-1]=[i[patient_column],int(i[alive_column]),'Alive']
        elif re.search('^[0-9]+$',i[death_column]):
            clinical3[-1]=[i[patient_column],int(i[death_column]),'Dead']
        else:
            pass
    else:
        if re.search('^[0-9]+$',i[alive_column]):
            clinical3.append([i[patient_column],int(i[alive_column]),'Alive'])
        elif re.search('^[0-9]+$',i[death_column]):
            clinical3.append([i[patient_column],int(i[death_column]),'Dead'])
        else:
            pass


##removing the empty value
clinical3=clinical3[1:]


##merging the data
newer_clinical=[]

for i in clinical3:
    if i[0] not in [j[0] for j in new_clinical]:
        newer_clinical.append(i)
    else:
        if i[1]<=new_clinical[[j[0] for j in new_clinical].index(i[0])][1]:
            newer_clinical.append(new_clinical[[j[0] for j in new_clinical].index(i[0])])
        else:
            newer_clinical.append(i)

for i in new_clinical:
    if i[0] not in [j[0] for j in newer_clinical]:
        newer_clinical.append(i)


## Grade, sex, and age information were taken from the "clinical_patient" file.  A dictionary was created for sex and grade.
more_clinical={}
grade_dict={}
grade_dict['Infiltrating Ductal Carcinoma']=1
grade_dict['Metaplastic Carcinoma']=3
grade_dict['Mucinous Carcinoma']=4
grade_dict['Medullary Carcinoma']=5
grade_dict['Infiltrating Lobular Carcinoma']=6




sex_dict={}
sex_dict['MALE']=0
sex_dict['FEMALE']=1

## The "clinical_patient" file can also contain patients not listed in the follow_up files.
## In these cases the clinical data for these patients gets appended to a new clinical list.

f=open(os.path.join(BASE_DIR,'tcga_data','BRCA','clinical','nationwidechildrens.org_clinical_patient_brca.txt'))
columns=f.readline().split('\t')
grade_column=columns.index('histological_type')
sex_column=columns.index('gender')
age_column=columns.index('age_at_diagnosis')
patient_column=columns.index('bcr_patient_barcode')
alive_column=columns.index('last_contact_days_to')
death_column=columns.index('death_days_to')
f.readline()
f.readline()
data=[i.split('\t') for i in f]
clinical4=[]
for i in data:
    try:
        more_clinical[i[patient_column]]=[grade_dict[i[grade_column]],sex_dict[i[sex_column]],int(i[age_column])]
        if re.search('^[0-9]+$',i[alive_column]):
            clinical4.append([i[patient_column],int(i[alive_column]),'Alive'])
        elif re.search('^[0-9]+$',i[death_column]):
            clinical4.append([i[patient_column],int(i[death_column]),'Dead'])
        else:
            pass

    except:
        pass


newest_clinical=[]

##It is possible that the clinical data in the clinical_patient file is more up to date than the follow_up files
##All the clinical data is merged checking which data is the most up to date

for i in clinical4:
    if i[0] not in [j[0] for j in newer_clinical]:
        newest_clinical.append(i)
    else:
        if i[1]<=newer_clinical[[j[0] for j in newer_clinical].index(i[0])][1]:
            newest_clinical.append(newer_clinical[[j[0] for j in newer_clinical].index(i[0])])
        else:
            newest_clinical.append(i)


##also do the reverse since clinical can contain patients not included in clinical4
for i in newer_clinical:
    if i[0] not in [j[0] for j in newest_clinical]:
        newest_clinical.append(i)


## only patients who had a follow up time greater than 0 days are included in the analysis
clinical=[i for i in newest_clinical if i[1]>0]

final_clinical=[]

## A new list containing both follow up times and grade, sex, and age is constructed.
## Only patients with grade, sex, and age information are included.
## Data is [[Patient ID, time (days), vital status, grade, sex, age at diagnosis],...]

for i in clinical:
    if i[0] in more_clinical:
        final_clinical.append(i+more_clinical[i[0]])




##In a separate script I parsed the mitranscriptome.expr.counts.tsv file and extracted the BRCA patient and expression values.
##From this file I will load the expression data.
##There are duplicated transcripts and the possibility of a patient having multiple sequencing files.


f=open(os.path.join(BASE_DIR,'tcga_data','BRCA','lncrna','BRCA.txt'))
##patient list is at the top of the file

patients=f.readline().strip().split()



##create a dictionary mapping patient to all of their lncrna expression data
patient_dict={}
for index, i in enumerate(patients):
    patient_dict[i[:12]]=''


##find which patients have complete clinical data, order the data, and average data if necessary
##it's possible there are expression data for patients without clinical data, and clinical data without expression data

##create a new clinical list called clinical_and_files for consistency with previous scripts
clinical_and_files=[]
for i in final_clinical:
    if i[0] in patient_dict:
        clinical_and_files.append(i)

##print average age at diagnosis
age=np.mean([i[5] for i in clinical_and_files])

##print number of males
males=len([i for i in clinical_and_files if i[4]==0])

##print number of females
females=len([i for i in clinical_and_files if i[4]==1])

##to get the median survival we need to call survfit from r


##prepare variables for R
ro.globalenv['times']=ro.IntVector([i[1] for i in clinical_and_files])

##need to create a dummy variable group
ro.globalenv['group']=ro.IntVector([0 for i in clinical_and_files])

##need a vector for deaths
death_dic={}
death_dic['Alive']=0
death_dic['Dead']=1
ro.globalenv['died']=ro.IntVector([death_dic[i[2]] for i in clinical_and_files])

res=ro.r('survfit(Surv(times,died) ~ as.factor(group))')

#the number of events(deaths) is the fourth column of the output
deaths=str(res).split('\n')[-2].strip().split()[3]


#the median survival time is the fifth column of the output
median=str(res).split('\n')[-2].strip().split()[4]


##write data to a file
f=open('patient_info.txt','w')
f.write('Average Age')
f.write('\t')
f.write('Males')
f.write('\t')
f.write('Females')
f.write('\t')
f.write('Deaths')
f.write('\t')
f.write('Median Survival')
f.write('\n')

f.write(str(age))
f.write('\t')
f.write(str(males))
f.write('\t')
f.write(str(females))
f.write('\t')
f.write(deaths)
f.write('\t')
f.write(median)
f.close()








