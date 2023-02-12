# Package import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

# Importing the data
df = pd.read_csv(
    r'/Users/wsm/Downloads/Mac Documents/Data analysis/Projects/Kaggle car/dirty_car_data')
# Importing backup data
df_backup = pd.read_csv(
    r'/Users/wsm/Downloads/Mac Documents/Data analysis/Projects/Kaggle car/dirty_car_data')

# Exploring the data
df.shape
df.info(show_counts=True)
df.head()

# Let's start by the maker column
# Replacing NA with unknown
df['maker'].fillna('unknown', inplace=True)
# lowercase
df['maker'] = df['maker'].str.lower()
# Remove leading/trailing whitespaces
df['maker'] = df['maker'].str.strip()
# Let's check for the unique values
df['maker'].unique()

# Some maker names are mispelled, for example 'Audii', 'porshe', 'volzwagen', 'peugot'
# First define the list of correct maker names
categories = ['volkswagen', 'mercedes-benz', 'unknown', 'bmw', 'nissan', 'audi',
              'opel', 'renault', 'skoda', 'ford', 'peugeot', 'seat', 'smart',
              'citroen', 'fiat', 'toyota', 'mazda', 'suzuki', 'volvo', 'kia',
              'honda', 'chevrolet', 'hyundai', 'porsche', 'subaru', 'rover',
              'mini', 'jaguar', 'lancia', 'mitsubishi', 'jeep', 'isuzu',
              'alfa-romeo', 'dacia', 'lexus', 'chrysler', 'dodge', 'maserati',
              'tesla', 'infinity', 'hummer', 'bentley', 'lotus', 'land-rover',
              'lamborghini', 'aston-martin', 'rolls-royce']

# Calculate the similarity score between each value in the 'maker' column and each name in 'categories'
scores = df['maker'].apply(
    lambda x: [fuzz.token_sort_ratio(x, name) for name in categories])

# Find the index of the highest similarity score for each value in 'maker'
highest_scores = scores.apply(lambda x: categories[np.argmax(x)])

# Replace values in 'maker' where the similarity score is at least 80
df['maker'] = np.where(scores.apply(
    lambda x: np.max(x) >= 70), highest_scores, df['maker'])

# Check unique values and if the number of unique values is the same as in categories
df['maker'].unique()
len(df['maker'].unique()) == len(categories)


# Now let's move on to the model column
df['model'].info(show_counts=True)
df['model'].head()
# Replace NA with unknown
df['model'].fillna('unknown', inplace=True)
# lowercase
df['model'] = df['model'].str.lower()
# Remove leading/trailing whitespaces
df['model'] = df['model'].str.strip()


# Now let's move on to the manufacture year column
df['manufacture_year'].info(show_counts=True)
df['manufacture_year'].head()
# Replace NA with the median manufacture year of the maker
median_manufacture_year = df.groupby('maker')['manufacture_year'].median()
df['manufacture_year'].fillna(
    df['maker'].map(median_manufacture_year), inplace=True)
# Let's check the range
df.boxplot(column=['manufacture_year'])
plt.show()
# Replace <1900 years with the median of their maker
df.loc[df['manufacture_year'] < 1900,
       'manufacture_year'] = df['maker'].map(median_manufacture_year)
# manufacture_year has a float data type, let's make it int
df['manufacture_year'].dtypes
df['manufacture_year'] = df['manufacture_year'].astype('int')


# Now let's move on to the engine_displacement column
df['engine_displacement'].info(show_counts=True)
df['engine_displacement'].head()
# Remove unit
df['engine_displacement'] = df['engine_displacement'].str.strip('cm')
# Change data type
df['engine_displacement'] = df['engine_displacement'].astype('int')
# Replace 0 with NA
df['engine_displacement'].replace(0, np.nan, inplace=True)
# Replace NA with the median engine_displacement of the maker
median_engine_displacement = df.groupby(
    'maker')['engine_displacement'].median()
df['engine_displacement'].fillna(
    df['maker'].map(median_engine_displacement), inplace=True)
# Let's check the range
df.boxplot(column=['engine_displacement'])
plt.show()
# Replace <49 & >15000 engine_displacement with the median of their maker
df.loc[(df['engine_displacement'] < 49) | (df['engine_displacement'] > 15000),
       'engine_displacement'] = df['maker'].map(median_engine_displacement)
# Change data type
df['engine_displacement'] = df['engine_displacement'].astype('int')


# Now let's move on to the engine_power column
df['engine_power'].info(show_counts=True)
df['engine_power'].head()
# Replace NA with the median maker power
median_engine_power = df.groupby('maker')['engine_power'].median()
df['engine_power'].fillna(
    df['maker'].map(median_engine_power), inplace=True)
# Let's check the range
df.boxplot(column=['engine_power'])
plt.show()
# Replace >750 engine_power with the median of their maker
df.loc[df['engine_power'] > 750,
       'engine_power'] = df['maker'].map(median_engine_power)
# Replace data type
df['engine_power'] = df['engine_power'].astype('int')


# Now let's move on to the transmission column
df['transmission'].info(show_counts=True)
df['transmission'].head()
# Replace NA with unknown
df['transmission'].fillna('unknown', inplace=True)
# lowercase
df['maker'] = df['maker'].str.lower()
# Remove leading/trailing whitespaces
df['maker'] = df['maker'].str.strip()
# Check unique values
df['transmission'].unique()
# Some transmissions are misspelled
# First define the list of correct transmissions
transmissions_categories = ['manual', 'automatic', 'unknown']

# Calculate the similarity score between each value in the 'transmission' column and each tr in 'transmissions_categories'
scores = df['transmission'].apply(
    lambda x: [fuzz.token_sort_ratio(x, tr) for tr in transmissions_categories])

# Find the index of the highest similarity score for each value in 'transmission'
highest_scores = scores.apply(lambda x: transmissions_categories[np.argmax(x)])

# Replace values in 'transmission' where the similarity score is at least 80
df['transmission'] = np.where(scores.apply(
    lambda x: np.max(x) >= 70), highest_scores, df['transmission'])
# Check if True
len(df['transmission'].unique()) == len(transmissions_categories)


# Now let's move on to the fuel_type column
df['fuel_type'].info(show_counts=True)
df['fuel_type'].head()
# Replace NA with unknown
df['fuel_type'].fillna('unknown', inplace=True)
# lowercase
df['fuel_type'] = df['fuel_type'].str.lower()
# Remove leading/trailing whitespaces
df['fuel_type'] = df['fuel_type'].str.strip()
# Check unique values
df['fuel_type'].unique()
# Some rows have the string 'nan' referring to NA, we will replace 'nan' with unknown
df['fuel_type'].replace('nan', 'unknown', inplace=True)


# Now let's move on to the door_count column
df['door_count'].info(show_counts=True)
df['door_count'].head()
df['door_count'].unique()
# Replace 'None' with NA
df['door_count'].replace('None', np.nan, inplace=True)
# Replace NA with the median maker door count
median_door_count = df.groupby('maker')['door_count'].median()
df['door_count'].fillna(
    df['maker'].map(median_door_count), inplace=True)
# Change data type
df['door_count'] = df['door_count'].astype('float').astype('int')
# Replace <2 & >7 dour cunt with the mode of their maker
df.loc[(df['door_count'] < 2) | (df['door_count'] > 6),
       'door_count'] = df['maker'].map(median_door_count)


# Now let's move on to the seat_count column
df['seat_count'].info(show_counts=True)
df['seat_count'].head()
df['seat_count'].unique()
# Replace 'None' with NA
df['seat_count'].replace('None', np.nan, inplace=True)
# Replace NA with the median maker seat count
median_seat_count = df.groupby('maker')['seat_count'].median()
df['seat_count'].fillna(
    df['maker'].map(median_seat_count), inplace=True)
# Change data type
df['seat_count'] = df['seat_count'].astype('float').astype('int')
# Replace <2 & >27 seat cunt with the mode of their maker
df.loc[(df['seat_count'] < 2) | (df['seat_count'] > 27),
       'seat_count'] = df['maker'].map(median_seat_count)


# Time for duplicates
# Dropping complete duplicate rows
df.drop_duplicates(inplace=True)
# Dropping duplicate rows having a difference only in seat_count or door_count
df.drop_duplicates(subset=['maker', 'model', 'manufacture_year', 'engine_displacement',
                   'engine_power', 'transmission', 'fuel_type'], keep=False, inplace=True)

# Dropping rows with no maker and no model
df = df[~((df['maker'] == 'unknown') & (df['model'] == 'unknown'))]

# Adding engine size in liters and engine power in hp
df['engine_size_liter'] = round(df['engine_displacement']/1000, 1)
df['engine_power_hp'] = round(df['engine_power'] * 1.34102).astype('int')

# Renaming columns
df = df.rename(columns={'engine_power': 'engine_power_kw',
               'engine_displacement': 'engine_displacement_cc'})

# Reordering columns
df = df[['maker', 'model', 'manufacture_year', 'engine_displacement_cc',
         'engine_size_liter', 'engine_power_kw', 'engine_power_hp',
         'transmission', 'fuel_type', 'door_count', 'seat_count']]

# Sorting the data by maker, model, and manufacture year ascending
df.sort_values(by=['maker', 'model', 'manufacture_year'],
               ascending=True, inplace=True)

# index
df.reset_index(drop=True, inplace=True)

pd.set_option('display.max_columns', None)
print(df.head(5))
df.info(show_counts=True)

# Exporting cleaned data
df.to_csv('car_data_cleaned', index=False)
