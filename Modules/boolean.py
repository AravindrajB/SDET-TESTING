import pandas as pd
import numpy as np

def boolean():

    print("boolean.py")
    # Read csv
    df = pd.read_csv("D:\csv_files\diabetes.csv")
    pd.reset_option("max_columns")
    # print(df.head())
    # print("Rows and columns:",df.shape)
    # df.info()

    # change to boolean type
    df1 = df.copy()
    df1['Outcome'] = df1.Outcome.astype("bool")
    df1['Outcome'] = df1['Outcome'].replace([1,0],['True','False'])
    df1["Age"] = np.where(df1["Age"] >= 45 ,True,False)
    df1["BloodPressure"] = np.where(df1["BloodPressure"] >= 80 ,True,False)
    # df.info()

    # percentage
    result = df1[["Outcome","BloodPressure","Age"]]
    count = 0
    for data in result:
        dataframe = result[data].value_counts()
        false_percent = dataframe[0]/sum(dataframe)*100
        false_count = dataframe[0]
        # print("false_count",false_count)
        # print("False percentage:",false_percent)
        true_percent = dataframe[1]/sum(dataframe)*100
        true_count = dataframe[1]
        # print("true count:",true_count)
        # print("True percentage:",true_percent)

        if true_percent <= 30:
            count += 1
            df.drop(data , axis=1 , inplace=True)
            print("Column not meeting true :",data,"\n",data,",True Percentage:",true_percent ,",False Percentage:",false_percent
                  ,",True Count:",true_count,",False Count:",false_count)
            # return f"boolean.py \nColumn not meeting true :{str(data)},True_Percentage-{true_percent},False_Percentage-{false_percent},True_Count-{true_count},False_Count-{false_count}\n"
    print("Number of column not meeting true:",count)
    print(" ")

# boolean()

