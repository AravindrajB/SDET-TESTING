import pandas as pd
import numpy as np

def outliers_function(outlier_threshold):

    dataframe = pd.read_csv('D:\csv_files\world_population.csv')
    pd.reset_option("max_columns")
    df1 = dataframe.copy()
    count = 0
    numerical_column = []
    for data in df1:
        expected1 = 'int64'
        expected2 = 'float64'
        actual = df1[data].dtypes
        if actual == expected1 or actual == expected2:
            numerical_column.append(data)

    # Outliers
    result = []
    for column in numerical_column:
        df1[column] = sorted(df1[column])
        outliers = []
        q1, q3 = np.percentile(df1[column], [25, 75])
        IQR = q3 - q1
        lower_bound = q1 - (1.5 * IQR)
        upper_bound = q3 + (1.5 * IQR)
        for record in df1[column]:
            if (record < lower_bound) | (record > upper_bound):
                outliers.append(record)
        outliers_count = len(outliers)
        outliers_percent = outliers_count / len(df1[column]) * 100
        # threshold = 3
        aa = pd.DataFrame(columns=['Column name','Count of outliers','Outliers percentage'])
        if outliers_percent > outlier_threshold:
            count += 1
            # value = ({"Column name":column,"Count of outliers":outliers_count,"Outliers percentage":outliers_percent})
            value = [column,outliers_count,outliers_percent]
            result.append(value)
    df = pd.DataFrame(data=result,columns=['COLUMN_NAME', 'COUNT_OF_OUTLIERS', 'OUTLIERS_PERCENTAGE'])
    return f'1.NUMERICAL_FEATURES\nEXCEPTED_OUTLIERS_THRESHOLD:{outlier_threshold}%\nNUMBER_OF_COLUMN_LESSERTHAN_THRESHOLD:{count}\nRESULT:\n{df}'
# print(outliers_function(5))

def categorical(categorical_threshold):

    dataframe = pd.read_csv('D:\csv_files\world_population.csv')
    pd.reset_option("max_columns")
    df1 = dataframe.copy()
    categorical_columns = []
    for data in df1:
        expected = 'str'
        actual = df1[data].dtypes
        if actual == expected:
            excepted_unique_count = 10
            count = df1[data].unique()
            actual_unique_count = len(count)
            if actual_unique_count < excepted_unique_count :
                categorical_columns.append(data)

    count_of_column = {}
    result = []
    for dataframe in df1:
        res = df1[dataframe].unique()
        length = len(res)
        if length <= categorical_threshold:
            count_of_column.update({dataframe:length})
    for key , value in count_of_column.items():
        values = [key,value]
        result.append(values)
    df = pd.DataFrame(result,columns=['COLUMN_NAME','THRESHOLD_VALUE'])

    return f'\n2.CATEGORICAL_FEATURES\nEXCEPTED_CATEGORICAL_THRESHOLD:{categorical_threshold}\nNUMBER_COLUMN_LESSERTHAN_THRESHOLD:{len(count_of_column)}\nRESULT:\n{df}'

# print(categorical(200))


def summary_details(missing_threshold,missing_val_list):

    dataframe = pd.read_csv('D:\csv_files\winequality.csv')
    df1 = dataframe.copy()
    null_result = []
    missing_value_count = 0
    null_values = df1.isnull().sum()
    for missing_value in missing_val_list:
        dynamic_missing_value = df1[(df1.loc[:] == '') | (df1.loc[:] == f'{missing_value}')].count()
        null_percent = (null_values+ dynamic_missing_value) / len(df1) * 100
        input_ = dict(null_percent)
        # check each column null percent
        for key , value in input_.items():
            if value > missing_threshold:
                values = [key,value]
                null_result.append(values)
        df = pd.DataFrame(null_result, columns=['COLUMN_NAME', 'NULL_PERCENTAGE'])

        missing_result_ = dict(dynamic_missing_value)
        for val in missing_result_.values():
            missing_value_count = missing_value_count + val

    # overall null values and percent
    row = df1.shape[0]
    column = df1.shape[1]
    total_record = row * column
    total_null_percentage = (df1.isnull().sum().sum() + missing_value_count) / total_record * 100

    # Number of column having null
    dictionary = df1.isnull().sum().to_dict()
    count = [i for i in dictionary.values() if i > 0]
    num_of_col_having_null = len(count)

    return f'\nMISSING_FEATURE\nMISSING_VALUE_THRESHOLD:{missing_threshold}%\nMISSING_VALUE_PERCENTAGE:\nRESULT:\n{df}\nNUMBER_OF_COLUMN_HAVING_NULL:{num_of_col_having_null}\nOVERALL_MISSING_PERCENTAGE:{total_null_percentage}%'

print(summary_details(1,['white','red']))