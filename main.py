from functions import *

import os

# creating the dictionary containing the info of the project
result_JSON_file = {'file name': 'report for the coding assignment',
                    'Start date': 'Jan. 22, 2023',
                    'Start time': '10 AM',
                    'End date': 'Jan, 22, 2023',
                    'End time': '2 PM'}


# getting the location of the source file
cur_path = os.getcwd()
file_path = os.path.join(cur_path, 'input/data.txt')

# to generate the dataset containing the information for naming columns and assigning data types
df_info = data_maker(data_generator(file_path, line_nums=[6, 21]))
df_info = pd.DataFrame(df_info)

# to generate the dataset containing the data with time samples as the columns' name
df = data_maker(data_generator(file_path, line_nums=list(range(27, 57))))
df = pd.DataFrame(df)

# naming the columns of the dataset based on row 7
df = column_namer(df, df_info)

# removing the datatype first letter from the naming column
df = column_renamer(df)

# applying the datatypes based on row 22
df = apply_data_type(df, df_info)

# creating a dictionary including the mean of the column (skipping the boolean columns)
mean_dict = mean_calculator(df)

# re-formatting the float32 to float64 before generating the JSON file (float32 is not supported by JSON)
mean_dict = data_reformater(mean_dict)

# combining the dict of the mean values with the dict of result_JSON_file
result_JSON_file = dict_combiner(result_JSON_file, mean_dict)

# writing the JSON file -- output file name: results-Erfan.json
json_writer(result_JSON_file)

# converting the dataframe as CSV file -- output file name: dataframe.csv
csv_writer(df)

print('Code executed successfully!')







