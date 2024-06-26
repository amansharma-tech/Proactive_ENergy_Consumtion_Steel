# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics

# Load DataSet
df=pd.read_csv('/content/drive/MyDrive/Project/Steel_industry_data.csv')

"""**Check basic info on the data set**"""

# Displaying the First Five Rows
df.head()

"""Data Description:"""

# DataFrame Dimensions
data_shape = df.shape
data_shape

num_rows = data_shape[0]
num_columns = data_shape[1]
print("Number of Samples:", num_rows)
print("Number of Features:", num_columns)

df.columns

# Descriptive Statistics
df.describe().T

# Display a summary of the DataFrame, including column names, data types, and non-null value counts
df.info()

"""**Exploratory Data Analysis (EDA)**

Pairplots using seaborn
"""

cols = ['Lagging_Current_Reactive.Power_kVarh', 'Leading_Current_Reactive_Power_kVarh', 'CO2(tCO2)',
        'Lagging_Current_Power_Factor', 'Leading_Current_Power_Factor', 'NSM']

sns.pairplot(df, x_vars=cols, y_vars='Usage_kWh', height=3, aspect=1.2, kind='scatter')
plt.show()

"""Average Usage by Week Status

"""

plt.figure(figsize=(10, 7))
sns.barplot(data=df, x="WeekStatus", y="Usage_kWh",errorbar=None)
plt.xlabel("Day of the Week", fontsize=18)
plt.ylabel("Average Usage", fontsize=18)
plt.title("Average Usage by Week Status", fontsize=25)
plt.show()

"""Average Usage by Day of the Week"""

plt.figure(figsize=(10, 7))
sns.barplot(data=df, x="Day_of_week", y="Usage_kWh",errorbar=None)
plt.xlabel("Day of the Week", fontsize=18)
plt.ylabel("Average Usage", fontsize=18)
plt.title("Average Usage by Day of the Week", fontsize=25)
plt.show()

"""Energy Consumption by Week Status and Load Type

"""

sns.barplot(data=df, x="WeekStatus", y="Usage_kWh", hue="Load_Type",errorbar=None)
plt.xlabel("Week Status", fontsize=18)
plt.ylabel("Energy Consumption", fontsize=18)
plt.title("Energy Consumption by Week Status and Load Type", fontsize=25)
plt.legend(title="Load Type", title_fontsize=12)
plt.show()

"""Correlation Matrix """

df.corr()

"""Correlation Heatmap"""

# Visualize the correlation using Heatmap
sns.set(font_scale=0.8)
plt.figure(figsize=(16,12))
sns.heatmap(df.corr(),annot=True)
plt.title(" Correlation", fontsize = 15, color = 'b', pad = 12, loc = 'center')
plt.show()

"""**Handling Missing And Categorical data**"""

# Calculate the number of missing values in each column of the DataFrame
missing_value_counts = df.isna().sum()
missing_value_counts

df.dtypes

df=df.drop(['date'], axis=1)

# Perform one-hot encoding on categorical variables
df = pd.get_dummies(df)

df.head()

"""**Data Preprocessing**

Splitting the DataFrame
"""

#Independent Features
X = df.drop(['Usage_kWh'], axis=1)  
#Dependent Feature/Target
y=df.Usage_kWh

"""Feature Selection

"""

# Feature Selection using SelectKBest and f_regression
from sklearn.feature_selection import SelectKBest,f_regression
y_=y.astype('int')
select_reg =  SelectKBest(k=10, score_func=f_regression).fit(X, y_)

X_Select = select_reg.transform(X)
X_Select.shape

Selected_features = pd.DataFrame({'columns': X.columns,
                              'Kept': select_reg.get_support()})
Selected_features

""" Standardizing the Features"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X_Select)

"""Test-train split"""

# Splitting the Data into Training and Testing Sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("Training Set - X_train shape:", X_train.shape)
print("Testing Set - X_test shape:", X_test.shape)
print("Training Set - y_train shape:", y_train.shape)
print("Testing Set - y_test shape:", y_test.shape)

"""**Linear Regression Model**"""

from sklearn.linear_model import LinearRegression 
lr=LinearRegression()
lr.fit(X_train,y_train)

#The intercept term of the linear model
lr.intercept_

# The coefficients of the linear model
lr.coef_

y_pred=lr.predict(X_test)

lr_model=pd.DataFrame({'Actual Value':y_test,'Predicted Value':y_pred,'Difference':y_test-y_pred})
lr_model[0:5]

"""Model Evaluation"""

print('LinearRegression model')
mean_squared_error=metrics.mean_squared_error(y_test,y_pred)
print('Sqaured mean error', round(np.sqrt(mean_squared_error),2))
print('R squared training',round(lr.score(X_train,y_train),4))
print('R sqaured testing',round(lr.score(X_test,y_test),4) )

"""Actual vs. Predicted Scatter Plot"""

plt.figure(figsize=(10, 7))
plt.scatter(y_test, y_pred)
plt.xlabel("Actual", fontsize=18)
plt.ylabel("Predicted", fontsize=18)
plt.title("Regression Model", fontsize=25)
plt.show()

"""**Ridge Regression Model**"""

from sklearn.linear_model import Ridge
ridge=Ridge(alpha=0.5)
ridge.fit(X_train,y_train)

yridge_pred=ridge.predict(X_test)

ridge_model=pd.DataFrame({'Actual Value':y_test,'Predicted Value':yridge_pred,'Difference':y_test-yridge_pred})
ridge_model[0:5]

"""Model Evaluation"""

print('Ridge Regression Model')
mean_squared_error=metrics.mean_squared_error(y_test,yridge_pred)
print('Sqaured mean error', round(np.sqrt(mean_squared_error),2))
print('R squared training',round(ridge.score(X_train,y_train),4))
print('R sqaured testing',round(ridge.score(X_test,y_test),4) )

"""Actual vs. Predicted Scatter Plot"""

plt.figure(figsize=(10, 7))
plt.scatter(y_test, yridge_pred, color='green')
plt.xlabel("Actual", fontsize=18)
plt.ylabel("Predicted", fontsize=18)
plt.title("Ridge Regression Model", fontsize=25)
plt.show()

"""**Lasso Regression Model** """

from sklearn.linear_model import Lasso
lasso=Lasso(alpha=0.5)
lasso.fit(X_train,y_train)

ylasso_pred=lasso.predict(X_test)

lasso_model=pd.DataFrame({'Actual Value':y_test,'Predicted Value':ylasso_pred,'Difference':y_test-ylasso_pred})
lasso_model[0:5]

"""Model Evaluation"""

print('Lasso Regression Model')
mean_squared_error=metrics.mean_squared_error(y_test,ylasso_pred)
print('Sqaured mean error', round(np.sqrt(mean_squared_error),2))
print('R squared training',round(lasso.score(X_train,y_train),4))
print('R sqaured testing',round(lasso.score(X_test,y_test),4) )

"""Actual vs. Predicted Scatter Plot"""

plt.figure(figsize=(10, 7))
plt.scatter(y_test, ylasso_pred)
plt.xlabel("Actual", fontsize=18)
plt.ylabel("Predicted", fontsize=18)
plt.title("Lasso Regression Model", fontsize=25)
plt.show()

"""
**ElasticNet Regression Model** 
"""

from sklearn.linear_model import ElasticNet
elasticNet=ElasticNet(alpha=0.5)
elasticNet.fit(X_train,y_train)

yelasticNet_pred=elasticNet.predict(X_test)

elasticNet_model=pd.DataFrame({'Actual Value':y_test,'Predicted Value':yelasticNet_pred,'Difference':y_test-yelasticNet_pred})
elasticNet_model[0:5]

"""Model Evaluation"""

print('ElasticNet Regression model')
mean_squared_error=metrics.mean_squared_error(y_test,yelasticNet_pred)
print('Sqaured mean error', round(np.sqrt(mean_squared_error),2))
print('R squared training',round(elasticNet.score(X_train,y_train),4))
print('R sqaured testing',round(elasticNet.score(X_test,y_test),4) )

"""Actual vs. Predicted Scatter Plot"""

plt.figure(figsize=(10, 7))
plt.scatter(y_test, yelasticNet_pred)
plt.xlabel("Actual", fontsize=18)
plt.ylabel("Predicted", fontsize=18)
plt.title("ElasticNet Regression Model", fontsize=25)
plt.show()

"""**Support Vector Regression Model**"""

from sklearn.svm import SVR
regressor = SVR(kernel = 'rbf')
regressor.fit(X, y)

yregressor_pred = regressor.predict(X_test)
regressor_model=pd.DataFrame({'Actual Value':y_test,'Predicted Value':yregressor_pred,'Difference':y_test-yregressor_pred})
regressor_model[0:5]

print('Support Vector Regression Model')
mean_squared_error=metrics.mean_squared_error(y_test,yregressor_pred)
print('Sqaured mean error', round(np.sqrt(mean_squared_error),2))
print('R squared training',round(regressor.score(X_train,y_train),4))
print('R sqaured testing',round(regressor.score(X_test,y_test),4) )

"""Actual vs. Predicted Scatter Plot"""

plt.figure(figsize=(10, 7))
plt.scatter(y_test,yregressor_pred)
plt.xlabel("Actual", fontsize=18)
plt.ylabel("Predicted", fontsize=18)
plt.title("Support Vector Regression Model", fontsize=25)
plt.show()

"""**Regression Models Comparison**"""

# Comparison of Regression Model R2 Scores
models = ['LinearRegression', 'Ridge', 'Lasso', 'ElasticNet', 'SVR']
score = [lr.score(X_test, y_test),
         ridge.score(X_test, y_test),
         lasso.score(X_test, y_test),
         elasticNet.score(X_test, y_test),
         regressor.score(X_test, y_test)]
colors = ['blue', 'green', 'red', 'orange', 'purple']

plt.figure(figsize=(10, 6))
plt.bar(models, score, color=colors)
plt.xlabel('Models',fontsize=12)
plt.ylabel('Scores',fontsize=12)
plt.title('Comparison of Regression Model Scores',fontsize=20)
plt.show()

# Comparison of Regression Models RMSE
rmse = [np.sqrt(metrics.mean_squared_error(y_test, y_pred)),
        np.sqrt(metrics.mean_squared_error(y_test, yridge_pred)),
        np.sqrt(metrics.mean_squared_error(y_test, ylasso_pred)),
        np.sqrt(metrics.mean_squared_error(y_test, yelasticNet_pred)),
        np.sqrt(metrics.mean_squared_error(y_test, yregressor_pred))]

plt.figure(figsize=(10, 6))
plt.bar(models, rmse, color=['cyan', 'lime', 'salmon', 'gold', 'magenta'])
plt.xlabel('Models',fontsize=12)
plt.ylabel('RMSE',fontsize=12)
plt.title('Comparison of Regression Models RMSE',fontsize=20)
plt.show()
