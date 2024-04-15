import pandas as pd
import numpy as np


def boolean_func(dataframe , bool_threshold):

    # dataframe = pd.read_csv(file_path)
    pd.reset_option("max_columns")
    df1 = dataframe.copy()
    bool_columns = []
    result = []
    count = 0
    for data in df1:
       expected = 'bool'
       actual = df1[data].dtypes
       if actual == expected:
          bool_columns.append(data)
    for bool in bool_columns:
        df = df1[bool].value_counts()
        false_percent = df[0]/sum(df)*100
        false_count = df[0]
        true_percent = df[1]/sum(df)*100
        true_count = df[1]
        if true_percent <= bool_threshold:
            count += 1
            # value = ({"column name":bool ,"true percentage":true_percent ,"true count":true_count ,"false percentage":false_percent ,"false_count":false_count})
            value = (bool,true_percent,true_count,false_percent,false_count)
            result.append(value)
    DF = pd.DataFrame(data=result , columns=['COLUMN_NAME','TRUE_PERCENTAGE','TRUE_COUNT','FALSE_PERCENTAGE','FALSE_COUNT'])
    return f'\n3.BOOLEAN_FEATURE\nEXCEPTED_BOOLEAN_THRESHOLD:{bool_threshold}% \nNUMBER_OF_COLUMN_NOT_MEETING_TRUE:{count} \nRESULT:\n{DF}'

# boolean_func()