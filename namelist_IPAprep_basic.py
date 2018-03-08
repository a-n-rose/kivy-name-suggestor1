'''
works in directory of where .txt files from SSA's name database are saved

First section:
puts most recent .txt list to .csv with column names "name","sex","popularity"

Second section:
translates names to IPA and adds new (BASIC) features to dataframe. Saves to .csv, ready for minor preprocessing for machine learning (one still has to one-hot-encode name length)

See documentation to apply more advanced features to dataframe
'''

import pandas as pd
import glob
import os



text_files = []
for txt in glob.glob("*.txt"):
    text_files.append(txt)
    
text_files = sorted(text_files, reverse = True)
latest_list = text_files[0]
filename = os.path.splitext(latest_list)[0]
year = filename[-4::]
list_df = pd.read_csv(latest_list)
list_df.columns = ["name","sex","popularity"]
new_filename = "namelist"+year
list_df.to_csv(new_filename+".csv")



from subprocess import check_output
from functools import reduce
import operator
from collections import OrderedDict


#create new dataframe for IPA feature generation
nl_df = list_df
nl_df["ipa"] = nl_df["name"].apply(lambda x:
                                       check_output([
                                           "espeak", "-q", "--ipa", "-v", "en-us", x
                                           ]).decode("utf-8")
                                       )
 
#separate ipa letters into lists --> create their own columns
nl_df["ipaletters"] = nl_df["ipa"].apply(lambda x: list(x))
ipalist = []
nl_df["ipaletters"].apply(lambda x: ipalist.append(x))

#make letter list one-dimensional
ipalist_re = reduce(operator.add, ipalist)

#unique ipa letters (no repeats)
ipa_used = list(OrderedDict.fromkeys(ipalist_re))
ipa_used = sorted(ipa_used)
#remove '/n' and ' ' from the ipa symbol list (not relevant - every name has that at beg and end)
ipa_rel = ipa_used[2::]

#create column for each ipa letter
#True if the name has the leter, False if not
for char in ipa_rel:
    nl_df[char] = nl_df["ipaletters"].apply(lambda x: char in x)




#adding new features

#primary stress symbol is: ipa_rel[-5] (the ipa_rel must be sorted - see above)
#secondary stress symbol is: ipa_rel[-4]
#identifying names where the primary stress is at the very beginning of the name
#index here is 1 because every name starts with an empty ' ' (space)
nl_df["trochee"] = nl_df["ipaletters"].apply(lambda x:
                                                 list(x).index(ipa_rel[-5])==1
                                                 )
# and multisyllabic names (names that also have 'secondary stress'):
nl_df["multisyllabic"] = nl_df["ipaletters"].apply(lambda x:
                                                       ipa_used[-4] in x
                                                       )

#create feature of name length (based on IPA letters, not English letters)
nl_df["length"] = nl_df["ipaletters"].apply(lambda x:
                                                len(x)
                                                )
#save name data with basic IPA information, stress, and length to csv
nl_df.to_csv(new_filename+"_basic.csv")

#you can make it more complicated but just with these features, machine-learning can be applied
#the more complicated version will continue in another script. See documentation.














