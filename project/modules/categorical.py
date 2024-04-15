import pandas as pd
import numpy as np

def categorical(dataframe,categorical_threshold):

    # dataframe = pd.read_csv(file_path)
    pd.reset_option("max_columns")
    df1 = dataframe.copy()
    categorical_columns = []
    for data in df1:
        expected1 = 'object'
        expected2 = 'string'
        actual = df1[data].dtypes
        if actual == expected1 or actual == expected2:
            excepted_unique_count = 10
            count = df1[data].unique()
            actual_unique_count = len(count)
            if actual_unique_count < excepted_unique_count :
                categorical_columns.append(data)

    result = []
    for column in categorical_columns:
        res = df1[column].unique()
        length = len(res)
        if length <= categorical_threshold:
            values = (column, length)
            result.append(values)
    DF = pd.DataFrame(result, columns=['COLUMN_NAME', 'THRESHOLD_VALUE'])

    return f'\n2.CATEGORICAL_FEATURES\nEXCEPTED_CATEGORICAL_THRESHOLD:{categorical_threshold}\nNUMBER_COLUMN_LESSERTHAN_THRESHOLD:{len(result)}\nRESULT:\n{DF}'

# categorical()
