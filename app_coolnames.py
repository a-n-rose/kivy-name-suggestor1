'''
15.2.2018
Very simple app: type in a name you like and get a list of either 
very similar, similar, or somewhat similar names shown to you

the input box will always be on the screen
the user can reload the screen as often as they want
and that's it! 
~ users can also click on one of the names and see similar ones as that one
'''

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton


import pandas as pd
from subprocess import check_output
import random
from random import shuffle
 
 

#make it possible to access current list of recommended names from other classes
class context:
    def __init__(self):
        self.rec_names = []
        self.current_name = ""

#present list of recommended names and allow each list item to operate as buttons
class SimilarNamesList(ListItemButton):
    pass

class CoolName(BoxLayout):
    #relating to kv file
    newname = ObjectProperty()
    rec_names_list = ObjectProperty()
    
    #load the names and their cluster groups
    def load_df(self):
        df = pd.read_csv("name_clusters.csv")
        return df

    #translate input text to ipa --> how similar names are searched
    def name2ipa(self,newname):
        newname_ipa = check_output(["espeak","-q","--ipa",'-v','en-us', newname]).decode('utf-8')
        return newname_ipa

    #search for the cluster group assigned to that name (in ipa form)
    def find_clustergroup(self,name_dataframe, newname_ipa,cluster_name = "clusters_ipa_100"):
        clustergroup = name_dataframe.get(name_dataframe["name_ipa"]==newname_ipa)[cluster_name].iloc[0]
        return clustergroup

    #obtain a dataframe of similar names to the input name
    def similar_names_df(self,name_dataframe, clustergroup, cluster_name = "clusters_ipa_100"):
        sim_namesdf = name_dataframe.get(name_dataframe[cluster_name]==clustergroup)
        sim_namesunique = sim_namesdf.drop_duplicates("name_ipa")
        return sim_namesunique

    #update the list in the kivy app         
    def show_recnames(self,rec_names):
        for name in rec_names:
            self.rec_names_list.adapter.data.extend([name])
        self.rec_names_list._trigger_reset_populate()
        

    def recommend_20random(self,sim_names_df):
        sim_names_df = sim_names_df.reset_index()
        rand20_indices = random.sample(range(0,len(sim_names_df["name"])),20)
        recnames_list = [sim_names_df["name"][i] for i in rand20_indices]
        shuffle(recnames_list)
        return recnames_list


    def mix_recommendations(self,list1, list2, list3):
        newmix = list1 + list2 + list3
        context = App.get_running_app().context
        #to ensure the name being compared to doesn't come up in the recommendation list
        current_name = context.current_name
        if current_name in newmix:
            newmix.remove(current_name)
        list(set(newmix))
        shuffle(newmix)
        ##update the context.recnames_list to the current recommended list/list of similar names pertaining to the most recent user input
        #the number here refers to the num names shown on screen
        context.rec_names = newmix[:40]
        self.show_recnames(newmix[:40])


    def submit_newname(self):
        context = App.get_running_app().context
        #check first if the input is from the listitembutton or from input field
        if self.rec_names_list.adapter.selection:
            newname = self.rec_names_list.adapter.selection[0].text
            context.current_name = newname
            self.ids.cool_name.text = newname
            #have to clear the listadapter.data of previously recommended naems
            context = App.get_running_app().context
            names_list = context.rec_names
            for name in names_list:
                self.rec_names_list.adapter.data.remove(name)
        else:
            newname = self.newname.text
            context.current_name = newname
            rec_names = context.rec_names
            if len(rec_names) > 0:
                for name in rec_names:
                    self.rec_names_list.adapter.data.remove(name)
        newname_ipa = self.name2ipa(newname)
        name_df = self.load_df()
        #I generated cluster groups with 15, 50, 100 total clusters
        #I based clustering on different features; see name_clusters.csv 
        #below I chose to include three cluster groups:
        #the clusters based on stress (trochaic, multisyllabic), ipa letters (international phonetic alphabet), and ipa features (fricative, plosive, voiced) - basically, sounds and features of the name they like --> finding other names with similar sounds and features (but not just from one cluster)
        clust1 = self.find_clustergroup(name_df, newname_ipa,"clusters_stress_50")
        clust2 = self.find_clustergroup(name_df, newname_ipa,"clusters_ipa_50")
        clust3 = self.find_clustergroup(name_df, newname_ipa,"clusters_ipafeat_stress_50")
        simnames_df1 = self.similar_names_df(name_df, clust1, "clusters_stress_50")
        simnames_df2 = self.similar_names_df(name_df, clust2, "clusters_ipa_50")
        simnames_df3 = self.similar_names_df(name_df, clust3, "clusters_ipafeat_stress_50")
        rec1 = self.recommend_20random(simnames_df1)
        rec2 = self.recommend_20random(simnames_df2)
        rec3 = self.recommend_20random(simnames_df3)
        self.mix_recommendations(rec1,rec2,rec3)
        
class CoolNamesApp(App):
    
    def build(self):
        self.context = context()
        return CoolName()
    
cnApp = CoolNamesApp()
cnApp.run()
        


