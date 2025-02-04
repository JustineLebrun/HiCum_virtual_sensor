# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 19:45:12 2025

@author: lebrunjus
"""

import numpy as np
from datetime import datetime

"""
    Files should haves the same step and duration time !!
"""

file_path_1 = "C:\\Users\\lebrunjus\\Desktop\\OpenMetrology\\Virtual_sensor\\HiCum_file_test\\noise_1000\\base_sin_1_noise_1000.txt"
file_path_2 = "C:\\Users\\lebrunjus\\Desktop\\OpenMetrology\\Virtual_sensor\\HiCum_file_test\\noise_1000\\base_sin_2_noise_1000.txt"
file_path_3 = "C:\\Users\\lebrunjus\\Desktop\\OpenMetrology\\Virtual_sensor\\HiCum_file_test\\noise_1000\\base_sin_3_noise_1000.txt"
file_path_sum = "C:\\Users\\lebrunjus\\Desktop\\OpenMetrology\\Virtual_sensor\\HiCum_file_test\\noise_1000\\test_file_noise_1000.txt"

data_set_1 = []
data_set_2 = []
data_set_3 = []
data_set_sum = []
time = []

def extract_data_from_file(file_path, data):
    try:
        with open(file_path) as file: # opens the existing file or creates it if non existant
            skip_comments = True
            first_line = True
            for line in file:  # iterate over lines directly
                
                if not line.strip() or line.startswith('#'):
                    continue
                
                parts = line.strip().rsplit('__', 1)
  
                time.append(parts[0])
                data.append(float(parts[-1]))
                
    except Exception as e:
        print("An error occured:", e)
    return data

extract_data_from_file(file_path_1, data_set_1)
extract_data_from_file(file_path_2, data_set_2)
extract_data_from_file(file_path_3, data_set_3)

if len(data_set_1) != len(data_set_2):
    print("Error: Data files have different lengths.")
else:
    # Sum the datasets
    for i in range(len(data_set_1)):
        data_set_sum.append(data_set_1[i] + data_set_2[i] + data_set_3[i])

    # print("Data Set 1:", data_set_1)
    # print("Data Set 2:", data_set_2)
    # print("Summed Data Set:", data_set_sum)

try:
    with open(file_path_sum, 'a') as file: # opens the existing file or creates it if non existant
        now = datetime.now()
        file.write("# Virtual Sensor Data Export\n")
        file.write(f"# Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("# YYYY__MM__DD__HH__MM__SS__Signal Value\n")

        for i, value in enumerate(data_set_sum):
            
            file.write(f"{time[i]}__{data_set_sum[i]:.6f}\n")
            
    print(f"Data successfully saved to {file_path_sum}")
except Exception as e:
    print(f"Error while saving file: {e}")
