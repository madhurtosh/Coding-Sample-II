
# coding: utf-8

# # Data Preparation

# In[2]:


import pandas as pd
import numpy as np
import os
pd.set_option('display.max_columns', 500)


# In[3]:


pwd = "D:/MOA Data"
os.chdir(pwd)


# In[3]:


filename = "staff_allocation_matrix.csv"
staff = pd.read_csv(filename, sep = None, parse_dates = [0], engine='python')
staff.drop(columns='Dept',inplace=True)
staff.rename({'LaborDate':'Date'}, axis='columns', inplace=True)
staff['Shift'].replace(['AM','PM'],[0,1],inplace=True)
staff = staff.groupby(['Date', 'Shift']).sum()


# In[4]:


filename = "ride_sales_by_shift.csv"
rides_revenue = pd.read_csv(filename, sep = None, parse_dates = ['Date'], engine='python')
rides_revenue.rename({'Revenue':'Rides Revenue'}, axis='columns', inplace=True)


# In[5]:


filename = "Item_Sales_by_Shift.csv"
items_revenue = pd.read_csv(filename, sep = None, parse_dates = ['SalesDate'], engine='python')
items_revenue.rename({'SalesDate':'Date', 'Sales':'Items Revenue'}, axis='columns', inplace=True)


# In[6]:


filename = "Food_Sales_by_Shift.csv"
food_revenue = pd.read_csv(filename, sep = None, parse_dates = ['SalesDate'], engine='python')
food_revenue.rename({'SalesDate':'Date', 'Sales':'Food Revenue'}, axis='columns', inplace=True)


# In[7]:


filename = "state_data.csv"
state = pd.read_csv(filename,sep = None,parse_dates = [1],engine='python')
state.rename({'Unnamed: 0':'#','shift':'Shift'}, axis='columns', inplace=True)


# In[8]:


df = rides_revenue.merge(food_revenue,left_on=['Date','Shift'],right_on=['Date','Shift'])


# In[9]:


df = df.merge(items_revenue,left_on=['Date','Shift'],right_on=['Date','Shift'])


# In[10]:


df = df.merge(state,left_on=['Date','Shift'],right_on=['Date','Shift'])


# In[11]:


df = df.merge(staff,left_on=['Date','Shift'],right_on=['Date','Shift'])
df.drop(columns=['id','#'],inplace=True)


# In[12]:


df.columns


# In[13]:


# Adding modified ridership column <that excudes missing scans>, and adding to df
filename = "state_data_filtered_ridership.csv"
modified_ridership = pd.read_csv(filename, sep = None, usecols = ['Date','Shift','riders'], parse_dates = [0], engine='python')
modified_ridership.rename(columns = {'riders':'Modified Ridership'}, inplace=True)
df = pd.merge(df, modified_ridership, how='left', on=['Date','Shift'])


# In[14]:


forecasted_ridership = pd.read_csv('Forecasted_Ridership_State.csv')
df['Date'] = pd.to_datetime(df['Date'])
forecasted_ridership['Date'] = pd.to_datetime(forecasted_ridership['Date'])
forecasted_ridership = forecasted_ridership.loc[:, ['Date','Ridership', 'Shift']]
df = pd.merge(df, forecasted_ridership, how='left', on=['Date','Shift'])


# In[15]:


forecasted_ridership.head()


# In[16]:


df.sort_values(by=['Date', 'Shift'], ascending=False, inplace=True)
tot_revenue = df['Rides Revenue'] + df['Food Revenue'] + df['Items Revenue']
df.insert(2, 'Total Revenue', tot_revenue)
df.rename(columns = {'riders':'Actual_Ridership', 'Ridership':'Forecasted_Ridership'}, inplace=True)
df['Forecasted_Ridership'] = round(df['Forecasted_Ridership'], 0)


# # Adding Pseudo Revenue

# In[17]:


filename = "WB_revenue.csv"
WB_pseudo_revenue = pd.read_csv(filename, sep = None, parse_dates = [0], engine='python')
WB_pseudo_revenue.rename({'TotAmt':'WB Pseudo Revenue'}, axis='columns', inplace=True)
WB_pseudo_revenue.sort_values(by='Date', axis=0, inplace=True)
WB_pseudo_revenue.head()


# In[18]:


filename = "points_revenue.csv"
points_pseudo_revenue = pd.read_csv(filename, sep = None, parse_dates = [0], engine='python')
points_pseudo_revenue.rename({'TotAmt':'Points Pseudo Revenue'}, axis='columns', inplace=True)
points_pseudo_revenue.sort_values(by='Date', axis=0, inplace=True)
points_pseudo_revenue.head()


# In[19]:


df = df.merge(WB_pseudo_revenue,left_on=['Date','Shift'],right_on=['Date','Shift'])
df = df.merge(points_pseudo_revenue,left_on=['Date','Shift'],right_on=['Date','Shift'])
df['Pseudo Rides Revenue'] = df['Points Pseudo Revenue'] + df['WB Pseudo Revenue']
df['Total Pseudo Revenue'] = df['Pseudo Rides Revenue'] + df['Food Revenue'] + df['Items Revenue']
df.head()


# In[20]:


#create department wise total allocation for rides, food, retail, and guest services
df['Rides Staff'] = df['RI25']+df['C0310']+df['C3336']+df['C1440']+df['C1927']+df['C4451']                     + df['C0450']+df['C0709']+df['8']+df['11']+df['23']+df['24']+df['28']                     + df['29']+df['37']+df['41']+df['42']+df['45']


# In[21]:


#create department wise total allocation for rides, food, retail, and guest services
df['Food Staff'] = df['670']+df['661']+df['684']+df['672']+df['686']+df['642'] + df['682']


# In[22]:


#create department wise total allocation for rides, food, retail, and guest services
df['Retail Staff'] = df['580']+df['554']+df['21']+df['576']+df['RE25']+df['561'] + df['556']


# In[23]:


#create department wise total allocation for rides, food, retail, and guest services
df['Guest Services Staff'] = df['120']+df['100']


# In[24]:


export_file_path = "D:/MOA Data/consolidated_df_v7.csv"
df.to_csv (export_file_path, index = None, header=True)


# In[4]:


#reimporting
filename = "consolidated_df_v7.csv"
df = pd.read_csv(filename, sep = None, parse_dates = [0], engine='python')
df



