import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn
from pandas import Series
from pandas import DataFrame
from io import StringIO
from scipy import stats
from datetime import datetime
from pandas_datareader import DataReader
import requests
#PLOTTING 
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
#-------------------------------DONOR DATA SET-----------------------------------------------
donor_df=pd.read_csv('C:/Users/HP/Downloads/Election_Donor_Data.csv')
donor_df.info()
print(donor_df.head())
print(donor_df['contb_receipt_amt'].value_counts())

don_mean=donor_df['contb_receipt_amt'].mean()
don_std=donor_df['contb_receipt_amt'].std()

print("The average Donation was %.2f with a st.d of %.2f" %(don_mean,don_std))

#WHY IS STANDARD DVIATION SOO LARGE?????
top_donor=donor_df['contb_receipt_amt'].copy()
top_donor.sort_values()
print(top_donor)
#WE CAN SEE THERE ARE NEGATIVE VALUES WHICH MAY BE CAUSING THE DEVIATION
top_donor=top_donor[top_donor > 0]
print(top_donor)
#ONLY POSITIVE VALUES
print(top_donor.value_counts().head(10))#TOP 10 MOST COMMON DONATIONS

common_don=top_donor[top_donor < 2500] #common donations
common_don.hist(bins=100,figsize=(12,4))
#PEOPLE DONATE ROUNDED NUMBER VALUES GENERALLY

#DONATIONS BY PARTY
candidates=donor_df.cand_nm.unique()
print(candidates)
#WE HAVE TO SEPERATE BARAK OBAMA FROM THE REPUBLICANS TO DO DO PARTY BASED CALCULATIONS
#THUS, WE HAVE 2 METHODS 1.FOR LOOP 2.MAPPING,MAPPING IS FASTER BUT YOU HAVE TO WRITE LONG PARAGRAPHS 

#METHOD1
party_map={'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}
          
donor_df['Party']=donor_df.cand_nm.map(party_map)
donor_df=donor_df[donor_df > 0]
print(donor_df.head(20))
#METHOD2
donor_df['Party']=np.zeros(len(donor_df))
for i in range(0,len(donor_df)):
    if donor_df['cand_nm'][i]=='Obama,Barack':
        donor_df['Party'][i]='Democrat'
    else:
        donor_df['Party'][i]='Republican'
print(donor_df.head(20))

print(donor_df.groupby('cand_nm')['contb_receipt_amt'].count())
cand_don = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()#sum to see total amount
print(cand_don)
#OR
donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')
print(cand_don)
#Now we cannot see the numbers properly,so lets plot them instead
cand_don.plot(kind='bar')

#We can also print them using for loop
i=0
for j in cand_don:
    print('%s raised $%.2f' %(cand_don.index[i],j))#cand_dom prints name as it is the index of the list
    print("\n")
    i+=1
   
occupation_df=donor_df.pivot_table('contb_receipt_amt',index='contbr_occupation',
                                   columns='Party',aggfunc='sum')
print(occupation_df.head())
print(occupation_df.shape)
#HOW TO MAKE SENSE OUT OF THESE 45073 OCCUPATIONS?? BYFILTERING OUT LOWER CONTRIBUTIONS
occupation_df=occupation_df[occupation_df.sum(1)>1000000]
print(occupation_df.shape)
occupation_df.plot(kind='bar',figsize=(12,4),cmap='seismic')
#Remove information requested and combine CEO and C.E.O
occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)
occupation_df.loc['CEO']=occupation_df.loc['CEO']+occupation_df.loc['C.E.O.']
occupation_df.drop('C.E.O.',inplace=True)
occupation_df.plot(kind='bar',figsize=(12,4),cmap='seismic')