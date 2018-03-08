# Kivy-Name-Recommender(simple)
Very simple version of a name recommender using the Kivy and Python languages. 
The frontend is not finished (at all). But it works. Has not been tested for funny text inputs. 

I will provide the links and .py scripts I used/wrote to collect and prepare names for the recommender as well as the scripts for the recommender and app.

### Necessary Installations
Espeak (for Python3+)
Numpy, Pandas

### Name list
All names used in the United States from 1880 until 2016 (at the time I wrote this) is available for download here:  https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data

Extract the file in the same directory as the script "nametxt2csv.py". 
* IMPORTANT!!! No other .txt files can be in the directory!!!!

Run the script and you will get the latest namelist saved in a .csv with column names (in the same directory).

### IPA features
For reference, here is a link to the International Phonetic Alphabet. https://www.internationalphoneticassociation.org/content/full-ipa-chart

In the same directory as the .csv namelist, to only apply basic IPA features, run the "namelist_IPAprep_basic.py" script. This will provide another .csv with several new features as columns. This would already be useful in various machine learning contexts. 
The more advanced-features script will be provided soon.


