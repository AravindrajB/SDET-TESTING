import argparse
import configparser
import pandas as pd
import modules.boolean as bool
import modules.categorical as cat
import modules.missing as miss
import modules.numerical as num


def config_setting(model_name):

    requirement_list = []
    parser = argparse.ArgumentParser(description='Test data validation model config')

    parser.add_argument('--config_model_names' , type=str , default=f'config/{model_name}_config.ini' , help = 'Config model for the model')
    arguments = parser.parse_args()

    # configparser object
    cfg = configparser.ConfigParser()

    # read config file
    cfg.read(arguments.config_model_names)
    config_data = cfg.items()
    for i in config_data:
        for actual1 in i:
            if actual1 == 'THRESHOLDS' or actual1 == 'TESTRUN':
                requirement_list.append(actual1)
    # THRESHOLDS
    threshold_ = []
    defaultthreshold_ = []
    excepted1 = 'THRESHOLDS'
    if excepted1 in requirement_list :
        cfg_dict = dict(cfg.items('THRESHOLDS'))
        a = cfg_dict.get('missing_value')
        missing_values = int(a.rstrip('%'))
        categorical_count = int(cfg_dict.get('categorical_count'))
        b = cfg_dict.get('boolean_value')
        boolean_value = int(b.rstrip('%'))
        c = cfg_dict.get('outlier_threshold')
        outliers_threshold = int(c.rstrip('%'))
        result1 = {'missing_values':missing_values,'categorical_count':categorical_count,'boolean_value':boolean_value,'outliers_threshold':outliers_threshold}
        threshold_.append(result1)

    else:

        default_missing_values, default_categorical_count, default_boolean_value, default_outliers_threshold = default_threshold()
        result2 = {'default_missing_values':default_missing_values,'default_categorical_count':default_categorical_count,'default_boolean_value':default_boolean_value,'default_outliers_threshold':default_outliers_threshold}
        defaultthreshold_.append(result2)

    return threshold_ , defaultthreshold_


# STEP 2
def default_threshold():

    cfg2 = configparser.ConfigParser()
    cfg2.read('config/base_config.ini')

    # Default threshold
    default = dict(cfg2.items('DEFAULT_THRESHOLDS'))
    a = default.get('missing_value')
    missing_values = int(a.rstrip('%'))
    categorical_count = int(default.get('categorical_count'))
    b = default.get('boolean_value')
    boolean_value = int(b.rstrip('%'))
    c = default.get('outlier_threshold')
    outliers_threshold = int(c.rstrip('%'))

    return missing_values, categorical_count, boolean_value, outliers_threshold

# STEP 3
def csv_name(model_name):

    cfg3_ = configparser.ConfigParser()
    cfg3_.read(f'config/{model_name}_config.ini')
    csv = []
    config_data = cfg3_.items()

    requirement_list2 = []
    for i in config_data:
        for actual1 in i:
            if actual1 == 'THRESHOLDS' or actual1 == 'TESTRUN':
                requirement_list2.append(actual1)

    excepted = 'TESTRUN'
    if excepted in requirement_list2 :
        testrun = dict(cfg3_.items('TESTRUN'))
        for k, val in testrun.items():
            if val == 'Yes' or val == 'YES' or val == 'yes':
                excepted_ = 'input_' + k  # input_train_dataset
                testdata_name = dict(cfg3_.items('TESTDATA_NAME'))
                for k1, val1 in testdata_name.items():
                    actual = k1
                    if actual == excepted_:
                        file_name = testdata_name.get(actual)
                        csv.append(file_name)

    else:
        testdata_name = dict(cfg3_.items('TESTDATA_NAME'))
        for file in testdata_name.values():
            csv.append(file)

    return csv


# STEP 4
def base_config_setting(model_name):

    cfg4 = configparser.ConfigParser()
    cfg4.read('config/base_config.ini')
    missing_val_list = []
    dataframe = []

    # Missing values info
    missing = dict(cfg4.items('MISSING_VALUES'))
    for missing_val_input in missing.values():
        missing_val_list.append(missing_val_input)

    # Folder name
    test_datas = dict(cfg4.items('TESTDATA_DIR'))
    for folder in test_datas.values():
        # Csv name
        csv = csv_name(f'{model_name}')
        for file_name in csv:
            file_path = folder + "/" + file_name
            pandas = pd.read_csv(file_path)
            dataframe.append(pandas)

    # Missing values info split
    # missing = dict(cfg4.items('MISSING_VALUES'))
    # for missing_val_input in missing.values():
    #     missing_val_list = missing_val_input.split(',')

    return dataframe,missing_val_list

# STEP 5
def result():

    cfg5 = configparser.ConfigParser()
    cfg5.read('config/base_config.ini')
    output_ = []
    base_config = dict(cfg5.items('MODELS'))
    for k, v in base_config.items():
        if v == 'YES' or v == 'Yes' or v == 'yes':
            dataframe, missing_val_list = base_config_setting(k)
            output_.append(f'{50*"-"}MODEL_NAME:{k}{50*"-"}')
            for df in dataframe:
                threshold, defaultthreshold = config_setting(k)
                # DefaultThreshold
                if defaultthreshold :
                    print('default')
                    for data in defaultthreshold:
                        for key, value in data.items():
                            if key == 'default_missing_values':
                                default_missing_values = data.get(key)
                                output_.append(miss.summary_details(df, default_missing_values, missing_val_list))
                            elif key == 'default_categorical_count':
                                default_categorical_count = data.get(key)
                                output_.append(cat.categorical(df, default_categorical_count))
                            elif key == 'default_boolean_value':
                                default_boolean_value = data.get(key)
                                output_.append(bool.boolean_func(df, default_boolean_value))
                            elif key == 'default_outliers_threshold':
                                default_outliers_threshold = data.get(key)
                                output_.append(num.outliers_function(df, default_outliers_threshold))
                else:
                    pass
                # Threshold
                if threshold:
                    for x in threshold:
                        for key1, value1 in x.items():
                            if key1 == 'missing_values':
                                missing_threshold = x.get(key1)
                                output_.append(miss.summary_details(df, missing_threshold, missing_val_list))
                            elif key1 == 'categorical_count':
                                categorical_threshold = x.get(key1)
                                output_.append(cat.categorical(df, categorical_threshold))
                            elif key1 == 'boolean_value':
                                bool_threshold = x.get(key1)
                                output_.append(bool.boolean_func(df, bool_threshold))
                            elif key1 == 'outliers_threshold':
                                outlier_threshold = x.get(key1)
                                output_.append(num.outliers_function(df, outlier_threshold))
                else:
                    pass
        else:
            output_.append(f'\nCHECK_YOUR_MODEL"{k}"')

    return output_

# STEP 6
def file_write(path):

    # Create
    # file_create = open(f'{path}/project_output','x')
    # if file_create:
    #     print('file create')
    # else:
    #     print('file does not create')

    # Write
    File_write = open(f'{path}/project_output','w')
    for out in result():
        File_write.write(out)
        File_write.write('\n')
    File_write.close()
    # Read
    read = open(f'{path}/project_output','r')
    for r in read:
        print(r)


if __name__ == "__main__":

    cfg3 = configparser.ConfigParser()
    cfg3.read('config/base_config.ini')
    # output path
    output = dict(cfg3.items('OUTPUT_PATH'))
    output_path = output.get('output')
    file_write(output_path)
    result()














'''
requirement_list = []
# step 1
def config_setting(model_name):

    parser = argparse.ArgumentParser(description='Test data validation model config')

    parser.add_argument('--config_model_names' , type=str , default=f'config/{model_name}_config.ini' , help = 'Config model for the model')
    arguments = parser.parse_args()

    # configparser object
    cfg = configparser.ConfigParser()

    # read config file
    cfg.read(arguments.config_model_names)
    cfg.read('config/base_config.ini')

    # getting items
    config_data = cfg.items()
    print('------------config',dict(config_data))
    for i in config_data:
        print('iiiiiiiiiiiiiiiiiiiiii',i)
        for actual1 in i:
            print('actualllllllllllll',actual1)
            if actual1 == 'THRESHOLDS' or actual1 == 'TESTRUN':
                requirement_list.append(actual1)

    # THRESHOLDS
    # threshold = []
    excepted1 = 'THRESHOLDS'
    if excepted1 in requirement_list :
        cfg_dict = dict(cfg.items('THRESHOLDS'))
        a = cfg_dict.get('missing_value')
        missing_values = int(a.rstrip('%'))
        categorical_count = int(cfg_dict.get('categorical_count'))
        b = cfg_dict.get('boolean_value')
        boolean_value = int(b.rstrip('%'))
        c = cfg_dict.get('outlier_threshold')
        outliers_threshold = int(c.rstrip('%'))

        # outcome= {'missing_values':missing_values,'categorical_count':categorical_count,'boolean_value':boolean_value,'outlier_threshold':outliers_threshold}
        # outcome = (missing_values,categorical_count,boolean_value,outliers_threshold)
        # threshold.append(outcome)

        # return missing_values ,categorical_count,boolean_value,outliers_threshold

    else:
        threshold()
        # return default_missing_values ,default_categorical_count,default_boolean_value,default_outliers_threshold
    return missing_values ,categorical_count,boolean_value,outliers_threshold

def threshold():
    default_missing_values, default_categorical_count, default_boolean_value, default_outliers_threshold = default_threshold()
    print('DEFAULT THRESHOLD')
    return default_missing_values, default_categorical_count, default_boolean_value, default_outliers_threshold

# STEP 2
def default_threshold():
    cfg2 = configparser.ConfigParser()
    cfg2.read('config/base_config.ini')

    # Default threshold
    default = dict(cfg2.items('DEFAULT_THRESHOLDS'))
    a = default.get('missing_value')
    missing_values = int(a.rstrip('%'))
    categorical_count = int(default.get('categorical_count'))
    b = default.get('boolean_value')
    boolean_value = int(b.rstrip('%'))
    c = default.get('outlier_threshold')
    outliers_threshold = int(c.rstrip('%'))

    return missing_values, categorical_count, boolean_value, outliers_threshold

# STEP 3
def csv_name(model_name):

    cfg3 = configparser.ConfigParser()
    cfg3.read(f'config/{model_name}_config.ini')
    csv = []
    excepted = 'TESTRUN'
    if excepted in requirement_list :
        testrun = dict(cfg3.items('TESTRUN'))
        for key, value in testrun.items():
            if value == 'Yes' or value == 'YES' or value == 'yes':
                excepted_ = 'input_' + key  # input_train_dataset
                testdata_name = dict(cfg.items('TESTDATA_NAME'))
                for key1, value1 in testdata_name.items():
                    actual = key1
                    if actual == excepted_:
                        file_name = testdata_name.get(actual)
                        print('file_name',file_name)
                        csv.append(file_name)

    else:
        testdata_name = dict(cfg3.items('TESTDATA_NAME'))
        for file in testdata_name.values():
            csv.append(file)

    return csv

# STEP 4
def base_config_setting(model_name):

    cfg4 = configparser.ConfigParser()
    cfg4.read('config/base_config.ini')
    missing_val_list = []
    dataframe = []

    # Missing values info
    missing = dict(cfg4.items('MISSING_VALUES'))
    for missing_val_input in missing.values():
        missing_val_list.append(missing_val_input)

    # Folder name
    test_datas = dict(cfg4.items('TESTDATA_DIR'))
    value = test_datas.values()
    for folder in test_datas.values():
        # Csv name
        csv = csv_name(model_name)
        for file_name in csv:
            file_path = folder + "/" + file_name
            pandas = pd.read_csv(file_path)
            dataframe.append(pandas)

    return dataframe,missing_val_list

# STEP 5
def result():

    cfg5 = configparser.ConfigParser()
    cfg5.read('config/base_config.ini')
    output = []
    base_config = dict(cfg5.items('MODELS'))
    for key, value in base_config.items():
        dataframe, missing_val_list = base_config_setting(key)
        if value == 'YES' or value == 'Yes' or value == 'yes':
            # bool_threshold, categorical_threshold, outlier_threshold, missing_threshold = config_setting(key)
            # dataframe, missing_val_list = base_config_setting(key)
            excepted1 = 'THRESHOLDS'
            if excepted1 in requirement_list:
                bool_threshold, categorical_threshold, outlier_threshold, missing_threshold = config_setting(key)
                for df in dataframe:
                    output.append(f'<-------------Model Name:{key}------------------>')
                    output.append(bool.boolean_func(df, bool_threshold))
                    output.append(num.outliers_function(df, outlier_threshold))
                    output.append(cat.categorical(df, categorical_threshold))
                    output.append(miss.summary_details(df, missing_threshold, missing_val_list))
            else:
                default_missing_values, default_categorical_count, default_boolean_value, default_outliers_threshold = threshold()
                for df in dataframe:
                    output.append(f'<-------------Model Name:{key}------------------>')
                    output.append(bool.boolean_func(df, default_boolean_value))
                    output.append(num.outliers_function(df, default_outliers_threshold))
                    output.append(cat.categorical(df, default_categorical_count))
                    output.append(miss.summary_details(df, default_missing_values, missing_val_list))
        else:
            output.append(f'Check Your model"{key}"')
    return output

# STEP 6
def file_write(path):

    # Create
    # file_create = open(f'{path}/project_output','x')
    # if file_create:
    #     print('file create')
    # else:
    #     print('file does not create')

    # Write
    File_write = open(f'{path}/project_output','w')
    for out in result():
        File_write.write(out)
        File_write.write('\n')
    File_write.close()
    # Read
    read = open(f'{path}/project_output','r')
    for output_ in read:
        print(output_)

if __name__ == "__main__":

    cfg3 = configparser.ConfigParser()
    cfg3.read('config/base_config.ini')
    # output path
    output = dict(cfg3.items('OUTPUT_PATH'))
    output_path = output.get('output')
    file_write(output_path)
    result()
#
'''

'''

# Step 1 --> read config , getting threshold values
def config_setting(model_name):

    parser = argparse.ArgumentParser(description='Test data validation model config')

    parser.add_argument('--config_model_names' , type=str , default=f'config/{model_name}_config.ini' , help = 'Config model for the model')
    arguments = parser.parse_args()

    # configparser object
    cfg = configparser.ConfigParser()

    # read config file
    cfg.read(arguments.config_model_names)

    # cfg_dict = dict(cfg.items('THRESHOLDS'))
    # print(cfg_dict)
    # a = cfg_dict.get('missing_value')
    # missing_values = int(a.rstrip('%'))
    # categorical_count = int(cfg_dict.get('categorical_count'))
    # b = cfg_dict.get('boolean_value')
    # boolean_value = int(b.rstrip('%'))
    # c = cfg_dict.get('outlier_threshold')
    # outliers_threshold = int(c.rstrip('%'))



    cfg_dict = dict(cfg.items('THRESHOLDS'))
    a = cfg_dict.get('missing_value')
    if a == None:
        boolean_value_, categorical_count_, outliers_threshold_, missing_values_ = default_threshold()
        print('default threshold')
        return boolean_value_, categorical_count_, outliers_threshold_, missing_values_
    else:
        # cfg_dict = dict(cfg.items('THRESHOLDS'))
        # print(cfg_dict)
        # a = cfg_dict.get('missing_value')
        missing_values = int(a.rstrip('%'))
        categorical_count = int(cfg_dict.get('categorical_count'))
        b = cfg_dict.get('boolean_value')
        boolean_value = int(b.rstrip('%'))
        c = cfg_dict.get('outlier_threshold')
        outliers_threshold = int(c.rstrip('%'))

        return boolean_value,categorical_count,outliers_threshold,missing_values

# Step 2 --> getting folder name , passing dynamic missing values
def base_config_setting():

    cfg2 = configparser.ConfigParser()
    cfg2.read('config/base_config.ini')
    missing_val_list = []
    dataframe = []

    # Missing values info
    missing = dict(cfg2.items('MISSING_VALUES'))
    for missing_val_input in missing.values():
        missing_val_list.append(missing_val_input)

    # Folder name
    test_datas = dict(cfg2.items('TESTDATA_DIR'))
    value = test_datas.values()
    for folder in test_datas.values():
        # Csv name
        csv = csv_name()
        for file_name in csv:
            file_path = folder + "/" + file_name
            pandas = pd.read_csv(file_path)
            dataframe.append(pandas)

    return dataframe,missing_val_list

# step 3 --> getting default thresholds
def default_threshold():

    cfg2 = configparser.ConfigParser()
    cfg2.read('config/base_config.ini')

    # Default threshold
    default = dict(cfg2.items('DEFAULT_THRESHOLDS'))
    a = default.get('missing_value')
    missing_values = int(a.rstrip('%'))
    categorical_count = int(default.get('categorical_count'))
    b = default.get('boolean_value')
    boolean_value = int(b.rstrip('%'))
    c = default.get('outlier_threshold')
    outliers_threshold = int(c.rstrip('%'))

    return missing_values,categorical_count,boolean_value,outliers_threshold

# getting csv name
def csv_name(model):
    cfg3 = configparser.ConfigParser()
    cfg3.read(f'config/{model}_config.ini')
    csv = []
    testrun = dict(cfg3.items('TESTRUN'))
    for key,value in testrun.items():
        if value == 'Yes' or value == 'YES' or value == 'yes':
            excepted = 'input_' + key                   # input_train_dataset
            testdata_name = dict(cfg3.items('TESTDATA_NAME'))
            for key1,value1 in testdata_name.items():
                actual = key1
                if actual == excepted:
                    file_name = testdata_name.get(actual)
                    csv.append(file_name)

    return csv

# Step 4 --> output , pass df to python files
def result():

    cfg2 = configparser.ConfigParser()
    cfg2.read('config/base_config.ini')
    output = []
    base_config = dict(cfg2.items('MODELS'))
    for key, value in base_config.items():
        if value == 'YES' or value == 'Yes' or value == 'yes':
            bool_threshold, categorical_threshold, outlier_threshold, missing_threshold = config_setting(key)
            dataframe, missing_val_list = base_config_setting()
            for df in dataframe:
                output.append(f'<-------------Model Name:{key}------------------>')
                output.append(bool.boolean_func(df, bool_threshold))
                output.append(num.outliers_function(df, outlier_threshold))
                output.append(cat.categorical(df, categorical_threshold))
                output.append(miss.summary_details(df, missing_threshold, missing_val_list))
        else:
            output.append(f'Check Your model"{key}"')
    return output

# Step 5 --> File handling
def file_write(path):
    # Create
    # file_create = open(f'{path}/project_output','x')
    # if file_create:
    #     print('file create')
    # else:
    #     print('file does not create')

    # Write
    File_write = open(f'{path}/project_output','w')
    for out in result():
        File_write.write(out)
        File_write.write('\n')
    File_write.close()
    # Read
    read = open(f'{path}/project_output','r')
    for output_ in read:
        print(output_)

if __name__ == "__main__":

    cfg3 = configparser.ConfigParser()
    cfg3.read('config/base_config.ini')
    # output path
    output = dict(cfg3.items('OUTPUT_PATH'))
    output_path = output.get('output')
    file_write(output_path)
    result()


'''


