import altair as alt
import networkx as nx
import nx_altair as nxa
import pandas as pd
import numpy as np
import streamlit as st 


url = 'https://github.com/caramnix/Social-Influence/blob/main/adj_matrix_116_House_Fowler.xlsx?raw=true'
df = pd.read_excel(url)

labels_dict= df.iloc[:,0].to_dict()

df= df.rename(index= df.iloc[:,0].to_dict()) 
df= df.iloc[:,1:]
df_array= np.array(df)

G= nx.from_numpy_matrix(df_array)
H = nx.relabel_nodes(G, labels_dict)

url2= 'https://github.com/caramnix/Social-Influence/raw/main/leginfo_116H.csv'
leg_info= pd.read_csv(url2) #"/Users/caranix/Library/CloudStorage/OneDrive-TheOhioStateUniversity/Social Influence/Data/Congress/116/House/leginfo_116H.csv")

leg_info= leg_info.rename(index= leg_info.iloc[:,0].to_dict()) 
leg_info= leg_info.iloc[:,1:]

leg_dict= leg_info.to_dict('index')


nx.set_node_attributes(H, leg_dict)

alt.data_transformers.disable_max_rows()

c= nxa.draw_networkx(H, node_color= 'Party', node_tooltip="Full Name").properties(width=700, height=700).configure_view(
            strokeWidth=0
        ) #) #, cmap= 'bwr',  

st.altair_chart(c)
