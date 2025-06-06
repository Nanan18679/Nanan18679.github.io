# -*- coding: utf-8 -*-
"""BANA 212 Group 4A Fertility Data Final Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ySos2_GECWhGMSRin1JbLCdEUUswRYWb

# Data Cleaning

## Obtain the needed datasets for analysis
"""

import pandas as pd

indicator_df = pd.read_csv('WBData Indicator NameList.csv')
indicator_df

df_fert = pd.read_csv('WBData Fertility Rates.csv')
df_fert = df_fert.drop(columns=['Country Code', 'Indicator Code'], errors='ignore')
df_fert

df_fert.set_index(['Country Name', 'Indicator Name'], inplace=True)

year_columns = [str(year) for year in range(1972, 2023)]
data_years = df_fert[year_columns]

data_years.reset_index(inplace=True)

# Melt the dataframe to move years into a single column
melted_data_fert = data_years.melt(id_vars=['Country Name', 'Indicator Name'],
                               var_name='Year', value_name='Value')

# Pivot the melted dataframe to set indicators as columns
pivoted_data_fert = melted_data_fert.pivot_table(index=['Country Name', 'Year'],
                                        columns='Indicator Name',
                                        values='Value')

final_data_fert = pivoted_data_fert.reset_index()

final_data_fert = final_data_fert[final_data_fert['Year'] != 'index']
final_data_fert

"""## Download raw dataset, merge with the needed indicators and format to analyze"""

df = pd.read_csv('WBData.csv')
df

merged_df = pd.merge(df, indicator_df, on='Indicator Name', how='inner')
merged_df = merged_df.drop(columns=['2023','Category'], errors='ignore')
merged_df

merged_df.set_index(['Country Name', 'Country Code', 'Country Region', 'Indicator Name'], inplace=True)

year_columns = [str(year) for year in range(1972, 2023)]
data_years = merged_df[year_columns]
data_years.reset_index(inplace=True)

data_years.reset_index(inplace=True)

melted_data = data_years.melt(id_vars=['Country Name', 'Country Code', 'Country Region', 'Indicator Name'],
                               var_name='Year', value_name='Value')

pivoted_data = melted_data.pivot_table(index=['Country Name', 'Country Code', 'Country Region', 'Year'],
                                        columns='Indicator Name',
                                        values='Value')

final_data = pivoted_data.reset_index()
final_data = final_data[final_data['Year'] != 'index']
final_data

final_data = pd.merge(final_data, final_data_fert, on=['Country Name', 'Year'], how='inner')
final_data

columns_to_drop = final_data.columns[final_data.isnull().sum() > 2000]
final_data = final_data.drop(columns=columns_to_drop)
final_data

final_data.isnull().sum()

"""## Create sub-dataframes for Categories"""

indicator_df['Category'].unique()

# Adjust this to match the exact name of the fertility rate indicator
fertility_indicator_name = 'Fertility rate, total (births per woman)_y'

# Filter for the "Fertility Rate" row with the correct indicator name
fertility_rate_row = indicator_df[indicator_df['Indicator Name'] == fertility_indicator_name]

# Build each category dataframe, ensuring each one includes the "Fertility Rate" indicator
soc_norms_indicator_df = pd.concat([indicator_df[indicator_df['Category'] == 'Social Norms'], fertility_rate_row]).drop_duplicates()
agr_urb_indicator_df = pd.concat([indicator_df[indicator_df['Category'] == 'Agriculture/Urbanization'], fertility_rate_row]).drop_duplicates()
health_indicator_df = pd.concat([indicator_df[indicator_df['Category'] == 'Healthcare'], fertility_rate_row]).drop_duplicates()
tech_indicator_df = pd.concat([indicator_df[indicator_df['Category'] == 'Technology'], fertility_rate_row]).drop_duplicates()
economy_indicator_df = pd.concat([indicator_df[indicator_df['Category'] == 'Economic Development'], fertility_rate_row]).drop_duplicates()
education_indicator_df = pd.concat([indicator_df[indicator_df['Category'] == 'Education'], fertility_rate_row]).drop_duplicates()

dataframes = {
    "soc_norms": soc_norms_indicator_df,
    "agr_urb": agr_urb_indicator_df,
    "health": health_indicator_df,
    "tech": tech_indicator_df,
    "economy": economy_indicator_df,
    "education": education_indicator_df
}

for key, indicator_df in dataframes.items():
    merged_df_i = pd.merge(df, indicator_df, on='Indicator Name', how='inner')
    merged_df_i = merged_df_i.drop(columns=['2023', 'Category'], errors='ignore')
    merged_df_i.set_index(['Country Name', 'Country Code', 'Country Region', 'Indicator Name'], inplace=True)

    year_columns_i = [str(year) for year in range(1972, 2023)]
    data_years_i = merged_df_i[year_columns_i]
    data_years_i.reset_index(inplace=True)

    melted_data_i = data_years_i.melt(id_vars=['Country Name', 'Country Code', 'Country Region', 'Indicator Name'],
                                  var_name='Year', value_name='Value')
    pivoted_data_i = melted_data_i.pivot_table(index=['Country Name', 'Country Code', 'Country Region', 'Year'],
                                           columns='Indicator Name', values='Value')

    final_data_i = pivoted_data_i.reset_index()
    final_data_i = final_data_i[final_data_i['Year'] != 'index']
    final_data_i = pd.merge(final_data_i, final_data_fert, on=['Country Name', 'Year'], how='inner')

    columns_to_drop_i = final_data_i.columns[final_data_i.isnull().sum() > 2000]
    final_data_i = final_data_i.drop(columns=columns_to_drop_i)

    globals()[f"final_data_{key}"] = final_data_i

    print(f"final_data_{key} created with {final_data_i.shape[0]} rows and {final_data_i.shape[1]} columns.")

final_data_soc_norms = final_data_soc_norms.rename(columns={'Fertility rate, total (births per woman)_y': 'Fertility rate, total (births per woman)'})

final_data_soc_norms

"""## Create sub-dataframes for regions & countries"""

regions_data = final_data.loc[final_data['Country Region'] == 'Region']
regions_data_soc_norms = final_data_soc_norms.loc[final_data_soc_norms['Country Region'] == 'Region']
regions_data_agr_urb = final_data_agr_urb.loc[final_data_agr_urb['Country Region'] == 'Region']
regions_data_health = final_data_health.loc[final_data_health['Country Region'] == 'Region']
regions_data_tech = final_data_tech.loc[final_data_tech['Country Region'] == 'Region']
regions_data_economy = final_data_economy.loc[final_data_economy['Country Region'] == 'Region']
regions_data_education = final_data_education.loc[final_data_education['Country Region'] == 'Region']

countries_data = final_data.loc[final_data['Country Region'] == 'Country']
countries_data_soc_norms = final_data_soc_norms.loc[final_data_soc_norms['Country Region'] == 'Country']
countries_data_agr_urb = final_data_agr_urb.loc[final_data_agr_urb['Country Region'] == 'Country']
countries_data_health = final_data_health.loc[final_data_health['Country Region'] == 'Country']
countries_data_tech = final_data_tech.loc[final_data_tech['Country Region'] == 'Country']
countries_data_economy = final_data_economy.loc[final_data_economy['Country Region'] == 'Country']
countries_data_education = final_data_education.loc[final_data_education['Country Region'] == 'Country']

"""# Visualizations"""

import matplotlib.pyplot as plt

regions_to_include = [
    "Africa Eastern and Southern", "Africa Western and Central", "Arab World",
    "East Asia & Pacific", "Europe & Central Asia", "European Union",
    "Latin America & Caribbean", "Middle East & North Africa", "North America",
    "South Asia", "Sub-Saharan Africa", "World"
]
regions_data_filtered = regions_data[regions_data['Country Name'].isin(regions_to_include)]

plt.figure(figsize=(14, 8))
for region in regions_data_filtered['Country Name'].unique():
    region_data = regions_data_filtered[regions_data_filtered['Country Name'] == region]
    plt.plot(region_data['Year'], region_data['Fertility rate, total (births per woman)_y'], label=region)

plt.xticks(rotation=45)
plt.legend(title='Regions', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlabel('Year')
plt.ylabel('Fertility Rate')
plt.title('Linear Progression of Each Region Over Time')
plt.legend(title='Regions')
plt.tight_layout()
plt.show()

import seaborn as sns

plt.figure(figsize=(12, 8))

for region in regions_data_filtered['Country Name'].unique():
    region_data = regions_data_filtered[regions_data_filtered['Country Name'] == region]
    sns.kdeplot(region_data['Fertility rate, total (births per woman)_y'], label=region, fill=True)

plt.xlabel('Fertility Rate')
plt.ylabel('Density')
plt.title('Density Plot of Fertility Rate by Region')
plt.legend(title='Regions', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

category_dataframes = [
    (final_data_soc_norms, "Social Norms"),
    (final_data_agr_urb, "Agriculture/Urbanization"),
    (final_data_health, "Healthcare"),
    (final_data_tech, "Technology"),
    (final_data_economy, "Economic Development"),
    (final_data_education, "Education")
]

fertility_column = 'Fertility rate, total (births per woman)'

fig, axes = plt.subplots(6, 1, figsize=(8, 36))

for ax, (df, title) in zip(axes, category_dataframes):
    numeric_df = df.select_dtypes(include='number')
    correlation_with_fertility = numeric_df.corr()[[fertility_column]].dropna()
    correlation_with_fertility = correlation_with_fertility.sort_values(by=fertility_column, ascending=False)
    sns.heatmap(correlation_with_fertility, annot=True, cmap='coolwarm', cbar=True, ax=ax)
    ax.set_title(f"Correlation of Each Indicator with Fertility Rate ({title})")

plt.tight_layout()
plt.show()

"""# Regression Model"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SequentialFeatureSelector
import numpy as np

"""### Social Norms"""

final_data_soc_norms = final_data_soc_norms.dropna()

# Ensure relevant features and target are selected
features = final_data_soc_norms.drop(columns = ['Fertility rate, total (births per woman)',
                                                'Country Name','Country Code','Country Region','Year',
                                               'Fertility rate, total (births per woman)_x'])
target = final_data_soc_norms['Fertility rate, total (births per woman)']

# Scale the features (optional for better numerical stability)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(scaled_features, target)

# Get coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Calculate predictions (fitted values)
predictions = model.predict(scaled_features)

# Analyze performance metrics (optional for insights)
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2 = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

# Apply Sequential Forward Selection (SFS)
sfs = SequentialFeatureSelector(estimator=model, n_features_to_select='auto', direction='forward', cv=5)
sfs.fit(scaled_features, target)

# Get selected features
selected_features = features.columns[sfs.get_support()]
print(f"Selected Features: {selected_features}")

# Create a new dataset with selected features
selected_features_data = features[selected_features]

# Scale the selected features
scaler_selected = StandardScaler()
selected_scaled_features = scaler_selected.fit_transform(selected_features_data )


# Fit the model using the selected features
model.fit(selected_scaled_features, target)

# Get the model coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Make predictions using the same dataset (since you are using the entire dataset)
predictions = model.predict(selected_scaled_features)

# Evaluate model performance
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2_soc_norms = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

"""### Agriculture/ Urbanization"""

final_data_agr_urb = final_data_agr_urb.dropna()

# Define features and target
features = final_data_agr_urb.drop(columns = ['Fertility rate, total (births per woman)',
                                                'Country Name','Country Code','Country Region','Year',
                                               ])
target = final_data_agr_urb['Fertility rate, total (births per woman)']

# Scale the features (optional for better numerical stability)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(scaled_features, target)

# Get coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Calculate predictions (fitted values)
predictions = model.predict(scaled_features)

# Analyze performance metrics (optional for insights)
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2 = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

# Apply Sequential Forward Selection (SFS)
sfs = SequentialFeatureSelector(estimator=model, n_features_to_select='auto', direction='forward', cv=5)
sfs.fit(scaled_features, target)

# Get selected features
selected_features = features.columns[sfs.get_support()]
print(f"Selected Features: {selected_features}")

# Create a new dataset with selected features
selected_features_data = features[selected_features]

# Scale the selected features
scaler_selected = StandardScaler()
selected_scaled_features = scaler_selected.fit_transform(selected_features_data )

# Fit the model using the selected features
model.fit(selected_scaled_features, target)

# Get the model coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Make predictions using the same dataset (since you are using the entire dataset)
predictions = model.predict(selected_scaled_features)

# Evaluate model performance
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2_agr_urb = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

"""### Healthcare"""

final_data_health = final_data_health.dropna()

# Define features and target
features = final_data_health.drop(columns = ['Fertility rate, total (births per woman)',
                                                'Country Name','Country Code','Country Region','Year',
                                               ])
target = final_data_health['Fertility rate, total (births per woman)']

# Scale the features (optional for better numerical stability)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(scaled_features, target)

# Get coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Calculate predictions (fitted values)
predictions = model.predict(scaled_features)

# Analyze performance metrics (optional for insights)
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2 = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

# Apply Sequential Forward Selection (SFS)
sfs = SequentialFeatureSelector(estimator=model, n_features_to_select='auto', direction='forward', cv=5)
sfs.fit(scaled_features, target)

# Get selected features
selected_features = features.columns[sfs.get_support()]
print(f"Selected Features: {selected_features}")

# Create a new dataset with selected features
selected_features_data = features[selected_features]

# Scale the selected features
scaler_selected = StandardScaler()
selected_scaled_features = scaler_selected.fit_transform(selected_features_data )

# Fit the model using the selected features
model.fit(selected_scaled_features, target)

# Get the model coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Make predictions using the same dataset (since you are using the entire dataset)
predictions = model.predict(selected_scaled_features)

# Evaluate model performance
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2_health = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

"""### Technology Development"""

final_data_tech = final_data_tech.dropna()

# Define features and target
features = final_data_tech.drop(columns = ['Fertility rate, total (births per woman)',
                                                'Country Name','Country Code','Country Region','Year',
                                               ])
target = final_data_tech['Fertility rate, total (births per woman)']

# Scale the features (optional for better numerical stability)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(scaled_features, target)

# Get coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Calculate predictions (fitted values)
predictions = model.predict(scaled_features)

# Analyze performance metrics (optional for insights)
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2 = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

# Apply Sequential Forward Selection (SFS)
sfs = SequentialFeatureSelector(estimator=model, n_features_to_select='auto', direction='forward', cv=5)
sfs.fit(scaled_features, target)

# Get selected features
selected_features = features.columns[sfs.get_support()]
print(f"Selected Features: {selected_features}")

# Create a new dataset with selected features
selected_features_data = features[selected_features]

# Scale the selected features
scaler_selected = StandardScaler()
selected_scaled_features = scaler_selected.fit_transform(selected_features_data )

# Fit the model using the selected features
model.fit(selected_scaled_features, target)

# Get the model coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Make predictions using the same dataset (since you are using the entire dataset)
predictions = model.predict(selected_scaled_features)

# Evaluate model performance
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2_tech = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

"""### Economy"""

final_data_economy = final_data_economy.dropna()

# Define features and target
features = final_data_economy.drop(columns = ['Fertility rate, total (births per woman)',
                                                'Country Name','Country Code','Country Region','Year',
                                               ])
target = final_data_economy['Fertility rate, total (births per woman)']

# Scale the features (optional for better numerical stability)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(scaled_features, target)

# Get coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Calculate predictions (fitted values)
predictions = model.predict(scaled_features)

# Analyze performance metrics (optional for insights)
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2 = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

# Apply Sequential Forward Selection (SFS)
sfs = SequentialFeatureSelector(estimator=model, n_features_to_select='auto', direction='forward', cv=5)
sfs.fit(scaled_features, target)

# Get selected features
selected_features = features.columns[sfs.get_support()]
print(f"Selected Features: {selected_features}")

# Create a new dataset with selected features
selected_features_data = features[selected_features]

# Scale the selected features
scaler_selected = StandardScaler()
selected_scaled_features = scaler_selected.fit_transform(selected_features_data )

# Fit the model using the selected features
model.fit(selected_scaled_features, target)

# Get the model coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Make predictions using the same dataset (since you are using the entire dataset)
predictions = model.predict(selected_scaled_features)

# Evaluate model performance
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2_economy = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

"""### Education"""

final_data_education = final_data_education.dropna()

# Define features and target
features = final_data_education.drop(columns = ['Fertility rate, total (births per woman)',
                                                'Country Name','Country Code','Country Region','Year',
                                               ])
target = final_data_education['Fertility rate, total (births per woman)']

# Scale the features (optional for better numerical stability)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(scaled_features, target)

# Get coefficients and intercept
print(f"Intercept: {model.intercept_}")
print(f"Coefficients: {model.coef_}")

# Calculate predictions (fitted values)
predictions = model.predict(scaled_features)

# Analyze performance metrics (optional for insights)
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(target, predictions)
r2_education = r2_score(target, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-Squared: {r2}")

"""### R-Squared Comparison between six categories"""

# Creating a DataFrame to compare R-squared values
data = {
    "Category": ["Social Norms", "Agriculture/Urbanization", "Healthcare", "Technology", "Economy", "Education"],
    "R-Squared": [r2_soc_norms, r2_agr_urb, r2_health, r2_tech, r2_economy, r2_education]
}

r2_comparison_df = pd.DataFrame(data)

# Rank the category
r2_comparison_df = r2_comparison_df.sort_values(by="R-Squared", ascending=False).reset_index(drop=True)

# Print the DataFrame
r2_comparison_df

import matplotlib.pyplot as plt

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Plot the sorted R-squared values
plt.figure(figsize=(10, 6))
plt.bar(r2_comparison_df["Category"], r2_comparison_df["R-Squared"], color=colors)
plt.xlabel("Category")
plt.ylabel("R-Squared Value")
plt.title("R-Squared Comparison by Category")
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

"""# ML Models"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import accuracy_score

from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

# Selecting only numeric columns from countries_data
countries_x = countries_data.select_dtypes(include=['float64', 'int64'])

# Handling missing values by imputing the mean
imputer = SimpleImputer(strategy='mean')
countries_x = imputer.fit_transform(countries_x)

# Extracting the target variable
countries_y = countries_data['Fertility rate, total (births per woman)_y'].values

# Perform k-fold cross-validation
kf = KFold(n_splits=10, shuffle=True, random_state=42)
mean_squared_errors = []

for train_index, test_index in kf.split(countries_x, countries_y):
    x_train, x_test = countries_x[train_index], countries_x[test_index]
    y_train, y_test = countries_y[train_index], countries_y[test_index]

    # Train your model
    model = DecisionTreeRegressor()
    model.fit(x_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(x_test)

    # Calculate mean squared error for this fold
    mse = mean_squared_error(y_test, y_pred)
    mean_squared_errors.append(mse)

# Calculate the mean MSE across all folds
mean_mse = np.mean(mean_squared_errors)
print("Mean Cross-Validated Mean Squared Error:", mean_mse)

"""> Perform feature selection to identify the most significant indicators affecting fertility rates."""

from sklearn.feature_selection import SelectKBest, f_regression

# Perform feature selection
selector = SelectKBest(score_func=f_regression, k='all')
selector.fit(countries_x, countries_y)

# Get feature scores and p-values
feature_scores = selector.scores_
feature_pvalues = selector.pvalues_

# Combine feature names, scores, and p-values into a DataFrame
feature_importance_df = pd.DataFrame({
    'Feature': countries_data.select_dtypes(include=['float64', 'int64']).columns,
    'Score': feature_scores,
    'P-Value': feature_pvalues
})

# Sort by score in descending order
feature_importance_df = feature_importance_df.sort_values(by='Score', ascending=False)
feature_importance_df

"""The feature selection process has identified the most significant indicators affecting fertility rates. The top indicators include:

1. Fertility rate (both `_x` and `_y` versions).
2. Birth rate, crude (per 1,000 people).
3. Population ages 00-04 (both female and male percentages).

These indicators have the highest scores and lowest p-values, indicating their strong relationship with fertility rates.

> Create additional visualizations to explore relationships between indicators and fertility rates.
"""

# Scatter plot for top indicators affecting fertility rates
plt.figure(figsize=(14, 8))

# Selecting top indicators based on feature importance
important_features = feature_importance_df.head(5)['Feature'].values

for feature in important_features:
    if feature != 'Fertility rate, total (births per woman)_y':  # Avoid self-correlation
        plt.scatter(countries_data[feature], countries_data['Fertility rate, total (births per woman)_y'], label=feature, alpha=0.6)

plt.xlabel('Indicator Value')
plt.ylabel('Fertility Rate')
plt.title('Scatter Plot of Top Indicators vs Fertility Rate')
plt.legend(title='Indicators', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

"""The scatter plot visualizes the relationship between the top indicators and fertility rates. Let me know if you need further analysis or additional visualizations.

> apply and compare other machnice learning models

> compare with life expentancy and gdp
"""

# Extracting GDP and Life Expectancy columns for comparison
comparison_columns = ['GDP per capita (current US$)', 'Life expectancy at birth, total (years)', 'Fertility rate, total (births per woman)_y']
comparison_data = countries_data[comparison_columns]

# Drop rows with missing values in the selected columns
comparison_data = comparison_data.dropna()
comparison_data

import seaborn as sns

# Pairplot to visualize relationships between GDP, Life Expectancy, and Fertility Rate
sns.pairplot(comparison_data, diag_kind='kde', kind='scatter', plot_kws={'alpha': 0.6})
plt.suptitle('Relationships Between GDP, Life Expectancy, and Fertility Rate', y=1.02)
plt.show()

"""The pairplot visualizes the relationships between GDP per capita, life expectancy, and fertility rate. Let me know if you need further analysis or specific insights from this data.

>
"""

from sklearn.linear_model import LinearRegression
import numpy as np

# Extract fertility rate and urbanization rate
fertility_rate = countries_data['Fertility rate, total (births per woman)_y']
urbanization_rate = countries_data['Urban population (% of total population)']

# Drop missing values
fertility_urban_data = pd.DataFrame({
    'Fertility Rate': fertility_rate,
    'Urbanization Rate': urbanization_rate
}).dropna()

# Prepare data for linear regression
X = fertility_urban_data['Urbanization Rate'].values.reshape(-1, 1)
y = fertility_urban_data['Fertility Rate'].values

# Perform linear regression
model = LinearRegression()
model.fit(X, y)

# Predict values for the regression line
x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_pred = model.predict(x_range)

# Plot the data and regression line
plt.figure(figsize=(10, 6))
plt.scatter(fertility_urban_data['Urbanization Rate'], fertility_urban_data['Fertility Rate'], alpha=0.6, label='Data Points')
plt.plot(x_range, y_pred, color='red', label='Regression Line')
plt.xlabel('Urbanization Rate (% of total population)')
plt.ylabel('Fertility Rate (births per woman)')
plt.title('Fertility Rate vs Urbanization Rate with Regression Line')
plt.legend()
plt.show()

"""The scatter plot of fertility rate versus urbanization rate, along with the linear regression line, has been displayed. Let me know if you need further analysis or adjustments.

> create kmeans clustering with fertility rate on y axis vs gdp of counties on x axis
"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Extract required data for clustering
gdp = countries_data['GDP per capita (current US$)']
fertility_rate = countries_data['Fertility rate, total (births per woman)_y']

# Drop missing values
clustering_data = pd.DataFrame({
    'GDP': gdp,
    'Fertility Rate': fertility_rate
}).dropna()

# Prepare data for clustering
X = clustering_data.values

# Apply KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X)

# Add cluster labels to the data
clustering_data['Cluster'] = clusters

# Plot the clustering results
plt.figure(figsize=(10, 6))
sns.scatterplot(x=clustering_data['GDP'], y=clustering_data['Fertility Rate'], hue=clustering_data['Cluster'], palette='viridis', s=50)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='red', marker='X', s=200, label='Centroids')
plt.xlabel('GDP per capita (current US$)')
plt.ylabel('Fertility Rate (births per woman)')
plt.title('KMeans Clustering: Fertility Rate vs GDP')
plt.legend(title='Cluster')
plt.show()

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Extract required data for clustering
gdp = countries_data['Age dependency ratio (% of working-age population)']
fertility_rate = countries_data['Fertility rate, total (births per woman)_y']

# Drop missing values
clustering_data = pd.DataFrame({
    'GDP': gdp,
    'Fertility Rate': fertility_rate
}).dropna()

# Prepare data for clustering
X = clustering_data.values

# Apply KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X)

# Add cluster labels to the data
clustering_data['Cluster'] = clusters

# Plot the clustering results
plt.figure(figsize=(10, 6))
sns.scatterplot(x=clustering_data['GDP'], y=clustering_data['Fertility Rate'], hue=clustering_data['Cluster'], palette='viridis', s=50)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='red', marker='X', s=200, label='Centroids')
plt.xlabel('Age dependency ratio (% of working-age population)')
plt.ylabel('Fertility Rate (births per woman)')
plt.title('KMeans Clustering: Fertility Rate vs Age dependency ratio (% of working-age population)')
plt.legend(title='Cluster')
plt.show()

