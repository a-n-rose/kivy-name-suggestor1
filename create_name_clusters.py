import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.cluster import KMeans



def load_df(input_file):
    df = pd.read_csv(input_file)
    return df

def Kmeans_cluster(num_clusters=15):
    num_clusters = num_clusters
    km = KMeans(n_clusters = num_clusters, init='k-means++', n_init=1, verbose=1)
    return km







#I want clusters based on:
#1) stress and multisyllable
#2) mouth location
#3) ipa features
#4) ipa letters themselves - any difference from ipa features?




input_file = "names_df.csv"
df = load_df(input_file)
#make copy
names_df = df

#create new database for saving clusters - will use in another script
#don't want all features. Just features relevant to user (male,female;popularity;recency)
nameinfo_columns = ["name","sex","number","year","name_ipa"] #in this dataset, year refers to year last used (in the USA)
names_clusters = names_df[nameinfo_columns]





#clusters based on ipa:
vectorizer = CountVectorizer(analyzer='char',decode_error='ignore',min_df=1, max_df=.9)
names_ipa = []
names_df['name_ipa'].apply(lambda x: names_ipa.append(x))
#creates vectors for each sound
namesounds_vectors = vectorizer.fit_transform(names_ipa)
#now apply tfidf
transformer = TfidfTransformer(smooth_idf = True)
#If smooth_idf=True (the default), the constant “1” is added to the numerator and denominator of the idf as if an extra document was seen containing every term in the collection exactly once, which prevents zero divisions: idf(d, t) = log [ (1 + n) / 1 + df(d, t) ] + 1.
tfidf_names = transformer.fit_transform(namesounds_vectors)
tfidf_names.toarray()
#Each row is normalized to have unit Euclidean norm
#Now... with the TfidfVectorizer:
#which basically does the counting and transforming together:
vectorizer = TfidfVectorizer(analyzer='char',decode_error='ignore',min_df=1, max_df=.9)
names_4_kmeans = vectorizer.fit_transform(names_ipa)
print(names_4_kmeans)

km15 = Kmeans_cluster()
km15_names = km15.fit(names_4_kmeans)

km50 = Kmeans_cluster(num_clusters=50)
km50_names = km50.fit(names_4_kmeans)

km100 = Kmeans_cluster(num_clusters=100)
km100_names = km100.fit(names_4_kmeans)

names_clusters['clusters_ipa_15'] = km15.labels_
names_clusters['clusters_ipa_50'] = km50.labels_
names_clusters['clusters_ipa_100'] = km100.labels_






#clusters based on stress:
stress_clmns = ["trochee","multisyllabic"]
df_stress = names_df[stress_clmns]
km_stress = KMeans(n_clusters = 15, random_state = 0).fit(df_stress)
labels_stress = km_stress.labels_
names_clusters['clusters_stress_15'] = labels_stress

km_stress = KMeans(n_clusters = 50, random_state = 0).fit(df_stress)
labels_stress = km_stress.labels_
names_clusters['clusters_stress_50'] = labels_stress

km_stress = KMeans(n_clusters = 100, random_state = 0).fit(df_stress)
labels_stress = km_stress.labels_
names_clusters['clusters_stress_100'] = labels_stress


#clusters based on location in mouth:
mouth_loc_clmns = ["close","close-mid","open-mid","open","front","central","back"]
df_mouthloc = names_df[mouth_loc_clmns]
km_mouthloc = KMeans(n_clusters = 15, random_state = 0).fit(df_mouthloc)
labels_mouthloc = km_mouthloc.labels_
names_clusters['clusters_mouthloc_15'] = labels_mouthloc

km_mouthloc = KMeans(n_clusters = 50, random_state = 0).fit(df_mouthloc)
labels_mouthloc = km_mouthloc.labels_
names_clusters['clusters_mouthloc_50'] = labels_mouthloc

km_mouthloc = KMeans(n_clusters = 100, random_state = 0).fit(df_mouthloc)
labels_mouthloc = km_mouthloc.labels_
names_clusters['clusters_mouthloc_100'] = labels_mouthloc





#clusters based on ipa features:
ipa_feat_clmns = ["long_vowel","bilabial","labiodental","dental","alveolar","postalveolar","palatal","velar","glottal","plosive","nasal","trill","flap","fricative","approximate","lateral_approximate", "long_vowel","bilabial","labiodental","dental","alveolar","postalveolar","palatal","velar","glottal","plosive","nasal","trill","flap","fricative","approximate","lateral_approximate"]
df_ipafeat = names_df[ipa_feat_clmns]
km_ipafeat = KMeans(n_clusters = 15, random_state = 0).fit(df_ipafeat)
labels_ipafeat = km_ipafeat.labels_
names_clusters['clusters_ipafeat_15'] = labels_ipafeat

km_ipafeat = KMeans(n_clusters = 50, random_state = 0).fit(df_ipafeat)
labels_ipafeat = km_ipafeat.labels_
names_clusters['clusters_ipafeat_50'] = labels_ipafeat

km_ipafeat = KMeans(n_clusters = 100, random_state = 0).fit(df_ipafeat)
labels_ipafeat = km_ipafeat.labels_
names_clusters['clusters_ipafeat_100'] = labels_ipafeat




#clusters based on combined features

#ipa features and stress:
#clusters based on ipa features:
ipafeat_stress_clmns = ipa_feat_clmns + stress_clmns 
df_ipafeat_stress = names_df[ipafeat_stress_clmns]
km_ipafeat_stress = KMeans(n_clusters = 15, random_state = 0).fit(df_ipafeat_stress)
labels_ipafeat_stress = km_ipafeat_stress.labels_
names_clusters['clusters_ipafeat_stress_15'] = labels_ipafeat_stress

km_ipafeat_stress = KMeans(n_clusters = 50, random_state = 0).fit(df_ipafeat_stress)
labels_ipafeat_stress = km_ipafeat_stress.labels_
names_clusters['clusters_ipafeat_stress_50'] = labels_ipafeat_stress

km_ipafeat_stress = KMeans(n_clusters = 100, random_state = 0).fit(df_ipafeat_stress)
labels_ipafeat_stress = km_ipafeat_stress.labels_
names_clusters['clusters_ipafeat_stress_100'] = labels_ipafeat_stress


#clusters based on ipa features and mouth location
ipafeat_mouthloc_clmns = ipa_feat_clmns + mouth_loc_clmns 
df_ipafeat_mouthloc = names_df[ipafeat_mouthloc_clmns]
km_ipafeat_mouthloc = KMeans(n_clusters = 15, random_state = 0).fit(df_ipafeat_mouthloc)
labels_ipafeat_mouthloc = km_ipafeat_mouthloc.labels_
names_clusters['clusters_ipafeat_mouthloc_15'] = labels_ipafeat_mouthloc

km_ipafeat_mouthloc = KMeans(n_clusters = 50, random_state = 0).fit(df_ipafeat_mouthloc)
labels_ipafeat_mouthloc = km_ipafeat_mouthloc.labels_
names_clusters['clusters_ipafeat_mouthloc_50'] = labels_ipafeat_mouthloc

km_ipafeat_mouthloc = KMeans(n_clusters = 100, random_state = 0).fit(df_ipafeat_mouthloc)
labels_ipafeat_mouthloc = km_ipafeat_mouthloc.labels_
names_clusters['clusters_ipafeat_mouthloc_100'] = labels_ipafeat_mouthloc



#save database to csv file 
names_clusters.to_csv("names_clusters_advanced.csv")
