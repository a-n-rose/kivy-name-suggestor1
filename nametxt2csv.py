'''
works in directory of where .txt files from SSA's name database are saved
puts most recent list to .csv with column names
'''

import numpy as np
import pandas as pd
import glob
import os

text_files = []
for txt in glob.glob('*.txt'):
    text_files.append(txt)
    
text_files = sorted(text_files, reverse = True)
latest_list = text_files[0]
filename = os.path.splitext(latest_list)[0]
filename = filename[10::]
list_df = pd.read_csv(latest_list)
list_df.columns = ["name","sex","popularity"]
list_df.to_csv(filename+".csv")

