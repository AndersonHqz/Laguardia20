#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Anderson's Capstone Project: Vehicle Crash Analysis in New York State (2019)

# Research Question: Does driving at nighttime result in more bodily injury crashes than daytime? Or does road surface condition have a bigger impact?


# In[ ]:


##-Process Outline--##
#--Compiling data sources--#
#--Data Cleaning--#
#--Data Execution--#
#--Conclusion--#
#--Linked Data Sources--#


# In[2]:


#--Compiling data sources--#
#Three data sources in total, one main source and two other sources used to merge into main source.
#Main data: From Data.NY.Gov (Motor Vehicle Crashes - Case Information: Three Year Window) [filtered down to only 2019].
#Sub data: Sunrise and sunset data in NY for all of 2019 by month.
#Sub data: Geographic Names Information System [GNIS] data which is used to identify geographic locations based on County.


#--Data Cleaning--#
#Merged Sunrise and Sunset data to main source using Time data.This was used to categorize when each crash happened; Daytime or Nighttime.
#Merged GNIS data to main source using County data. This was to apply a geographical data point to be used for visual representation.
#Created a new Count column in main source as it has many useful applications for plotting data.
#Deleted two original columns from main source as they did not add value. Deleted two columns created for merging purposes use only.
#Cleaned column names
#Created a unified injury outcome column with keyword matching


# In[3]:


import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# In[4]:


# Datasets
crashes_df = pd.read_csv(r"C:\Users\RxPills\Documents\LaGuardia\NY_Motor_Vehicle_Crashes_Case_Information_2019.csv")
sunrise_sunset_df = pd.read_csv(r"C:\Users\RxPills\Documents\LaGuardia\Sunrise_Sunset_Times_NY_2019_Data.csv")
gnis_df = pd.read_csv(r"C:\Users\RxPills\Documents\LaGuardia\GNIS_ID_NY_Data.csv")

# Process datetime columns
crashes_df["Crash_Datetime"] = pd.to_datetime(crashes_df["Date"] + " " + crashes_df["Time"], format="%m/%d/%Y %H:%M")
crashes_df["Month"] = crashes_df["Crash_Datetime"].dt.strftime("%B")

# Sunrise/sunset strings converter to datetime.time objects
sunrise_sunset_df["Sunrise"] = pd.to_datetime(sunrise_sunset_df["Sunrise"], format="%H:%M").dt.time
sunrise_sunset_df["Sunset"] = pd.to_datetime(sunrise_sunset_df["Sunset"], format="%H:%M").dt.time

# Lookup dictionary for sunrise/sunset by month
sun_times = sunrise_sunset_df.set_index("Month")[["Sunrise", "Sunset"]].to_dict("index")

# Function to determine if crash occurred during the day or night
def determine_day_night(row):
    month = row["Month"]
    crash_time = row["Crash_Datetime"].time()
    sunrise = sun_times[month]["Sunrise"]
    sunset = sun_times[month]["Sunset"]
    return "Daytime" if sunrise <= crash_time <= sunset else "Nighttime"

# Created Day_Night function column
crashes_df["Day_Night"] = crashes_df.apply(determine_day_night, axis=1)

# Process GNIS_ID column
gnis_df["County"] = gnis_df["County"].str.upper().str.strip()
crashes_df["County Name"] = crashes_df["County Name"].str.upper().str.strip()

# Merged files based on County Name
crashes_df = crashes_df.merge(gnis_df, how="left", left_on="County Name", right_on="County")

# Cleaned GNIS_ID to remove .0 and ensure it's a string
crashes_df["GNIS_ID"] = crashes_df["GNIS_ID"].fillna(0).astype(int).astype(str)
crashes_df.loc[crashes_df["GNIS_ID"] == "0", "GNIS_ID"] = None

# Added a Count column
crashes_df["Count"] = 1


# In[5]:


# Dropped non value adding columns
crashes_df.drop(columns=["Police Report", "DOT Reference Marker Location"], inplace=True)


# In[6]:


# Dropped duplicate data columns resulting from data merging
crashes_df.drop(columns=["Crash_Datetime", "County"], inplace=True)


# In[7]:


# Cleaned column names for consistency/ease
crashes_df.columns = crashes_df.columns.str.strip().str.lower().str.replace(" ", "_")


# In[9]:


# Standardized the column to make matching easier/possible
crashes_df['crash_descriptor'] = crashes_df['crash_descriptor'].str.lower()

# Defined a set of values that indicate bodily injury
injury_keywords = {
    'injury accident',
    'fatal accident',
    'property damage & injury accident'
}

# Created injury_outcome column: True if crash_descriptor matches any injury keyword
crashes_df['injury_outcome'] = crashes_df['crash_descriptor'].isin(injury_keywords)


# In[17]:


#Final columns output
crashes_df.dtypes


# In[ ]:


#--Data Execution--#

#Executed variety of commands to answer the research question based on what the data said and created illustration to communicate the findings.
#Gathered total number of crashes and summarized data in various ways with "Injury Outcome" as underlying factor
#Mean injury to show ratio (%) based on time of day
#Mean injury outcome by road surface condition
#Various plot types to illustrate findings
# Bar plot
# Heatmap plot
# Point plot


# In[10]:


print(crashes_df['injury_outcome'].value_counts())


# In[38]:


# Frequency count
crashes_df['injury_outcome'].value_counts(normalize=True)


# In[32]:


# Mean injury outcome by time of day (Day vs Night)
injury_by_daynight


# In[34]:


# Mean injury outcome by road surface condition
injury_by_road.sort_values('injury_outcome', ascending=False)


# In[64]:


# To create a single side by side figure for both subplots
plt.figure(figsize=(14, 6))

# Plot 1: Harmful crashes by time of day
plt.subplot(1, 2, 1)
sns.barplot(data=injury_by_daynight, x='day_night', y='injury_outcome')
plt.title("Proportion of Harmful Crashes: Day vs Night")
plt.ylabel("Proportion of Harmful Crashes")
plt.ylim(0, 1)

# Plot 2: Harmful crash ratio by road condition
plt.subplot(1, 2, 2)
sns.barplot(data=ratios, x='Condition', y='Harmful Crash Ratio')
plt.title('Harmful Crash Ratio: Dry vs Adverse Conditions')
plt.ylabel("Proportion of Harmful Crashes")
plt.ylim(0, 1)

plt.tight_layout()
plt.show()


# In[58]:


# Heatmap (had to pivot data)
heatmap_data = injury_by_road_daynight.pivot(
    index='road_surface_conditions',
    columns='day_night',
    values='injury_outcome'
)

# Heatmap plot
plt.figure(figsize=(10, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    cmap='YlOrRd',
    fmt=".2f",
    cbar_kws={'label': 'Harmful Crash Proportion'},
    vmin=0, vmax=1
)
plt.title("Heatmap: Harmful Crash Proportion by Road Condition and Time of Day")
plt.ylabel("Road Surface Condition")
plt.xlabel("Time of Day")
plt.tight_layout()
plt.show()


# In[60]:


# Point plot
plt.figure(figsize=(12, 6))
sns.pointplot(
    data=injury_by_road_daynight,
    x='injury_outcome',
    y='road_surface_conditions',
    hue='day_night',
    dodge=True,
    markers=["o", "s"],
    linestyles=""
)
plt.title("Harmful Crash Proportion by Road Condition and Time of Day (Point Plot)")
plt.xlabel("Proportion of Harmful Crashes")
plt.ylabel("Road Surface Condition")
plt.xlim(0, 1)
plt.legend(title='Time of Day')
plt.tight_layout()
plt.show()


# In[ ]:


#--Conclusion--#

#The data clearly shows that oppose to popular belief, daytime driving leads to a higher bodily harm crash ratio than nighttime.
#The data also clearly shows that road surface conditions do not have a bigger impact with more badily harm crashes coming in dry conditions.


# In[44]:


# Filter for non-dry (adverse) road conditions
adverse_conditions_df = crashes_df[crashes_df['road_surface_conditions'].str.lower() != 'dry']

# Calculate harmful crash ratio for adverse conditions
harmful_ratio_adverse = adverse_conditions_df['injury_outcome'].mean()

print(f"Harmful crash ratio (adverse road conditions only): {harmful_ratio_adverse:.2%}")


# In[46]:


# Make road condition lowercase to ensure consistent comparison
crashes_df['road_surface_conditions'] = crashes_df['road_surface_conditions'].str.lower()

# Separate into dry and adverse conditions
dry_df = crashes_df[crashes_df['road_surface_conditions'] == 'dry']
adverse_df = crashes_df[crashes_df['road_surface_conditions'] != 'dry']

# Ratio calculation
dry_ratio = dry_df['injury_outcome'].mean()
adverse_ratio = adverse_df['injury_outcome'].mean()

# Final results displayed
print(f"Harmful crash ratio (Dry conditions):     {dry_ratio:.2%}")
print(f"Harmful crash ratio (Adverse conditions): {adverse_ratio:.2%}")


# In[68]:


# Make day night lowercase to ensure consistent comparison
crashes_df['day_night'] = crashes_df['day_night'].str.lower()

# Separate into day and night dataframes
day_df = crashes_df[crashes_df['day_night'] == 'daytime']
night_df = crashes_df[crashes_df['day_night'] == 'nighttime']

# Ratio calculation
day_ratio = day_df['injury_outcome'].mean()
night_ratio = night_df['injury_outcome'].mean()

# Final results displayed
print(f"Harmful crash ratio (Daytime):   {day_ratio:.2%}")
print(f"Harmful crash ratio (Nighttime): {night_ratio:.2%}")


# In[ ]:


#--Linked Data Sources--#
#https://data.ny.gov/Transportation/Motor-Vehicle-Crashes-Case-Information-Three-Year-/e8ky-4vqe/explore/

#https://www.sunrise-and-sunset.com/en/sun/united-states/new-york-city/2019/january

#https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Civil_Boundaries/MapServer/2

