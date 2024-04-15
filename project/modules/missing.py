import pandas as pd
import numpy as np
def summary_details(dataframe,missing_threshold,missing_val_list):

    # dataframe = pd.read_csv(file_path)
    df1 = dataframe.copy()
    null_result = []
    missing_value_count = 0
    null_values = df1.isnull().sum()
    for missing_value in missing_val_list:
        dynamic_missing_value = df1[(df1.loc[:] == '') | (df1.loc[:] == f'{missing_value}')].count()
        null_percent = (null_values + dynamic_missing_value) / len(df1) * 100
        input_ = dict(null_percent)
        # check each column null percent
        for key, value in input_.items():
            if value > missing_threshold:
                values = (key, value)
                null_result.append(values)
        # df = pd.DataFrame(null_result, columns=['COLUMN_NAME', 'MISSING_VALUE_PERCENTAGE'])

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

    df = pd.DataFrame(null_result, columns=['COLUMN_NAME', 'MISSING_VALUE_PERCENTAGE'])

    return f'\n1.MISSING_FEATURE\nMISSING_VALUE_THRESHOLD:{missing_threshold}%\nMISSING_VALUE_PERCENTAGE:\nRESULT:\n{df}\nNUMBER_OF_COLUMN_HAVING_NULL:{num_of_col_having_null}\nOVERALL_MISSING_PERCENTAGE:{total_null_percentage}%'


# summary_details()






















    # # dataframe = pd.read_csv(file_path)
    # df1 = dataframe.copy()
    # null_result = []
    # missing_result = []
    #
    # # Null values percentage
    # null_values = df1.isnull().sum()
    # empty_str = df1[df1.loc[:] == ''].count()
    # null_percent = df1.isnull().sum() + empty_str / len(df1) * 100
    # input_ = dict(null_percent)
    # # check each column null percent
    # for key , value in input_.items():
    #     if value > missing_threshold:
    #         null_result.append({"column":key,"percentage":value})
    # # overall null values and percent
    # row = df1.shape[0]
    # column = df1.shape[1]
    # total_record = row * column
    # total_null_percentage = df1.isnull().sum().sum() / total_record * 100
    #
    # # Missing values
    # for missing_value in missing_val_list:
    #     c = df1[df1.loc[:] == missing_value].count()
    #     missing = (c / len(df1)) * 100
    #     dict_missing = dict(missing)
    #     # check each column MISSING percent
    #     for key_miss , value_miss in dict_missing.items():
    #         if value_miss > missing_threshold :
    #             missing_result.append({"column":key_miss,"percentage":value_miss})
    #     # overall 'MISSING' values and percent
    #     overall_missing_percentage = len(missing_result) / total_record * 100
    #
    # # Number of column having null
    # dictionary = df1.isnull().sum().to_dict()
    # count = [i for i in dictionary.values() if i > 0]
    # num_of_col_having_null = len(count)
    #
    # return f'Missing.py\nExcepted Missing_Value Threshold:{missing_threshold}%\nNull values percentage:result={null_result}\nNumber of column having null:{num_of_col_having_null}\nMissing value percentage:result={missing_result}' \
    #        f'\nOverall null percentage:{total_null_percentage}\nOverall missing percentage:{overall_missing_percentage}'


 # -9999 Values
 #    b = df1[df1.loc[:] == -9999].count()
 #    each = (b / len(df1)) * 100
 #    dict_each = dict(each)
 #    # check each column -9999 percent
 #    for key_ , value_ in dict_each.items():
 #        if value_ > missing_threshold:
 #            result_9999.append({"column":key_,"percentage":value_})
 #    # overall -9999 values and percent
 #    overall_9999_percentage = len(result_9999)/ total_record * 100

# a = df1[df1.loc[:] == -9999].count().sum()
    # b = df1[df1.loc[:] == -9999].count()
    # percentage_9999 = a / 100 * len(df1)
    # each = (b / len(df1)) * 100
    # dict_each = dict(each)
    # for (key_each, value_each), (key, value) in zip(dict_each.items(), input_.items()):
    #     if key_each == key:
    #         if (value + value_each) > missing_threshold:
    #             result.append({"key": key, "value": value})
    #
    # missing_value_percentage = len(result)/df1.shape[0]*100