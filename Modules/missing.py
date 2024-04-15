import pandas as pd
import numpy as np

def summary_details():

    # data = [["Aravind",22,"Software",1,160.2,"male",-9999,15000],
    #         [None, 33, "",2, -9999, "female",np.NAN,20000],
    #         ["Sudharsan", 22, "DataEngineer",3, 160, "male",-9999,25000],
    #         ["Sujeeth", 23, "DataEngineer",5, 165, "male",np.NAN,27000],
    #         [None, np.NAN, "QA",4, 160.2, "male",-9999,24000]
    #         ]
    # dataframe = pd.DataFrame(data = data ,
    #                          columns= ["Name","Age","Role","YOE","Height","Gender","-9999","Salary"])

    df = pd.read_csv("D:\csv_files\winequality.csv")
    temp_dataframe = df.copy()

    # print(dataframe)
    # print("Number of Columns:",dataframe.shape[1])
    # print("Number of Row's:",dataframe.shape[0])

    # 1.Null Values
    null_values = temp_dataframe.isnull().sum()
    # print("Number of null values:",null_values)

    # Null values percentage
    null_percent = temp_dataframe.isnull().sum()/len(temp_dataframe)*100
    # print("Null_Percentage:",null_percent)

    total_null = temp_dataframe.isnull().sum().sum()/len(temp_dataframe)*100
    # print("Null values percentage:",total_null)

    # Null percentage with df
    missing = pd.DataFrame({"column_name":temp_dataframe.columns ,"null_percent":null_percent})
    # print(missing)

    # 2.Missing
    dictionary = temp_dataframe.isnull().sum().to_dict()
    count = [i for i in dictionary.values() if i > 0]
    # print("number of column having null values:",len(count))
    ms = len(count)
    per = ms/len(temp_dataframe)*100
    # print("Percentage of missing null value:",per)

    # 3.-9999
    a = temp_dataframe[temp_dataframe.loc[:] == -9999].count().sum()
    b = temp_dataframe[temp_dataframe.loc[:] == -9999].count()
    over_all = a/100*len(temp_dataframe)
    each = (b / len(temp_dataframe)) * 100
    # print("Percentage of -9999:",over_all)
    # print("Each column percent of -9999:",each)

    return f"missing.py\nNull values percentage:{total_null}\nNumber of column having null values:{len(count)}\nPercentage of -9999:{over_all}\n"
    # for i in df.values:
    #     if i > 0:
    #         print(i)

    # print([[df.index[df.values == i], i] for i in df.values if i > 0])

# summary_details()














# Read CSV
# df = pd.read_csv("D:\csv_files\winequality.csv")
# print(df.head(5))
# print("Number of Columns:",df.shape[1])
# print("Number of Records:",df.shape[0])
#
# # Null values
# print("Number of null values:",df.isnull().sum())
#
# # Missing
# temp = df.copy()
# dictionary = temp.isna().sum().to_dict()
# count = [i for i in dictionary.values() if i > 0]
# print("Missing values:",len(count))

# another way
# count = 0
# for values in dictionary.values():
#     if values > 0:
#         count += 1
#     else:
#         pass

