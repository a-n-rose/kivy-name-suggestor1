'''
works in directory of where .txt files from SSA's name database are saved
puts most recent list to namelist[year].csv with column names "name", "sex", "popularity"
'''

import pandas as pd
import glob
import os

text_files = []
for txt in glob.glob('*.txt'):
    text_files.append(txt)
    
text_files = sorted(text_files, reverse = True)
latest_list = text_files[0]
filename = os.path.splitext(latest_list)[0]
year = filename[-4::]
list_df = pd.read_csv(latest_list)
list_df.columns = ["name","sex","popularity"]
list_df.to_csv("namelist"+year+".csv")
