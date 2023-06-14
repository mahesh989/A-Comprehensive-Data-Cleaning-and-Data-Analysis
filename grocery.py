import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns


#reading
df= pd.read_csv('./Australia_Grocery_2022Sep.csv', sep=',')


df.shape #gives number of rows and columns
df.info()  #provides datatype and respective data info null or not
df.head()  #gives first 5 rows by default
df.tail(10) #gives last 10 rows as we desire 

#Checking Null values
null_cols = df.columns[df.isnull().any()]
null_df = df[null_cols].isnull().sum().to_frame(name='Null Count')\
          .merge(df[null_cols].isnull().mean().mul(100).to_frame(name='Null Percent'), left_index=True, right_index=True)
null_df_sorted = null_df.sort_values(by='Null Count', ascending=False)
print(null_df_sorted)

#drop the column
df.drop(['in_stock','Retail_price'], axis=1, inplace=True)

#drop entries with null values
# Remove rows with null values
df = df.dropna()

#Checking the duplicate entries
df[df.duplicated()].shape[0] # gives number of duplicate entries


distinct_entries = pd.Series(df['Price_per_unit'].value_counts()).sort_values(ascending=True)
# print sorted unique values
print(distinct_entries)


#separate into numerical and categorical values
column_category=df.select_dtypes(include=['object']).columns
print(column_category)

column_numerical = df.select_dtypes(include=np.number).columns.tolist()
print(column_numerical)
# Calculate descriptive statistics for the selected columns
# Select the two numerical columns for analysis
column1 = 'Package_price'
column2 = 'unit_price'
# Calculate descriptive statistics for the selected columns
statistics = df[[column1, column2]].describe()
print(statistics)

# Count the number of entries with unit_price equal to zero
num_zero_unit_prices = (df['unit_price'] == 0).sum()
print("Number of entries with unit_price equal to zero:", num_zero_unit_prices)

#remove the row where unitprice is zero
df = df[df['unit_price'] != 0]




categorical_columns = ['Category', 'Sub_category', 'Product_Group', 'Brand', 'state', 'city']
# Create a subplot with 2 rows and 3 columns
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Flatten the axes array for easy indexing
axes = axes.flatten()

# Plot bar diagrams for each categorical column
for i, column in enumerate(categorical_columns):
    # Count the frequency of each category
    category_counts = df[column].value_counts()

    # Select the top categories based on the specified conditions
    if column == 'Sub_category':
        top_categories = category_counts.head(10)
    elif column == 'Brand':
        top_categories = category_counts.head(10)
    elif column == 'state':
        top_categories = category_counts
    elif column == 'city':
        top_categories = category_counts.head(5)
    else:
        top_categories = category_counts.head(5)

    # Plot the bar diagram
    top_categories.plot(kind='bar', ax=axes[i])
    axes[i].set_title(column)
    axes[i].set_ylabel("Frequency")

# Adjust the spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()




#Relations between categorical and numerical variables
fig, axarr = plt.subplots(1, 2, figsize=(15, 6))
df.groupby('Category')['unit_price'].mean().sort_values(ascending=False).head(10).plot.bar(ax=axarr[0], fontsize=12, color='purple')
axarr[0].set_title("Category vs Unit Price (Avg)", fontsize=18)
axarr[0].set_xticklabels(axarr[0].get_xticklabels(), rotation=45)

df.groupby('Sub_category')['unit_price'].mean().sort_values(ascending=False).head(5).plot.bar(ax=axarr[1], fontsize=12, color='purple')
axarr[1].set_title("Subcategory vs Unit Price (Avg)", fontsize=18)
axarr[1].set_xticklabels(axarr[1].get_xticklabels(), rotation=45)

plt.subplots_adjust(hspace=0.5)
sns.despine()

plt.show()

#average price for each category and each table
average_prices = df.pivot_table(values='unit_price', index='Category', columns='state', aggfunc='mean')
print(average_prices.to_string())




