import pandas as pd
import numpy as np

def outliers():

    print("numerical.py")
    df = pd.read_csv("D:\csv_files\diabetes.csv")
    pd.reset_option("max_columns")
    # print(df.head())
    # print("Rows and columns:", df.shape)
    # df.info()

    # Outliers
    # df.drop(["Outcome", "BloodPressure", "Age"], axis=1, inplace=True)
    df1 = df.copy()
    for dataframe in df1:
        df1[dataframe] = sorted(df1[dataframe])
        result = []
        q1, q3 = np.percentile(df1[dataframe], [25, 75])
        IQR = q3 - q1
        lower_bound = q1 - (1.5 * IQR)
        # print("lower:",lower_bound)
        upper_bound = q3 + (1.5 * IQR)
        # print("upper:",upper_bound)
        for record in df1[dataframe]:
            if (record < lower_bound) | (record > upper_bound):
                result.append(record)
        length = len(result)
        outliers_percent = length / len(df1[dataframe]) * 100
        # print(dataframe, outliers_percent)
        feature= []
        threshold = 3
        if outliers_percent > threshold:
            df.drop(dataframe, axis=1, inplace=True)
            print("Column name:",dataframe,",Count of outliers:",length)
            # return f"numerical.py\nColumn name:{dataframe},Count of outliers-{length}"

    # print(df.head())

# outliers()
