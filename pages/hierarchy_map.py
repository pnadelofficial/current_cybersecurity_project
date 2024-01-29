import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hierarchy map")

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

df = load_data()
df['Description'] = df['Description'].fillna('No description')
df['Description'] = df['Description'].str.wrap(40).str.replace('\n', '<br>')
fig = px.treemap(df, path=[px.Constant("Home"), 'ancestor', 'parent', 'child'], values='normalized_refs', custom_data='Description', ) # colors: follow what's in Nvivo

fig.data[0].texttemplate = "<br><br><em style='font-size:75px'>%{label}</em><br>Code count (normalized by number of files): %{value}<br>Description: %{customdata[0]}"
fig.update_traces(root_color="lightgrey")
fig.update_layout(
    treemapcolorway = ["cornflowerblue", "orange", "lightgrey", "darkorange", "green"],
    margin = dict(t=50, l=50, r=50, b=50)
)

st.plotly_chart(fig,theme="streamlit", use_container_width=True)
