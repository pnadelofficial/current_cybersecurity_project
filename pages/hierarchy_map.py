import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.title("Hierarchy map")

@st.cache_data
def load_data():
    df = pd.read_excel('./data/Codebook - NVivo_Project_Data_FEB24 - Mar 4, 2024.xlsx')
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
    treemapcolorway = ["darkgreen", "darkblue", "darkred", "teal", "saddlebrown"],
    margin = dict(t=50, l=50, r=50, b=50)
)

st.plotly_chart(fig,theme="streamlit", use_container_width=True)

st.header("Document level (name TBD)")

doc_mapping = {
    '2009 Cyberspace Policy Review Assuring a Trusted and R':'2009 Cyberspace Policy Review_CLEAN',
    '2010_national_security_strategy':'2010_national_security_strategy_CLEAN',
    '2011 DOD Strategy for Operating in Cy':'2011 DOD Strategy for Operating in Cyber_CLEAN',
    '2011':'2011-national-military-strategy_CLEAN',
    '2011_International_strategy_for_cyberspace':'2011_international_strategy_for_cyberspace_CLEAN',
    'QDR as of 29JAN10 1600':'2010_QDR_CLEAN'
}
rev_doc_mapping = {v:k for k,v in doc_mapping.items()}

choices = st.multiselect("Choose documents to compare", list(doc_mapping.values()))
choices_rev = [rev_doc_mapping[c] for c in choices]
if len(choices) > 0:
    if len(choices) < 3:
        cols = st.columns(len(choices))
        for i, col in enumerate(cols):
            with col:
                fig = utils.plot_treemap_from_ps(choices_rev[i])
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices)
        for i, tab in enumerate(tabs):
            with tab:
                fig = utils.plot_treemap_from_ps(choices_rev[i])
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

