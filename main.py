from functions import *
import os

result_JSON_file = {'file name': 'report for the coding assignment',
                    'Start date': 'Jan. 22, 2023',
                    'Start time': '10 AM',
                    'End date': 'Jan, 22, 2023',
                    'End time': '2 PM'}


# getting the location of the source file
cur_path = os.getcwd()
print(cur_path)
# exit()
file_path = os.path.join(cur_path,'input/data.txt')

# to generate the dataset containing the information for naming columns and assigning data types
df_info = data_maker(data_generator(file_path, [6, 21]))
df_info = pd.DataFrame(df_info)
# df_info.head()

# to generate the dataset containing the data with time samples as the columns' name
df = data_maker(data_generator(file_path, list(range(27, 57))))
df = pd.DataFrame(df)
# df.head()

df = column_namer(df, df_info)
df = column_renamer(df)
df = apply_data_type(df, df_info)
mean_dict = mean_calculator(df)
mean_dict = data_reformater(mean_dict)
result_JSON_file = dict_combiner(result_JSON_file, mean_dict)
json_writer(result_JSON_file)

print('Code executed successfully!')







