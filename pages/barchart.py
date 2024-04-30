import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.title("Bar chart")

st.header('All codes by parent code')
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

color_mapping = {
    "Academic Interaction":"gold",
    "Liberalism":"darkgreen", 
    "Constructivism":"darkblue", 
    "Realism":"darkred", 
    "Cyber Persistence":"saddlebrown", 
    "Policy Engineering Tasks":"teal"
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

st.header("Document level")

doc_mapping = {
    '2009 Cyberspace Policy Review Assuring a Trusted and R':'2009 Cyberspace Policy Review_CLEAN',
    '2010_national_security_strategy':'2010_national_security_strategy_CLEAN',
    '2011 DOD Strategy for Operating in Cy':'2011 DOD Strategy for Operating in Cyber_CLEAN',
    '2011':'2011-national-military-strategy_CLEAN',
    '2011_International_strategy_for_cyberspace':'2011_international_strategy_for_cyberspace_CLEAN',
    'QDR as of 29JAN10 1600':'2010_QDR_CLEAN',
    "2015 National Security Strategy CLEAN": "2015 National Security Strategy CLEAN",
    '2015 WH Report on Cyber Deterrence Policy Final CLEAN': '2015 WH Report on Cyber Deterrence Policy Final CLEAN',
    '2014 Quadrennial Defense Review CLEAN': '2014 Quadrennial Defense Review CLEAN',
    '2015 DOD Cyber Strategy CLEAN': '2015 DOD Cyber Strategy CLEAN',
    '2015 National Military Strategy CLEAN': '2015 National Military Strategy CLEAN',
}
rev_doc_mapping = {v:k for k,v in doc_mapping.items()}

st.header("Top level codes by documents")

choices_top_level = st.multiselect("Choose documents to compare", list(doc_mapping.values()), key=0)
choices_top_level  = [rev_doc_mapping[c] for c in choices_top_level ]

if len(choices_top_level ) > 0:
    if len(choices_top_level) < 3:
        cols = st.columns(len(choices_top_level ))
        for i, col in enumerate(cols):
            with col:
                df = utils.make_df_from_ps_top_level(choices_top_level[i])
                fig = px.bar(df, x='refs', y='child', title=doc_mapping[choices_top_level [i]], orientation='h')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices_top_level)
        for i, tab in enumerate(tabs):
            with tab:
                df = utils.make_df_from_ps_top_level(choices_top_level[i])
                fig = px.bar(df, x='refs', y='child', title=doc_mapping[choices_top_level [i]], orientation='h')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.header('All codes by documents')

choices = st.multiselect("Choose documents to compare", list(doc_mapping.values()), key=1)
choices = [rev_doc_mapping[c] for c in choices]

if len(choices) > 0:
    if len(choices) < 3:
        cols = st.columns(len(choices))
        for i, col in enumerate(cols):
            with col:
                df = utils.make_df_from_ps(choices[i])
                fig = px.bar(df, x='refs', y='child', title=doc_mapping[choices[i]], orientation='h')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices)
        for i, tab in enumerate(tabs):
            with tab:
                df = utils.make_df_from_ps(choices[i])
                fig = px.bar(df, x='refs', y='child', title=doc_mapping[choices[i]], orientation='h')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)