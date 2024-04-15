import pandas as pd
import numpy as np

def categorical():

    print("categorical")
    df = pd.read_csv("D:\csv_files\diabetes.csv")
    pd.reset_option("max_columns")
    df1 = df.copy()
    df1['Outcome'] = df1.Outcome.astype("bool")
    df1['Outcome'] = df1['Outcome'].replace([1, 0], ['True', 'False'])
    df1["Age"] = np.where(df1["Age"] >= 45, True, False)
    df1["BloodPressure"] = np.where(df1["BloodPressure"] >= 70, True, False)

    # df = pd.read_csv("D:\csv_files\winequality.csv")
    # print(df.head(5))
    # print("Number of Columns:",df.shape[1])
    # print("Number of Records:",df.shape[0])
    #df1 = df.copy()

    count_of_column = {}
    for dataframe in df1:
        result = df1[dataframe].unique()
        length = len(result)
        # print(length)
        threshould = 2
        if length <= threshould:
            count_of_column.update({dataframe:length})
            # print("Column_name:",dataframe,"-Threshould",length)
    print("count of column having lesser than threshold:",len(count_of_column))
    for key , value in count_of_column.items():
        # return f"categorical.py\nCount of column having lesser than threshold:{len(count_of_column)}column name:{key},threshould:{value} \n"
        print("column name:",key,"threshould:",value)

    print(" ")
# categorical()















# data = [["Aravind",22,"Software",1,160.2,"male",-9999,15000],
    #         [None, 33, "",2, -9999, "female",np.NAN,20000],
    #         ["Sudharsan", 22, "DataEngineer",3, 160, "male",-9999,25000],
    #         ["Sujeeth", 23, "DataEngineer",5, 165, "male",np.NAN,27000],
    #         [None, np.NAN, "DataEngineer",4, 160.2, "male",-9999,24000]
    #         ]
    # dataframe = pd.DataFrame(data = data ,
    #                          columns= ["Name","Age","Role","YOE","Height","Gender","-9999","Salary"])
    # print(dataframe)
    # print("\n")
    # # Threshold
    # temp = dataframe.Role.value_counts()
    # dictionary = temp.to_dict()
    # for key in dictionary:
    #     value = dictionary[key]
    #     if value > 2:
    #         print(key)
    # print("\n")
    # df1 = dataframe[["Gender", "Role"]]
    # for col in df1:
    #     temp = df1[col].value_counts()
    #     dictionary = temp.to_dict()
    #     for key in dictionary:
    #         value = dictionary[key]
    #         if value > 2:
    #             print(key)
