def data_generator(location, line_nums):
    """
      This function reads lines specified by the user
      - param location: location of the input file
      - param line_nums: desired line numbers

      - return: list of the desired lines
    """

    def get_lines(file, line_nums):
        """
          This function reads the desired lines from the input file
          - param file: input file object

          return: returns a list of desired lines without any modifications on them
        """
        return [x for i, x in enumerate(file) if i in line_nums]

    with open(location, 'r') as file:
        lines = get_lines(file, line_nums)
        desired_lines = []
        for line in lines:
            desired_lines.append(line.split())  # to remove separater (\t) from each line

    return desired_lines


def value_extractor(input_list):
    """
    The sampling time is repeated for each value for all the sensors - This function
    only extracts the values and return a list of values from all the sensors at each sampling time
    - param input_list: a list of data containing sampling time and values from each sensor at one sampling time

    - return: a list including only the values (NOT the sampling time)
    * Used in data_maker()
    """

    list_values = []
    for i in range(1, len(input_list) + 1, 2):
        list_values.append(input_list[i])

    return list_values


def data_maker(list_inputs):
    """
    Makes a dictionary of the data;
      key=sampling time -- value=data from the sensors at a specific time
    - param list_inputs: a nested list containing the elments of each line

    - return: a dictionary containing the data, columns as time samples
    """
    dict_data = {}
    for i in range(len(list_inputs)):
        label = list_inputs[i][0]
        values = value_extractor(list_inputs[i])
        dict_data[label] = values

    return dict_data


def column_namer(df, df_info):
    """
    assign proper name for each column of data from the dataframe containing information
    - param df: dataframe of sensers' data with sampling time as columns's name
    - param df_info: dataframe including the naming about the dataset in the 'Name' column

    - return: a dataframe with columns indicating the sensor's name and indexes as time sample
    """

    df = df.T  # transpose the dataframe
    df.columns = df_info['Name']  # setting the names for the columns

    return df


def column_renamer(df):
    """
    the naming convention includes the datatypes' first letter at the beginning of the name,
    this function rename the columns to an appropriate name
    - param: the dataframe with time samples as indexes and sensor's names as columns

    - return: a dataframe with proper naming for the columns
    """

    df.rename(columns=lambda x: x[1:], inplace=True)

    return df


def apply_data_type(df, df_info):
    """
      It assing a proper datatype for each column based on the information provided in the source file
      'BIT' --> Boolean
      'REAL32' --> float32
      'REAL64' --> float64
      'INT16' --> int16

      - param df: dataframe containing the sensor's data with proper naming for columns and rows
      - param df_info: dataframe containing the datatypes for each sensor in the 'Data-Type' column.

      - return: a dataframe with properly assigned data types and naming.
    """

    for col_name, data_type in zip(df.columns, df_info['Data-Type']):

        if data_type == 'BIT':
            df[col_name] = df[col_name].astype('int').astype('bool')

        if data_type == 'REAL32':
            df[col_name] = df[col_name].astype('float32')

        elif data_type == 'REAL64':
            df[col_name] = df[col_name].astype('float64')

        elif data_type == 'INT16':
            df[col_name] = df[col_name].astype('int16')

    return df


def mean_calculator(df):
    """
    This function skips the columns with boolean values and calculate the mean of the rest

    - param df: dataframe with properly assigned datatypes and naming

    - return: a dictionary of the averages -- {KEY='sensor's name': VALUE='average for each sensor over time'}
    """

    dict_averages = {}
    for col in df.columns:
        if df[col].dtype == 'bool':
            continue
        else:
            mean = df[col].mean()
            dict_averages[col] = mean

    return dict_averages


def data_reformater(dict_results):
    """
    JSON files only do not support float32, before making the JSON files, data with the format of
    float32 are converted to float64

    - param dict_results: a dictionary cotaining the average values
      {KEY='sensor's name': VALUE='average for each sensor over time'}

    - return: the modifed results with all numeric values as float64
    """
    for key, value in dict_results.items():
        if type(value) == np.float32:
            dict_results[key] = np.float64(value)

    return dict_results


import numpy as np
import pandas as pd
import json


def dict_combinber(dict_assignment_info, dict_data_specs):
    """
    Combines 2 dictionaries - the mean values for the sensors are stored as list of dictionaries with KEY='data specification'
    - param dict_assignment_info: dictionary containing the assignment's info
    - param dict_data_specs: dictionray cotaining the mean values

    - return: a dictionray containing information from both of the dictionaries.
    """

    dict_assignment_info['Data Specification'] = [dict_data_specs]

    return dict_assignment_info


def json_writer(python_dict):
    """
    Get's a python dict and writes a JSON file

    - param: a python dictionary
    """

    with open("Erfan's results.json", 'w') as file:
        json.dump(python_dict, file, indent=2)  # setting proper indentation to get a readable output!
