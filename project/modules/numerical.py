import pandas as pd
import numpy as np

def outliers_function(dataframe,outlier_threshold):

    # dataframe = pd.read_csv(file_path)
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
        if outliers_percent > outlier_threshold:
            count += 1
            value = (column, outliers_count, outliers_percent)
            result.append(value)
    df = pd.DataFrame(data=result, columns=['COLUMN_NAME', 'COUNT_OF_OUTLIERS', 'OUTLIERS_PERCENTAGE'])

    return f'\n4.NUMERICAL_FEATURES\nEXCEPTED_OUTLIERS_THRESHOLD:{outlier_threshold}%\nNUMBER_OF_COLUMN_GREATERTHAN_THRESHOLD:{count}\nRESULT:\n{df}'


# outliers_function()
