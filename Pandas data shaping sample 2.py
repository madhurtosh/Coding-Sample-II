import re
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_rows', 25)
pd.set_option('display.max_columns', 500)
###############################################
# Bringing together "STATE" data at Daily Level
###############################################

os. chdir("D:/MOA Data/Original Data")
budget = pd.read_csv('Budget.csv')
calendar = pd.read_csv('Calendar.csv')
weather = pd.read_csv('Weather.csv')

budget = budget.drop(columns = ['BudgetID','Label'])
budget = budget[budget['Code']!='11']
#This is the forecasted ridership in absolute numbers, not $ value
budget.columns = ['Date','Forecasted_ridership','LocationId']
 
budget2 = budget.groupby('Date')['Forecasted_ridership'].sum().reset_index()
budget2['Date'] = pd.to_datetime(budget2['Date'])

calendar['Date'] = pd.to_datetime(calendar['Date'])

weather['Date'] = pd.to_datetime(weather['Date'])
weather = weather.iloc[:, [1,2,3,4,5,6,7]]

calendar = calendar.iloc[:, [0,3]] # Consider only date and holiday flag
calendar.columns = ['Date','isHoliday']
calendar['isHoliday'] = calendar['isHoliday'].replace(np.NaN,0)

df = pd.merge(budget2, calendar, on='Date')
df = pd.merge(df, weather, on='Date')
df = df.drop(columns = ['Ave_TMaxF','Ave_TMinF'])

df['Month'] = df['Date'].dt.month
df['Month_no'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.dayofweek
df['DayofWeek'] = df['Date'].dt.dayofweek

#Convert Day and Week variables to one-hot encoding
df = pd.get_dummies(df, columns = ['Month_no', 'Day'])

os. chdir("D:/MOA Data/State and forecasted ridership")
df.to_csv('Forecasted_Ridership_State_Daily level.csv')

##############################################
# Dividing forecasted ridership at Shift Level
##############################################

actual_ridership = pd.read_csv('ridership_shift.csv') #Actual shift level ridership historically

group1 = actual_ridership[actual_ridership['DayofWeek'] <= 3] # Monday to Thursday
group2 = actual_ridership[actual_ridership['DayofWeek'] == 4] # Friday
group3 = actual_ridership[actual_ridership['DayofWeek'] == 5] # Saturday
group4 = actual_ridership[actual_ridership['DayofWeek'] == 6] # Sunday

group1_AM = group1[group1['shift'] == 0]
group1_AM_average = np.mean(group1_AM['riders'])
group1_PM = group1[group1['shift'] == 1]
group1_PM_average = np.mean(group1_PM['riders'])

group2_AM = group2[group2['shift'] == 0]
group2_AM_average = np.mean(group2_AM['riders'])
group2_PM = group2[group2['shift'] == 1]
group2_PM_average = np.mean(group2_PM['riders'])

group3_AM = group3[group3['shift'] == 0]
group3_AM_average = np.mean(group3_AM['riders'])
group3_PM = group3[group3['shift'] == 1]
group3_PM_average = np.mean(group3_PM['riders'])

group4_AM = group4[group4['shift'] == 0]
group4_AM_average = np.mean(group4_AM['riders'])
group4_PM = group4[group4['shift'] == 1]
group4_PM_average = np.mean(group4_PM['riders'])

group1_ratio = (group1_AM_average/group1_PM_average)
group2_ratio = (group2_AM_average/group2_PM_average)
group3_ratio = (group3_AM_average/group3_PM_average)
group4_ratio = (group4_AM_average/group4_PM_average)

df.columns

df1 = df[df['DayofWeek'] <= 3]
df2 = df[df['DayofWeek'] == 4]
df3 = df[df['DayofWeek'] == 5]
df4 = df[df['DayofWeek'] == 6]

df1['AM_Ridership'] = df1['Ridership'] * group1_ratio / (group1_ratio + 1)
df1['PM_Ridership'] = df1['Ridership'] / (group1_ratio + 1)

df2['AM_Ridership'] = df2['Ridership'] * group2_ratio / (group2_ratio + 1)
df2['PM_Ridership'] = df2['Ridership'] / (group2_ratio + 1)

df3['AM_Ridership'] = df3['Ridership'] * group3_ratio / (group3_ratio + 1)
df3['PM_Ridership'] = df3['Ridership'] / (group3_ratio + 1)

df4['AM_Ridership'] = df4['Ridership'] * group4_ratio / (group4_ratio + 1)
df4['PM_Ridership'] = df4['Ridership'] / (group4_ratio + 1)

df = df1.append([df2,df3,df4])
df2 = pd.melt(df, id_vars='Date',value_vars = ['AM_Ridership','PM_Ridership'])

df2.columns = ['Date','Shift','Ridership']
df2['Date'] = pd.to_datetime(df2['Date'])

df2['DayofWeek'] = df2['Date'].dt.dayofweek
df2['Month'] = df2['Date'].dt.month
df2 = pd.get_dummies(df2, columns = ['DayofWeek','Month'])

df2['Shift'] = df2['Shift'].replace('AM_Ridership',0)
df2['Shift'] = df2['Shift'].replace('PM_Ridership',1)
df2 = df2.sort_values(by = ['Date'])

df2 = pd.merge(df2,calendar, how='left' ,on='Date')
df2 = pd.merge(df2,weather, how='left', on='Date')
df2 = df2.drop(columns = ['Ave_TMaxF','Ave_TMinF'])

df2.to_csv('Forecasted_Ridership_State_Shift level.csv')


###############################################
# Dividing forecasted ridership at Hourly Level
###############################################

os. chdir("D:/MOA Data/Ridership")
hourly_actual_ridership = pd.read_csv('Ridership_Hourly.csv') #Actual hourly ridership historically

hourly_actual_ridership['Date'] = pd.to_datetime(hourly_actual_ridership['Date'])
hourly_actual_ridership['DayofWeek'] = hourly_actual_ridership['Date'].dt.dayofweek

group1 = hourly_actual_ridership[hourly_actual_ridership['DayofWeek'] <= 3] # Monday to Thursday
group2 = hourly_actual_ridership[hourly_actual_ridership['DayofWeek'] == 4] # Friday
group3 = hourly_actual_ridership[hourly_actual_ridership['DayofWeek'] == 5] # Saturday
group4 = hourly_actual_ridership[hourly_actual_ridership['DayofWeek'] == 6] # Sunday

group1_ratio = group1.groupby('Hour').TotalUsers.sum()
group2_ratio = group2.groupby('Hour').TotalUsers.sum()
group3_ratio = group3.groupby('Hour').TotalUsers.sum()
group4_ratio = group4.groupby('Hour').TotalUsers.sum()


df.columns

df1 = df[df['DayofWeek'] <= 3]
df2 = df[df['DayofWeek'] == 4]
df3 = df[df['DayofWeek'] == 5]
df4 = df[df['DayofWeek'] == 6]

df1['Hour9_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[9] / group1_ratio.sum())
df1['Hour10_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[10] / group1_ratio.sum())
df1['Hour11_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[11] / group1_ratio.sum())
df1['Hour12_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[12] / group1_ratio.sum())
df1['Hour13_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[13] / group1_ratio.sum())
df1['Hour14_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[14] / group1_ratio.sum())
df1['Hour15_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[15] / group1_ratio.sum())
df1['Hour16_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[16] / group1_ratio.sum())
df1['Hour17_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[17] / group1_ratio.sum())
df1['Hour18_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[18] / group1_ratio.sum())
df1['Hour19_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[19] / group1_ratio.sum())
df1['Hour20_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[20] / group1_ratio.sum())
df1['Hour21_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[21] / group1_ratio.sum())
df1['Hour22_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[22] / group1_ratio.sum())
df1['Hour23_forecastged_ridership'] = df1['Forecasted_ridership']*(group1_ratio[23] / group1_ratio.sum())
df2['Hour9_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[9] / group1_ratio.sum())
df2['Hour10_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[10] / group1_ratio.sum())
df2['Hour11_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[11] / group1_ratio.sum())
df2['Hour12_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[12] / group1_ratio.sum())
df2['Hour13_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[13] / group1_ratio.sum())
df2['Hour14_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[14] / group1_ratio.sum())
df2['Hour15_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[15] / group1_ratio.sum())
df2['Hour16_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[16] / group1_ratio.sum())
df2['Hour17_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[17] / group1_ratio.sum())
df2['Hour18_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[18] / group1_ratio.sum())
df2['Hour19_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[19] / group1_ratio.sum())
df2['Hour20_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[20] / group1_ratio.sum())
df2['Hour21_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[21] / group1_ratio.sum())
df2['Hour22_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[22] / group1_ratio.sum())
df2['Hour23_forecastged_ridership'] = df2['Forecasted_ridership']*(group1_ratio[23] / group1_ratio.sum())
df3['Hour9_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[9] / group1_ratio.sum())
df3['Hour10_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[10] / group1_ratio.sum())
df3['Hour11_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[11] / group1_ratio.sum())
df3['Hour12_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[12] / group1_ratio.sum())
df3['Hour13_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[13] / group1_ratio.sum())
df3['Hour14_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[14] / group1_ratio.sum())
df3['Hour15_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[15] / group1_ratio.sum())
df3['Hour16_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[16] / group1_ratio.sum())
df3['Hour17_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[17] / group1_ratio.sum())
df3['Hour18_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[18] / group1_ratio.sum())
df3['Hour19_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[19] / group1_ratio.sum())
df3['Hour20_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[20] / group1_ratio.sum())
df3['Hour21_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[21] / group1_ratio.sum())
df3['Hour22_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[22] / group1_ratio.sum())
df3['Hour23_forecastged_ridership'] = df3['Forecasted_ridership']*(group1_ratio[23] / group1_ratio.sum())
df4['Hour9_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[9] / group1_ratio.sum())
df4['Hour10_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[10] / group1_ratio.sum())
df4['Hour11_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[11] / group1_ratio.sum())
df4['Hour12_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[12] / group1_ratio.sum())
df4['Hour13_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[13] / group1_ratio.sum())
df4['Hour14_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[14] / group1_ratio.sum())
df4['Hour15_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[15] / group1_ratio.sum())
df4['Hour16_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[16] / group1_ratio.sum())
df4['Hour17_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[17] / group1_ratio.sum())
df4['Hour18_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[18] / group1_ratio.sum())
df4['Hour19_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[19] / group1_ratio.sum())
df4['Hour20_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[20] / group1_ratio.sum())
df4['Hour21_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[21] / group1_ratio.sum())
df4['Hour22_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[22] / group1_ratio.sum())
df4['Hour23_forecastged_ridership'] = df4['Forecasted_ridership']*(group1_ratio[23] / group1_ratio.sum())

df = df1.append([df2,df3,df4])
df3 = pd.melt(df, id_vars='Date',
              value_vars = ['Hour9_forecastged_ridership',
                            'Hour10_forecastged_ridership',
                            'Hour11_forecastged_ridership',
                            'Hour12_forecastged_ridership',
                            'Hour13_forecastged_ridership',
                            'Hour14_forecastged_ridership',
                            'Hour15_forecastged_ridership',
                            'Hour16_forecastged_ridership',
                            'Hour17_forecastged_ridership',
                            'Hour18_forecastged_ridership',
                            'Hour19_forecastged_ridership',
                            'Hour20_forecastged_ridership',
                            'Hour21_forecastged_ridership',
                            'Hour22_forecastged_ridership',
                            'Hour23_forecastged_ridership'])

df3.columns = ['Date','Hour','Forecasted_ridership']
#Extract Hour (int) from the string 'Hourxx_forecastged_ridership'
#using Regex library
df3['Hour'] = df3['Hour'].transform(lambda x: int(re.findall(r'\d+',x)[0]))


df3['Date'] = pd.to_datetime(df3['Date'])
df3 = df3.sort_values(by = ['Date'])

df3 = pd.merge(df3,calendar, how='left' ,on='Date')
df3 = pd.merge(df3,weather, how='left', on='Date')
df3 = df3.drop(columns = ['Ave_TMaxF','Ave_TMinF'])

df3['DayofWeek'] = df3['Date'].dt.dayofweek
df3['Day'] = df3['Date'].dt.dayofweek
df3['Month'] = df3['Date'].dt.month
df3['Month_no'] = df3['Date'].dt.month
df3['Hour_no'] = df3['Hour']
df3 = pd.get_dummies(df3, columns = ['Day','Month_no', 'Hour'])

os. chdir("D:/MOA Data/State and forecasted ridership")
df3.to_csv('Forecasted_Ridership_State_Hourly_level.csv')
