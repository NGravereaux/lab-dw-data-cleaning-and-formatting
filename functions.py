import pandas as pd
import re

# format col titles:


def format_column_titles(df):
    # Define a function to clean a single column name
    def clean_column(name):
        name = name.strip()  # Remove leading and trailing spaces
        # Replace non-alphanumeric characters with underscores
        name = re.sub(r'[^0-9a-zA-Z]+', '_', name)
        # Replace multiple underscores with a single underscore
        name = re.sub(r'_+', '_', name)
        name = name.lower()  # Convert to lowercase
        return name.strip('_')  # Remove leading and trailing underscores

    # Apply the clean_column function to all column names in the DataFrame
    df.columns = [clean_column(col) for col in df.columns]
    return df.columns

# formatting state column


def replace_st_by_state(df):
    # `st` could be replaced for `state`:
    df.rename(columns={'st': 'state'}, inplace=True)
    return df.columns

# formatting cleaning_unconsistent_values:


def cleaning_unconsistent_values(df):
    # cleaning gender values:
    df['gender'] = df['gender'].replace(['Femal', 'female'], 'F')
    df['gender'] = df['gender'].replace(['Male'], 'M')
    # cleaning state values:
    df['state'] = df['state'].replace(
        {"AZ": "Arizona", "Cali": "California", "WA": "Washington"})
    # cleaning education values:
    df['education'] = df['education'].replace(['Bachelors'], 'Bachelor')
    # cleaning customer_lifetime_value values:
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace(
        '%', '')
    # cleaning vehicle_class values:
    df['vehicle_class'] = df['vehicle_class'].replace(
        ["Sports Car", "Luxury SUV", "Luxury Car"], 'Luxury')
    return (
        df['gender'].value_counts(),
        df['state'].value_counts(),
        df['education'].value_counts(),
        df['customer_lifetime_value'].value_counts(),
        df['vehicle_class'].value_counts()
    )

# formatting data types:
# Customer lifetime value to numeric:


def format_customer_lifetime_value(df):
    df['customer_lifetime_value'] = pd.to_numeric(
        df['customer_lifetime_value'], errors='coerce')
    return df.dtypes


# Number of open complaints formatting:
def number_open_complaints_formatting(df):
    df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(
        lambda x: int(x.split('/')[1]) if pd.notnull(x) else 0)
    return df['number_of_open_complaints'].value_counts()


# Dealing with Null values (Check Unique values, %, Missing values, %, data type):
def unique_and_missing_values_dtype(df):
    # Total lines (total number of rows)
    total_rows = len(df)

    # Non-null counts and data types
    non_null_counts = df.notnull().sum()
    dtypes = df.dtypes

    # Count of unique values
    unique_count = df.nunique()

    # Percentage of unique values
    unique_percentage = (df.nunique() / total_rows) * 100

    # Count of missing values
    missing_count = df.isnull().sum()

    # Percentage of missing values
    missing_percentage = df.isnull().mean() * 100

    # Combine into a DataFrame
    summary = pd.DataFrame({
        'total_lines': total_rows,
        'non-Null_count': non_null_counts,
        'dtype': dtypes,
        'unique_values': unique_count,
        '%_unique': unique_percentage.round(2).astype(str) + '%',
        'missing_values': missing_count,
        '%_missing': missing_percentage.round(2).astype(str) + '%'
    })

    return summary


# dealing with duplicates:
def duplicated_data_checking(df):
    # Print the shape of the DataFrame (number of rows and columns)
    print("\nShape of the DataFrame:\n")
    print(df.shape)

    # Print the count of duplicate rows
    print("\nDuplicate Rows Number:\n")
    print(df.duplicated().sum())


# fill missing values
def fill_missing_values(df):

    # Select categorical and numerical columns
    categorical_data = df.select_dtypes(include=['object', 'category']).columns
    numerical_data = df.select_dtypes(include=['number']).columns

    # Fill missing values in numerical columns with the mean
    for column in numerical_data:
        df[column] = df[column].fillna(df[column].mean())

    # Fill missing values in categorical columns with the mode
    for column in categorical_data:
        if not df[column].mode().empty:  # Check if mode exists
            df[column] = df[column].fillna(df[column].mode()[0])

    return df.shape
