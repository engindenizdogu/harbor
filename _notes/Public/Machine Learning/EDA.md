---
title: Exploratory Data Analysis (EDA)
---
# What is Exploratory Data Analysis (EDA)?
Exploratory Data Analysis (EDA) refers to the critical process of performing initial investigations on data so as to discover patterns, to spot anomalies, to test hypothesis and to check assumptions with the help of summary statistics and graphical representations.
## EDA Checklist
#### 1. Initial Data Inspection
- Load the dataset into a suitable data structure (e.g., pandas DataFrame)
- Check the dimensions of the dataset (.shape, number of rows and columns)
- Display the first and last few rows to get a quick overview
- Get the data types of each column (.info())
- Check for a primary key or unique identifier column
- Get summary statistics for numerical columns (.describe())
- Get a count of unique values for categorical columns
- Check the distribution of the target variable (eg. data['target'].value_counts())

#### 2. Missing Values Analysis
- Identify columns with missing values (data.isna().sum())
- Calculate the percentage of missing values per column
- Visualize the missing data pattern (e.g., using a heatmap or bar chart)
- Consider the potential reasons for the missingness (e.g., MCAR, MAR, MNAR)
- Decide on an initial strategy for handling missing values (e.g., imputation, dropping rows/columns)

#### 3. Univariate Analysis
- For numerical features:
	- Plot histograms or density plots to visualize distributions
	- Plot box plots to identify potential outliers
	- Calculate skewness and kurtosis
- For categorical features:
	- Create bar charts to visualize the frequency of each category
	- Create count plots for categorical columns

#### 4. Bivariate Analysis
- For numerical vs. numerical features:
	- Create scatter plots
	- Compute the correlation matrix (e.g., Pearson, Spearman)
	- Visualize the correlation matrix using a heatmap
- For categorical vs. numerical features:
	- Create box plots or violin plots grouped by the categorical feature
	- Use summary statistics (e.g., mean, median) of the numerical feature for each category
- For categorical vs. categorical features:
	- Create stacked bar charts or mosaic plots
	- Create a contingency table
	- Perform chi-squared test to check for independence

#### 5. Feature Engineering and Hypothesis Generation
- Encode labels for classification problems
- Analyze the relationship between features and the target variable
- Identify potential new features that can be created from existing ones (e.g., date parts, ratios, polynomial features)
- Brainstorm and document hypotheses about the data and potential feature interactions
- Validate the business/domain understanding of the features

#### 6. Data Quality and Consistency Checks
- Check for inconsistencies in data types (e.g., numbers stored as strings)
- Standardize categorical values (e.g., 'USA' vs. 'United States')
- Identify and handle duplicate records
- Check for data entry errors or illogical values (e.g., age = 200)
- Examine date/time features for proper formatting and time zone issues

#### 7. Outlier Detection
- Use visualizations (box plots, scatter plots) to identify outliers
- Use statistical methods (e.g., Z-score, IQR) to flag potential outliers
- Document and decide on a strategy for handling outliers (e.g., removal, capping, transformation)

#### 8. Data Distribution and Scaling
- Check if the dataset is imbalanced
- Check if numerical features are normally distributed
- Consider log or power transformations for skewed data
- Plan for feature scaling (e.g., Standardization or Normalization) if required by the model
- Convert categorical features into numerical features if needed

#### 9. Dimensionality Reduction (Initial Thought)
- Review the number of features
- Consider if there are highly correlated features that can be combined or one can be dropped
- Identify features with very low variance

#### 10. Final Report and Summary
- Document all findings in a clear and concise report
- Summarize key insights, data quality issues, and proposed next steps
- Present the findings to the team and get feedback before moving to the modeling phase.

###### Sources
- [Exploratory Data Analysis for beginners 🔥🔥](https://www.kaggle.com/code/jihenbelhoudi/exploratory-data-analysis-for-beginners#2.-Distribution-plot-for-all-columns:)
- [Exploratory Data Analysis (EDA) checklist - fnl.es](https://fnl.es/Science/Statistics/Exploratory+Data+Analysis+(EDA)+checklist)