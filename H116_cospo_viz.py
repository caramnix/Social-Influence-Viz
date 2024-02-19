import altair as alt
import networkx as nx
import nx_altair as nxa
import pandas as pd
import numpy as np
import streamlit as st 


st.markdown("<div style='background:#e6e6e6'><h3 style='font-weight:bold; color:#252626'>  Cosponsorship Network, 116th Congress (2019-2021)</h3></div>", unsafe_allow_html=True)


url = 'https://github.com/caramnix/Social-Influence-Viz/blob/main/adj_matrix_116_House_Fowler.xlsx?raw=true'
df = pd.read_excel(url)

labels_dict= df.iloc[:,0].to_dict()

df= df.rename(index= df.iloc[:,0].to_dict()) 
df= df.iloc[:,1:]
df_array= np.array(df)

G=  nx.from_numpy_array(df_array) #nx.from_numpy_matrix(df_array)
H = nx.relabel_nodes(G, labels_dict)

H.remove_edges_from([(n1, n2) for n1, n2, w in H.edges(data="weight") if w < 3])


url2= 'https://github.com/caramnix/Social-Influence-Viz/raw/main/leginfo_116H.csv'
leg_info= pd.read_csv(url2) #"/Users/caranix/Library/CloudStorage/OneDrive-TheOhioStateUniversity/Social Influence/Data/Congress/116/House/leginfo_116H.csv")

leg_info= leg_info.rename(index= leg_info.iloc[:,0].to_dict()) 
leg_info= leg_info.iloc[:,1:]

leg_dict= leg_info.to_dict('index')


nx.set_node_attributes(H, leg_dict)

url3 = 'https://raw.githubusercontent.com/caramnix/Social-Influence-Viz/main/connectedness_house_116.csv'
connectedness_leg= pd.read_csv(url3)

connectedness_leg= connectedness_leg.rename(index= connectedness_leg.iloc[:,0].to_dict()) 
connectedness_leg2= connectedness_leg.iloc[:,1:]

c_dict= connectedness_leg2.to_dict('index')

nx.set_node_attributes(H, c_dict)

alt.data_transformers.disable_max_rows()


H.remove_nodes_from(list(nx.isolates(H)))

c= nxa.draw_networkx(H, 
    node_size='Connectedness:Q',
    node_color= 'Party', 
    node_tooltip=["Full Name","Connectedness"],
    linewidths=0).interactive().properties(width=700, height=700)

#c= nxa.draw_networkx(H, 
#    node_size='Connectedness:Q',
#    node_color= 'Party', 
#    node_tooltip="Full Name").properties(width=700, height=700).interactive()

#c= nxa.draw_networkx(H, node_color= 'Party', node_tooltip="Full Name").properties(width=700, height=700) #) #, cmap= 'bwr',  

st.altair_chart(c)
