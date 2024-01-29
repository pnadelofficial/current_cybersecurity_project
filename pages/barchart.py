import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bar chart")

@st.cache_data
def load_data():
    df = pd.read_excel('./data/Codebook - NVivo_Project_Data_31DED23 (1) - Jan 25, 2024.xlsx')
    df = df.drop(['Folder'], axis=1)
    df['ancestor'] = df.Name.str.split('\\', expand=True)[0]
    df['parent'] = df.Name.str.split('\\', expand=True)[1]
    df['child'] = df.Name.str.split('\\', expand=True)[2]
    df['normalized_refs'] = df.References/df.Files
    df = df.drop(['Name', 'References', 'Files'], axis=1).dropna(subset='normalized_refs').reset_index(drop=True)
    return df[~(df.child.isnull())] # must be leaf node for px

color_mapping = {
    "Liberalism":"cornflowerblue", 
    "Constructivism":"orange", 
    "Realism":"lightgrey", 
    "Cyber Persistence":"darkorange", 
    "Policy Engineering Tasks":"green"
}

df = load_data()
df['Description'] = df['Description'].fillna('No description')
df['Description'] = df['Description'].str.wrap(40).str.replace('\n', '<br>')

selected_parent = st.selectbox('Select parent code', df.ancestor.unique())
df = df[df.ancestor == selected_parent]

fig = px.bar(df, x='normalized_refs', y='child', hover_data='Description', orientation='h')
fig.update_traces(marker_color=color_mapping[selected_parent])
fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=1100)  

st.plotly_chart(fig)